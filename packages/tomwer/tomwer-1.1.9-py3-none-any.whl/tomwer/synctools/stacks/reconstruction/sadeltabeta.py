# coding: utf-8
###########################################################################
# Copyright (C) 2016-2019 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "08/06/2021"


from processview.core.manager import ProcessManager
from tomwer.synctools.sadeltabeta import QSADeltaBetaParams
from tomwer.synctools.axis import QAxisRP
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.process.reconstruction.sadeltabeta.sadeltabeta import (
    SADeltaBetaProcess,
)
from tomwer.core.settings import get_lbsram_path, isOnLbsram
from tomwer.core.utils import isLowOnMemory
from processview.core.manager import DatasetState
from ..processingstack import FIFO, ProcessingThread
from processview.core.superviseprocess import SuperviseProcess
from tomwer.io.utils import format_stderr_stdout
from silx.gui import qt
import logging
import functools

_logger = logging.getLogger(__name__)


class SADeltaBetaProcessStack(FIFO, qt.QObject):
    """Implementation of the `.AxisProcess` but having a stack for treating
    scans and making computation in threads"""

    def __init__(self, sa_delta_beta_params, process_id=None):
        qt.QObject.__init__(self)
        FIFO.__init__(self, process_id=process_id)
        assert sa_delta_beta_params is not None
        self._dry_run = False
        self._process_fct = None

    def patch_processing(self, process_fct):
        self._computationThread.patch_processing(process_fct)

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    def _process(self, data, configuration, callback=None):
        ProcessManager().notify_dataset_state(
            dataset=data,
            process=self,
            state=DatasetState.ON_GOING,
        )
        _logger.processStarted("start sa-delta-beta {}" "".format(str(data)))
        assert isinstance(data, TomwerScanBase)
        if data.axis_params is None:
            data.axis_params = QAxisRP()
        if data.sa_delta_beta_params is None:
            data.sa_delta_beta_params = QSADeltaBetaParams()
        self._data_currently_computed = data
        sa_delta_beta_params = QSADeltaBetaParams.from_dict(configuration)
        if isOnLbsram(data) and isLowOnMemory(get_lbsram_path()) is True:
            # if computer is running into low memory on lbsram skip it
            mess = "low memory, skip sa-delta-beta-axis calculation", data.path
            ProcessManager().notify_dataset_state(
                dataset=data, process=self._process_id, state=DatasetState.SKIPPED
            )
            _logger.processSkipped(mess)
            data.sa_delta_beta_params.set_value(None)
            if callback is not None:
                callback()
            self.scan_ready(scan=data)
        else:
            self._data_currently_computed = data
            self._computationThread.init(
                data=data, sa_delta_beta_params=sa_delta_beta_params
            )
            # need to manage connect before starting it because
            fct_callback = functools.partial(self._end_threaded_computation, callback)
            self._computationThread.finished.connect(fct_callback)
            self._computationThread.start()

    def _end_computation(self, data, future_tomo_obj, callback):
        """
        callback when the computation thread is finished

        :param scan: pass if no call to '_computationThread is made'
        """
        assert isinstance(data, TomwerScanBase)
        FIFO._end_computation(
            self, data=data, future_tomo_obj=future_tomo_obj, callback=callback
        )

    def _end_threaded_computation(self, callback=None):
        assert self._data_currently_computed is not None
        self._computationThread.finished.disconnect()
        if callback:
            callback()
        FIFO._end_threaded_computation(self)

    def _create_processing_thread(self, process_id=None) -> qt.QThread:
        return _ProcessingThread(process_id=process_id)


class _ProcessingThread(ProcessingThread, SuperviseProcess):
    """
    Thread use to execute the processing of the axis position
    """

    def __init__(self, process_id=None):
        SuperviseProcess.__init__(self, process_id=process_id)
        try:
            ProcessingThread.__init__(self, process_id=process_id)
        except TypeError:
            ProcessingThread.__init__(self)
        self.center_of_rotation = None
        self._dry_run = False
        self._scan = None
        self._sa_delta_beta_params = None
        self._patch_process_fct = None
        """function pointer to know which function to call for the axis
        calculation"""
        self.__patch = {}
        """Used to patch some calculation method (for test purpose)"""

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    def patch_processing(self, process_fct):
        self._patch_process_fct = process_fct

    def init(self, data, sa_delta_beta_params):
        self._scan = data
        self._sa_delta_beta_params = sa_delta_beta_params

    def run(self):
        self.sigComputationStarted.emit()
        if self._patch_process_fct:
            scores = {}
            for db in self._sa_delta_beta_params.delta_beta_values:
                scores[db] = self._patch_process_fct(db)
            self._scan.sa_delta_beta_params.scores = scores
            SADeltaBetaProcess.autofocus(scan=self._scan)
            self.db_value = self._scan.sa_delta_beta_params.autofocus
        else:
            sa_delta_beta = SADeltaBetaProcess(
                inputs={
                    "dump_process": False,
                    "data": self._scan,
                    "dry_run": self._dry_run,
                    "sa_delta_beta_params": self._sa_delta_beta_params,
                },
                process_id=self.process_id,
            )
            # loop is required for distributed since version 2021
            try:
                sa_delta_beta.run()
            except Exception as e:
                _logger.error(str(e))
                mess = "SADeltaBeta computation for {} failed.".format(str(self._scan))
                state = DatasetState.FAILED
            else:
                mess = "SADeltaBeta computation for {} succeed.".format(str(self._scan))
                state = DatasetState.WAIT_USER_VALIDATION
                self.db_value = self._scan.sa_delta_beta_params.autofocus

            nabu_logs = []
            for std_err, std_out in zip(sa_delta_beta.std_errs, sa_delta_beta.std_outs):
                nabu_logs.append(format_stderr_stdout(stdout=std_out, stderr=std_err))
            self._nabu_log = nabu_logs
            nabu_logs.insert(0, mess)
            details = "\n".join(nabu_logs)
            ProcessManager().notify_dataset_state(
                dataset=self._scan,
                process=self,
                state=state,
                details=details,
            )

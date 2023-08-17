# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "30/07/2020"


from tomwer.core.utils.scanutils import format_output_location
from tomwer.core.process.task import TaskWithProgress
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from nxtomomill import converter as nxtomomill_converter
from nxtomomill.io.config import TomoHDF5Config as HDF5Config
from nxtomomill.io.config import TomoEDFConfig as EDFConfig

import os
import logging

_logger = logging.getLogger(__name__)


class H5ToNxProcess(
    TaskWithProgress,
    input_names=("h5_to_nx_configuration",),
    optional_input_names=("progress", "hdf5_scan"),
    output_names=("data",),
):
    """
    Process to convert from a bliss dataset to a nexus compliant dataset
    """

    @staticmethod
    def deduce_output_file_path(master_file_name, scan, entry, outputdir=None):
        if outputdir is not None:
            file_dir = outputdir
        else:
            file_dir = os.path.dirname(master_file_name)
        file_name = os.path.basename(master_file_name)
        if "." in file_name:
            file_name = "".join(file_name.split(".")[:-1])

        entry_for_file_name = entry.lstrip("/")
        entry_for_file_name = entry_for_file_name.replace("/", "_")
        entry_for_file_name = entry_for_file_name.replace(".", "_")
        entry_for_file_name = entry_for_file_name.replace(":", "_")
        output_file_name = "_".join(
            (os.path.splitext(file_name)[0], entry_for_file_name + ".nx")
        )
        file_dir = format_output_location(file_dir, scan=scan)
        return os.path.join(file_dir, output_file_name)

    def run(self):
        config = self.inputs.h5_to_nx_configuration
        if isinstance(config, dict):
            config = HDF5Config.from_dict(config)
        elif not isinstance(config, HDF5Config):
            raise TypeError(
                "h5_to_nx_configuration should be a dict or an instance of {HDF5Config}"
            )
        config.bam_single_file = True
        try:
            convs = nxtomomill_converter.from_h5_to_nx(
                configuration=config, progress=self.progress
            )
        except Exception as e:
            _logger.error(e)
            pass

        if not len(convs) <= 1:
            raise RuntimeError(
                f"the H5ToNxProcess expects to create at most one NXtomo. {len(convs)} created"
            )
        for conv in convs:
            conv_file, conv_entry = conv
            scan_converted = HDF5TomoScan(scan=conv_file, entry=conv_entry)
            _logger.processSucceed(
                f"{config.input_file} {config.entries} has been translated to {scan_converted}"
            )
            self.outputs.data = scan_converted


class EDFToNxProcess(
    TaskWithProgress,
    input_names=("edf_to_nx_configuration",),
    optional_input_names=("progress", "edf_scan"),
    output_names=("data",),
):
    """
    Task calling edf2nx in order to insure conversion from .edf to .nx (create one NXtomo to be used elsewhere)
    """

    def run(self):
        config = self.inputs.edf_to_nx_configuration
        if isinstance(config, dict):
            config = EDFConfig.from_dict(config)
        elif not isinstance(config, EDFConfig):
            raise TypeError(
                "edf_to_nx_configuration should be a dict or an instance of {TomoEDFConfig}"
            )
        file_path, entry = nxtomomill_converter.from_edf_to_nx(
            configuration=config, progress=self.progress
        )
        self.outputs.data = HDF5TomoScan(entry=entry, scan=file_path)

    @staticmethod
    def deduce_output_file_path(folder_path, output_dir, scan):
        if output_dir is None:
            output_dir = os.path.dirname(folder_path)

        folder_path = format_output_location(folder_path, scan=scan)
        return os.path.join(output_dir, os.path.basename(folder_path) + ".nx")

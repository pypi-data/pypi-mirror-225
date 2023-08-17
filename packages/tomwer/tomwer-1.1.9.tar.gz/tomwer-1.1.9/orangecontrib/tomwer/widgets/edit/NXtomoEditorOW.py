from orangewidget import gui
from tomwer.gui.edit.nxtomoeditor import NXtomoEditorDialog as _NXtomoEditorDialog
from orangewidget.widget import Input, Output
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from silx.gui import qt
from ...orange.managedprocess import SuperviseOW
import logging

_logger = logging.getLogger(__name__)


class NXtomoEditorDialog(_NXtomoEditorDialog):
    def __init__(self, parent) -> None:
        assert isinstance(parent, SuperviseOW)
        self._ow = parent
        # we need to save it become looks like orange is doing some stuff with parenting
        super().__init__(parent)

        # connect signal / slot
        self._buttons.button(qt.QDialogButtonBox.Ok).released.connect(
            self._overwriteNXtomo
        )

    def _overwriteNXtomo(self, *args, **kwargs):
        scan = self.mainWidget.getScan()
        if scan is not None:
            assert isinstance(self._ow, SuperviseOW)
            try:
                self.overwriteNXtomo()
            except Exception as e:
                _logger.error(
                    f"Fail to overwrite NXtomo ({scan.get_identifier().to_str()}). Error is {e}"
                )
                self._ow.notify_failed(scan=scan)
            else:
                self._ow.notify_succeed(scan=scan)
                # self.validate()
            self._ow._validateScan(scan)


class NXtomoEditorOW(SuperviseOW):
    """
    Widget to edit manually an NXtomo
    """

    name = "nxtomo-editor"
    id = "orange.widgets.tomwer.edit.NXtomoEditorOW.NXtomoEditorOW"
    description = "Interface to edit manually a NXtomo"
    icon = "icons/nx_tomo_editor.svg"
    priority = 10
    keywords = [
        "hdf5",
        "nexus",
        "tomwer",
        "file",
        "edition",
        "NXTomo",
        "editor",
        "energy",
        "distance",
        "pixel size",
    ]

    class Inputs:
        data = Input(name="data", type=TomwerScanBase)

    class Outputs:
        data = Output(name="data", type=TomwerScanBase)

    want_main_area = True
    resizing_enabled = True
    compress_signal = False

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        _layout = gui.vBox(self.mainArea, self.name).layout()
        self.widget = NXtomoEditorDialog(parent=self)
        _layout.addWidget(self.widget)

    def _validateScan(self, scan):
        self.Outputs.data.send(scan)
        super().hide()

    @Inputs.data
    def setScan(self, scan):
        if scan is None:
            pass
        elif not isinstance(scan, HDF5TomoScan):
            raise TypeError(
                f"expect to have an instance of {HDF5TomoScan}. {type(scan)} provided."
            )
        else:
            self.widget.setScan(scan)
            self.show()
            self.raise_()

    def sizeHint(self):
        return qt.QSize(400, 500)

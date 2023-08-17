import gc
import pytest
from silx.gui import qt
from tomwer.tests.utils import skip_gui_test
from silx.gui.utils.testutils import TestCaseQt
from orangecontrib.tomwer.widgets.edit.NXtomoEditorOW import NXtomoEditorOW


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestNXtomoEditorOW(TestCaseQt):
    """Test that the NXtomoEditorOW widget work correctly. Processing test are done in the core module. gui test are done in the tomwer.gui.edit module"""

    def setUp(self):
        super().setUp()
        self._window = NXtomoEditorOW()

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        self._window = None
        gc.collect()

    def test(self):
        self._window.show()
        self.qWaitForWindowExposed(self._window)

import pytest
from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.gui.qfolderdialog import QDataDialog


@pytest.mark.parametrize("multi_selection", (True, False))
def test_qdata_dialog(
    qtapp,  # noqa F401
    multi_selection,
):
    dialog = QDataDialog(parent=None, multiSelection=multi_selection)
    dialog.files_selected()

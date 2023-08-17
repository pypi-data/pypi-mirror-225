from ewokscore.task import Task as EwoksTask
from tomwer.core.utils.scanutils import data_identifier_to_scan


class _VolumeSelectorPlaceHolder(
    EwoksTask, input_names=["volume"], output_names=["volume"]
):
    def run(self):
        self.outputs.volume = data_identifier_to_scan(self.inputs.volume)

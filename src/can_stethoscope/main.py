from can_stethoscope.data_processor import ProcessCanData
from can_stethoscope.file_manager import FileManager


class DataProcessor:
    def __init__(self, file_dir, file_prefix=None):
        file_manager = FileManager(file_dir,
                                   file_prefix)
        file_manager.read_file_data()
        self.data = ProcessCanData(scope_data=file_manager.scope_data)
        self.data.generate_duration()

    def _get_can_frames(self) -> list:
        return self.data.generate_can_msg_list()

    def plot_raw_volts(self):
        self.data.plot_raw_volts()

    def plot_binary(self):
        self.data.plot_binary()

    def plot_binary_durations(self):
        self.data.describe_and_plot_binary_duration()

    def print_basic_description(self):
        self.data.basic_stats()

    def print_can_frames(self):
        for each_frame in self._get_can_frames():
            print(each_frame)

    def can_to_csv(self, file_name: str):
        if '.csv' == file_name[-4:]:
            file_name = file_name[:-4]
        self.data.can_to_csv(file_name)

    def plot_single_frame(self, index, every_sample=False, show_volts=False):
        self.data.plot_single_frame(index, every_sample, show_volts)

    def plot_every_frame(self, file, show_volts=False):
        self.data.plot_every_frame(file, show_volts)


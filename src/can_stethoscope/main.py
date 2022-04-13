from can_stethoscope.data_processor import ProcessCanData
from can_stethoscope.file_manager import FileManager


class DataProcessor:
    def __init__(self, additional_data_dir: str = None):
        file_manager = FileManager('F250',
                                   'clean_f250_2',
                                   additional_data_dir)
        file_manager.process_raw_filenames()
        self.data = ProcessCanData(scope_data=file_manager.scope_data)
        self.data.generate_duration()

    def plot_can(self):
        self.data.filter_binary()
        self.data.can_plot()

    def plot_binary_durations(self):
        self.data.describe_and_plot_binary_duration()

    def print_basic_description(self):
        self.data.basic_stats()

    def get_can_frames(self) -> list:
        return self.data.generate_can_msg_list()


def main():
    processor = DataProcessor()
    processor.print_basic_description()
    processor.get_can_frames()
    processor.plot_binary_durations()


def print_basic_description():
    processor = DataProcessor()
    processor.print_basic_description()


def get_can_frames(data_dir=None):
    processor = DataProcessor(additional_data_dir=data_dir)
    print(processor.get_can_frames())

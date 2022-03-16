from can_stethoscope.data_processor import ProcessCanData
from can_stethoscope.file_manager import FileManager


class DataProcessor:
    def __init__(self):
        file_manager = FileManager('F250', 'clean_f250_2')
        file_manager.process_raw_filenames()
        self.data = ProcessCanData(scope_data=file_manager.scope_data)

    def plot_can(self):
        self.data.filter_binary()
        self.data.can_plot()

    def print_basic_description(self):
        self.data.basic_stats()

    def get_can_frames(self):
        self.data.generate_duration()


def main():
    processor = DataProcessor()
    processor.get_can_frames()
    processor.data.describe_and_plot_binary_duration()


if __name__ == '__main__':
    main()

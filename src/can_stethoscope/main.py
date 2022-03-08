from can_stethoscope.data_processor import ProcessCanData
from can_stethoscope.file_manager import FileManager


def main():
    file_manager = FileManager('F250', 'clean_f250_2')
    file_manager.process_raw_filenames()
    data_processor = ProcessCanData(scope_data=file_manager.scope_data)
    data_processor.filter_binary()
    data_processor.can_plot()


if __name__ == '__main__':
    main()




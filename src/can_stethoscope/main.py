from data_processor import ProcessCanData
from file_manager import FileManager


def main():
    file_manager = FileManager('F250', 'clean_f250_2')
    file_manager.process_raw_filenames()
    data_processor = ProcessCanData(scope_data=file_manager.scope_data)
    data_processor.voltage_observation()


if __name__ == '__main__':
    main()




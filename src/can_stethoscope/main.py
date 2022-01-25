from data_processor import ProcessCanData
from file_manager import FileManager


def main():
    file_manager = FileManager('civi', 'clean_civic')
    file_manager.process_raw_filenames()
    data_processor = ProcessCanData(scope_data=file_manager.scope_data)
    data_processor.basic_stats()


if __name__ == '__main__':
    main()




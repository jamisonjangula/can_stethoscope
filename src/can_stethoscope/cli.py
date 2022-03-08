import argparse
import pkg_resources
from can_stethoscope.file_manager import FileManager
from can_stethoscope.data_processor import ProcessCanData


def main():
    parser = argparse.ArgumentParser('can_stetho',
                                     description="Generate insights on CAN data from file or streamed in from hardware")
    subparsers = parser.add_subparsers(dest="subparser")

    subparsers.add_parser("version",
                          help="Displays can-stetho version")

    process_csv_parser = subparsers.add_parser("process-oscope-csv",
                                               help="prepare data for analysis")
    process_csv_parser.add_argument("--file",
                                    type=str,
                                    help="File Path to file to import",
                                    required=True)
    process_csv_parser.add_argument("--prefix",
                                    type=str,
                                    default="stetho_cleaned",
                                    help="File prefix for final cleaned data file",
                                    required=True)

    get_msg_parser = subparsers.add_parser("get-messages",
                                           help="get a list of CAN messages and their timestamp")
    get_msg_parser.add_argument("--file",
                                type=str,
                                help="File Path to the imported dataset which contains voltage mesasurements",
                                required=True)

    args = parser.parse_args()
    if args.subparser == "version":
        print(f"{pkg_resources.get_distribution('can_stethoscope').version}")
    elif args.subparser == "process-oscope-csv":
        file_manager = FileManager(clean_file_name=args.prefix,
                                   split_file_name="can_stetho")
        file_manager.process_raw_filenames()
    elif args.subparser == "get_ford_messages":
        file_manager = FileManager('F250', 'clean_f250_2')
        file_manager.process_raw_filenames()
        data_processor = ProcessCanData(scope_data=file_manager.scope_data)
        data_processor.histogram_plot()
    else:
        parser.print_help()

import argparse
import pkg_resources
from can_stethoscope.file_manager import FileManager
from can_stethoscope.data_processor import ProcessCanData
from can_stethoscope.main import get_can_frames
from can_stethoscope.main import plot_voltages


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
    get_msg_parser.add_argument("-d",
                                "--dir",
                                type=str,
                                help="File Path to the imported dataset which contains voltage measurements")

    graph_volts = subparsers.add_parser("graph-volts",
                                        help="get a list of CAN messages and their timestamp")
    graph_volts.add_argument("-d",
                             "--dir",
                             type=str,
                             help="File Path to the imported dataset which contains voltage measurements")

    args = parser.parse_args()
    if args.subparser == "version":
        print(f"{pkg_resources.get_distribution('can_stethoscope').version}")
    elif args.subparser == "process-oscope-csv":
        file_manager = FileManager(clean_file_name=args.prefix,
                                   split_file_name="can_stetho")
        file_manager.process_raw_filenames()
    elif args.subparser == "get-messages":
        if args.dir:
            get_can_frames(data_dir=args.dir)
        else:
            get_can_frames()
    elif args.subparser == "graph-volts":
        if args.dir:
            plot_voltages(data_dir=args.dir)
        else:
            plot_voltages()
    else:
        parser.print_help()

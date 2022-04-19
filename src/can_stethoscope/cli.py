import argparse
import pkg_resources
from can_stethoscope.file_manager import FileManager
from can_stethoscope.main import DataProcessor


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

    print_can_frames = subparsers.add_parser("print-can-frames",
                                             help="get a list of CAN messages and their timestamp")
    print_can_frames.add_argument("-d",
                                  "--dir",
                                  type=str,
                                  help="File Path to the imported dataset which contains voltage measurements")

    can_frames_csv = subparsers.add_parser("can-frames-to-csv",
                                           help="get a list of CAN messages and their timestamp")
    can_frames_csv.add_argument("file",
                                type=str,
                                help="File Path to record to")
    can_frames_csv.add_argument("-d",
                                "--dir",
                                type=str,
                                help="File Path to the imported dataset which contains voltage measurements")

    plot_raw_volts = subparsers.add_parser("plot-raw-volts",
                                           help="get a list of CAN messages and their timestamp")
    plot_raw_volts.add_argument("-d",
                                "--dir",
                                type=str,
                                help="File Path to the imported dataset which contains voltage measurements")

    plot_single_frame = subparsers.add_parser("plot-single-frame",
                                              help="get a list of CAN messages and their timestamp")
    plot_single_frame.add_argument("index",
                                   type=int)
    plot_single_frame.add_argument("-d",
                                   "--dir",
                                   type=str,
                                   help="File Path to the imported dataset which contains voltage measurements")

    plot_binary = subparsers.add_parser("plot-binary",
                                        help="graph binary values by time")
    plot_binary.add_argument("-d",
                             "--dir",
                             type=str,
                             help="File Path to the imported dataset which contains voltage measurements")

    plot_binary_durations = subparsers.add_parser("plot-binary-durations",
                                                  help="graph binary duration lengths")
    plot_binary_durations.add_argument("-d",
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
    elif args.subparser == "print-can-frames":
        data_processor = DataProcessor(additional_data_dir=args.dir)
        data_processor.print_can_frames()
    elif args.subparser == "can-frames-to-csv":
        data_processor = DataProcessor(additional_data_dir=args.dir)
        data_processor.can_to_csv(args.file)
    elif args.subparser == "plot-raw-volts":
        data_processor = DataProcessor(additional_data_dir=args.dir)
        data_processor.plot_raw_volts()
    elif args.subparser == "plot-single-frame":
        data_processor = DataProcessor(additional_data_dir=args.dir)
        data_processor.plot_single_frame(args.index)
    elif args.subparser == "plot-binary":
        data_processor = DataProcessor(additional_data_dir=args.dir)
        data_processor.plot_binary()
    elif args.subparser == "plot-binary-durations":
        data_processor = DataProcessor(additional_data_dir=args.dir)
        data_processor.plot_binary_durations()
    else:
        parser.print_help()

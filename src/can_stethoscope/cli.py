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

    process_raw = subparsers.add_parser("process-raw",
                                        help="prepare data for analysis")
    process_raw.add_argument("dir",
                             default="raw_can_data",
                             type=str,
                             help="string of the path to the directory that contains the raw data")
    process_raw.add_argument("--prefix",
                             type=str,
                             help="string to appear at the beginning of the processed data files")

    print_can_frames = subparsers.add_parser("print-can-frames",
                                             help="get a list of CAN messages and their timestamp")
    print_can_frames.add_argument("--dir",
                                  default="raw_can_data",
                                  type=str,
                                  help="string of the path to the directory that contains the raw data")
    print_can_frames.add_argument("--prefix",
                                  type=str,
                                  help="string to appear at the beginning of the processed data files")

    can_frames_csv = subparsers.add_parser("can-frames-to-csv",
                                           help="save all the raw frame data to a csv file")
    can_frames_csv.add_argument("file",
                                type=str,
                                help="File Path to record to")
    can_frames_csv.add_argument("--dir",
                                default="raw_can_data",
                                type=str,
                                help="string of the path to the directory that contains the raw data")
    can_frames_csv.add_argument("--prefix",
                                type=str,
                                help="string to appear at the beginning of the processed data files")

    plot_raw_volts = subparsers.add_parser("plot-raw-volts",
                                           help="graph raw voltage measurements")
    plot_raw_volts.add_argument("--dir",
                                default="raw_can_data",
                                type=str,
                                help="string of the path to the directory that contains the raw data")
    plot_raw_volts.add_argument("--prefix",
                                type=str,
                                help="string to appear at the beginning of the processed data files")

    plot_single_frame = subparsers.add_parser("plot-single-frame",
                                              help="graph a single can frame in the data recorded")
    plot_single_frame.add_argument("index",
                                   type=int)
    plot_single_frame.add_argument("-e",
                                   help="displays a line where every sample was taken",
                                   action='store_true')
    plot_single_frame.add_argument("-v",
                                   help="displays raw voltage",
                                   action='store_true')
    plot_single_frame.add_argument("--dir",
                                   default="raw_can_data",
                                   type=str,
                                   help="string of the path to the directory that contains the raw data")
    plot_single_frame.add_argument("--prefix",
                                   type=str,
                                   help="string to appear at the beginning of the processed data files")

    plot_every_frame = subparsers.add_parser("plot-every-frame",
                                             help="graph every can frame")
    plot_every_frame.add_argument("file",
                                  type=str,
                                  help="File Path to record to")
    plot_every_frame.add_argument("-v",
                                  help="displays raw voltage",
                                  action='store_true')
    plot_every_frame.add_argument("--dir",
                                  default="raw_can_data",
                                  type=str,
                                  help="string of the path to the directory that contains the raw data")
    plot_every_frame.add_argument("--prefix",
                                  type=str,
                                  help="string to appear at the beginning of the processed data files")

    plot_binary = subparsers.add_parser("plot-binary",
                                        help="graph binary values by time")
    plot_binary.add_argument("--dir",
                             default="raw_can_data",
                             type=str,
                             help="string of the path to the directory that contains the raw data")
    plot_binary.add_argument("--prefix",
                             type=str,
                             help="string to appear at the beginning of the processed data files")

    plot_binary_durations = subparsers.add_parser("plot-binary-durations",
                                                  help="graph binary duration lengths")
    plot_binary_durations.add_argument("--dir",
                                       default="raw_can_data",
                                       type=str,
                                       help="string of the path to the directory that contains the raw data")
    plot_binary_durations.add_argument("--prefix",
                                       type=str,
                                       help="string to appear at the beginning of the processed data files")

    args = parser.parse_args()
    if args.subparser == "version":
        print(f"{pkg_resources.get_distribution('can_stethoscope').version}")
    elif args.subparser == "process-raw":
        file_manager = FileManager(file_dir=args.dir,
                                   file_prefix=args.prefix)
        file_manager.load_created_files()
    elif args.subparser == "print-can-frames":
        data_processor = DataProcessor(file_dir=args.dir,
                                       file_prefix=args.prefix)
        data_processor.print_can_frames()
    elif args.subparser == "can-frames-to-csv":
        data_processor = DataProcessor(file_dir=args.dir,
                                       file_prefix=args.prefix)
        data_processor.can_to_csv(args.file)
    elif args.subparser == "plot-raw-volts":
        data_processor = DataProcessor(file_dir=args.dir,
                                       file_prefix=args.prefix)
        data_processor.plot_raw_volts()
    elif args.subparser == "plot-single-frame":
        data_processor = DataProcessor(file_dir=args.dir,
                                       file_prefix=args.prefix)
        data_processor.plot_single_frame(args.index, args.e, args.v)
    elif args.subparser == "plot-every-frame":
        data_processor = DataProcessor(file_dir=args.dir,
                                       file_prefix=args.prefix)
        data_processor.plot_every_frame(args.file, args.v)
    elif args.subparser == "plot-binary":
        data_processor = DataProcessor(file_dir=args.dir,
                                       file_prefix=args.prefix)
        data_processor.plot_binary()
    elif args.subparser == "plot-binary-durations":
        data_processor = DataProcessor(file_dir=args.dir,
                                       file_prefix=args.prefix)
        data_processor.plot_binary_durations()
    else:
        parser.print_help()

import argparse
import sys

from .summary import read_csv, summarize


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize normalized bioassay observations")
    subparsers = parser.add_subparsers(dest="command", required=True)
    summary_parser = subparsers.add_parser("summarize")
    summary_parser.add_argument("input", help="input observation CSV")
    args = parser.parse_args()
    if args.command == "summarize":
        print("compound\tassay\tconcentration\tunit\tn\tmean_activity\tsd_activity")
        for result in summarize(read_csv(args.input)):
            sd = "" if result.sd_activity is None else f"{result.sd_activity:.6g}"
            print(f"{result.compound}\t{result.assay}\t{result.concentration:g}\t{result.unit}"
                  f"\t{result.n}\t{result.mean_activity:.6g}\t{sd}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

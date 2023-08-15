import sys
from argparse import ArgumentParser, FileType
from datetime import datetime

import dateiter
from dateiter import DEFAULT_DATE_FORMAT


class App:
    @classmethod
    def run(cls, args: list[str] | None = None):
        parser = ArgumentParser(
            prog="dateiter",
            description="date iterator tool.",
        )

        parser.add_argument(
            "--version",
            action="version",
            version=f"%(prog)s {dateiter.__version__}",
        )

        parser.add_argument(
            "start",
            type=str,
            nargs="?",
            help="start date. format: YYYY-MM-DD",
        )
        parser.add_argument(
            "--start-date",
            type=str,
            help="start date. format: YYYY-MM-DD",
        )

        parser.add_argument(
            "end",
            type=str,
            nargs="?",
            help="end date. format: YYYY-MM-DD",
        )
        parser.add_argument(
            "--end-date",
            type=str,
            help="end date. format: YYYY-MM-DD",
        )

        parser.add_argument(
            "--step",
            type=int,
            default=1,
            help="iteration step[day] (Default: 1).",
        )

        parser.add_argument(
            "--input-date-format",
            type=str,
            default=DEFAULT_DATE_FORMAT,
            help=(
                f"input date format (Default: {DEFAULT_DATE_FORMAT}).".replace(
                    "%", "%%"
                )
            ),
        )

        parser.add_argument(
            "--format",
            "--output-date-format",
            type=str,
            default=DEFAULT_DATE_FORMAT,
            help=(
                f"output date format (Default: {DEFAULT_DATE_FORMAT}).".replace(
                    "%", "%%"
                )
            ),
        )

        parser.add_argument(
            "--output-file",
            "-o",
            type=FileType("w"),
            help="output file (Default=stdout).",
        )

        space = parser.parse_args(args)

        if space.start_date is not None:
            start_date = space.start_date
        else:
            if space.start is not None:
                start_date = space.start
            elif space.end_date is not None:
                start_date = space.end_date
            else:
                start_date = datetime.today().strftime(space.input_date_format)

        if space.end_date is not None:
            end_date = space.end_date
        else:
            if space.end is not None:
                end_date = space.end
            else:
                end_date = None

        for date in dateiter.dateiter(
            start_date,
            end_date,
            step=space.step,
            format=space.input_date_format,
        ):
            print(date.strftime(space.format), file=space.output_file)


def main():
    try:
        App.run()
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()

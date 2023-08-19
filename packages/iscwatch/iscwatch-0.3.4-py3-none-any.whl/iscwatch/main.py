import csv
import datetime
import logging
import logging.config
import sys
from dataclasses import asdict, fields
from typing import Annotated, Final

import pkg_resources
import typer

from iscwatch.advisory import Advisory
from iscwatch.logconfig import logging_config
from iscwatch.scrape import iter_advisories

logging.config.dictConfig(logging_config)

PACKAGE_NAME: Final = "iscwatch"


def cli():
    """CLI entry point executes typer-wrapped main function"""
    typer.run(main)


def main(
    since: Annotated[
        datetime.datetime,
        typer.Option(
            "--since",
            "-s",
            help="Only output those advisories updated or released since specified date.",
            formats=["%Y-%m-%d"],
        ),
    ] = datetime.datetime.min,
    version: Annotated[
        bool,
        typer.Option("--version", "-v", help="Show iscwatch application version and exit."),
    ] = False,
    no_headers: Annotated[
        bool,
        typer.Option(
            "--no-headers", "-n", help="Omit column headers from CSV advisory summary output."
        ),
    ] = False,
    last_updated: Annotated[
        bool,
        typer.Option(
            "--last-updated",
            "-l",
            help="Show date when Intel last updated its security advisories and exit.",
        ),
    ] = False,
):
    """Output security advisory summaries from the Intel Security Center website.
    
    With no options, iscwatch outputs all Intel security advisory summaries in CSV format with
    column headers.  Typically, a starting date is specified using the --since option to 
    constrain the output to a manageable subset.
    
    """
    if version:
        print_version()
    elif last_updated:
        last_updated_advisory = max(iter_advisories(), key=lambda a: a.updated)
        print(last_updated_advisory.updated)
    else:  # output advisories
        selected_advisories = [
            a for a in iter_advisories() if not since or a.updated >= since.date()
        ]
        print_csv_advisories(selected_advisories, no_headers)


def print_csv_advisories(advisories: list[Advisory], no_headers: bool):
    """Convert advisories into dictionaries and output in CSV format."""
    fieldnames = [field.name for field in fields(Advisory)]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, lineterminator="\n")
    if not no_headers:
        writer.writeheader()
    writer.writerows(asdict(advisory) for advisory in advisories)


def print_version():
    """Output current version of the application."""
    try:
        distribution = pkg_resources.get_distribution(PACKAGE_NAME)
        print(f"{distribution.project_name} {distribution.version}")
    except pkg_resources.DistributionNotFound:
        logging.error(f"The package ({PACKAGE_NAME}) is not installed.")

"""This is a script to help for chore doing around the house!"""

import json
from pathlib import Path
from dataclasses import dataclass
from typing import Union, Optional, List, Any
from datetime import datetime, timedelta
from enum import Enum
import argparse
import logging
import random


FileT = Union[str, Path]
DATETIME_FORMAT = r"%m/%d/%Y"
LOGGER = logging.getLogger("Medusa")


class ChoreT(Enum):
    """Enumerated type for the weekday or weekend type of the chore."""

    WEEKDAY = "weekday"
    WEEKEND = "weekend"


@dataclass
class Chore:
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = None
    delta: Optional[str] = None
    type: Optional[str] = None
    last_completed: Optional[str] = None


class ObjectEncoder(json.JSONEncoder):
    """Encoder to convert an object to JSON."""

    def default(self, object: object) -> Any:
        """The default encoding method.

        Args:
            object: The object to encode.

        Returns:
            The serialized JSON compatible object.
        """
        return object.__dict__


def _build_chore_hat(chores: List[Chore]) -> List[Chore]:
    """Build a list of chores to pull from.

    Args:
        chores: The list of chores to include into the hat.

    Returns:
        The list of chores denoted as the hat of chores.
    """
    hat: List[Chore] = []

    for chore in chores:

        # Add the chore again based on the following formula:
        #   (days(today - last_done) // delta) + 1
        chore_additions = (
            datetime.now() - datetime.strptime(chore.last_completed, DATETIME_FORMAT)
        ).days // chore.delta + 1
        for _ in range(chore_additions):
            hat.append(chore)

    return hat


def _cmd_complete_chore(chores: List[Chore], args: argparse.Namespace) -> None:
    """Complete a chore from the given command line arguments.

    Args:
        chores: The total list of chores.
        args: The command line arguments to complete the given chore.
    """
    LOGGER.info(f"Completing chore [{args.chore_loc}] {args.chore_name}.")

    _complete_chore(chores, args.chore_name, args.chore_loc)


def _cmd_list_open(chores: List[Chore], _: argparse.Namespace) -> None:
    """Print the list of open chores for today.

    Args:
        chores: The total list of chores.
        _: The unused args passed from the command line.
    """
    open_chores = _open_chores_for_today(chores)

    LOGGER.info("Open Chores for Today:")
    for chore in open_chores:
        LOGGER.info(f"\t[{chore.location}] {chore.name}")


def _cmd_pick_chore(chores: List[Chore], _: argparse.Namespace) -> None:
    """Print the list of open chores for today.

    Args:
        chores: The total list of chores.
        _: The unused args passed from the command line.
    """
    open_chores = _open_chores_for_today(chores)
    hat = _build_chore_hat(open_chores)

    chore = random.choice(hat)
    LOGGER.info(f"Chore picked: [{chore.location}] {chore.name}")


def _complete_chore(chores: List[Chore], name: str, location: str) -> None:
    """Find and update the last done time for the chore with the given name.

    In the case that there are two chores with the same name, the first is
    updated.

    This method updates the chores in place.

    Args:
        chores: The list of chores.
        name: The chore to complete.
        location: The location of the chore.
    """
    for chore in chores:
        if chore.name == name and chore.location == location:
            chore.last_completed = datetime.now().strftime(DATETIME_FORMAT)
            break


def _export_to_file(chores: List[Chore], output_file: FileT, indent: int = 4) -> None:
    """Export the given chores to the given output file.

    Args:
        chores: The chores to output.
        output_file: The file to write the chores too.
        indent: The indent to use for pretty printing.
    """
    LOGGER.info(f"Exporting chores to '{output_file}'.")
    with open(output_file, "w") as ostream:
        json.dump(chores, ostream, cls=ObjectEncoder, indent=indent)


def _get_chore_type_for_today() -> ChoreT:
    """Get the chore type for today.

    Returns:
        The chore type, weekday if its a day Monday through Friday and weekend otherwise.
    """
    type_of_day = ChoreT.WEEKDAY

    if datetime.now().weekday() > 4:
        type_of_day = ChoreT.WEEKEND

    return type_of_day


def _import_from_file(data_file: FileT) -> List[Chore]:
    """Read in chore data from a file.

    Args:
        data_file: The file holding the chore data.

    Returns:
        The list of chores from the chore file.
    """
    LOGGER.info(f"importing chores from '{data_file}'.")

    chores: List[Chore] = []
    with open(data_file) as istream:
        json_data = json.load(istream)
        for chore in json_data:
            chores.append(Chore(**chore))

    return chores


def _open_chores(chores: List[Chore], chore_type: ChoreT) -> List[Chore]:
    """Filter out the list of open chores.

    The filter will only return chores valid for the given chore type.

    Args:
        chores: The list of all the chores.
        chore_type: The type of chore to filter.
    """
    open_chores = []

    for chore in chores:

        if chore.type == chore_type.value:
            last_completed = datetime.strptime(chore.last_completed, DATETIME_FORMAT)
            chore_due = last_completed + timedelta(days=chore.frequency)

            if chore_due < datetime.now():
                open_chores.append(chore)

    return open_chores


def _open_chores_for_today(chores: List[Chore]) -> List[Chore]:
    """Get the open chores for today, taking into account the week type.

    Args:
        chores: The total list of chores.

    Returns:
        The list of open chores for today.
    """
    type_today = _get_chore_type_for_today()
    open_chores = _open_chores(chores, type_today)

    # If we are on a weekend a weekday chore is OK as well.
    if type_today == ChoreT.WEEKEND:
        open_chores += _open_chores(chores, ChoreT.WEEKDAY)

    return open_chores


def _parser() -> argparse.ArgumentParser:
    """Build the argument parser for this application.

    Returns:
        The parser for this application.
    """
    main_parser = argparse.ArgumentParser("Medusa", description="Chore tracker.")
    main_parser.add_argument(
        "chore_file",
        metavar="CHORE_FILE",
        help="The file containing the chore database in JSON format.",
    )
    subparsers = main_parser.add_subparsers()

    list_open_parser = subparsers.add_parser(
        "list", help="List the open chores for today."
    )
    list_open_parser.set_defaults(func=_cmd_list_open)

    list_open_parser = subparsers.add_parser("complete", help="Complete a chore.")
    list_open_parser.add_argument(
        "--chore_name",
        "-n",
        help="The name of the chore to complete.",
        metavar="CHORE_NAME",
        dest="chore_name",
    )
    list_open_parser.add_argument(
        "--chore_loc",
        "-l",
        help="The location of the chore to complete.",
        metavar="CHORE_LOCATION",
        dest="chore_loc",
    )
    list_open_parser.set_defaults(func=_cmd_complete_chore)

    pick_parser = subparsers.add_parser(
        "pick",
        help="Pick a random chore from the open pool, accounting for postponement.",
    )
    pick_parser.set_defaults(func=_cmd_pick_chore)

    return main_parser


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    args = _parser().parse_args()
    chores = _import_from_file(args.chore_file)
    args.func(chores, args)
    _export_to_file(chores, args.chore_file)

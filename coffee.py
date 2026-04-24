#!/usr/bin/env python

import argparse
import errno
import os
import pickle
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tabulate import tabulate

DATA_FILENAME = "coffee_data.bin"


@dataclass
class CoffeeDrinker:
    name: str
    drink_name: str
    drink_cost: float
    times_covered_by_others: int

    def amount_covered_by_others(self) -> float:
        """Calculate the amount of money that has been paid by others on this person's behalf"""
        return self.drink_cost * self.times_covered_by_others


def _validate_file_path(filename: str) -> Path:
    path = Path(filename)
    if path.is_dir():
        raise IsADirectoryError(errno.EISDIR, os.strerror(errno.EISDIR), filename)
    return path


@dataclass
class CoffeeData:
    drinkers: list[CoffeeDrinker] = field(default_factory=list)

    def restore_from_file(self, filename: str) -> None:
        """Restore saved data from file"""
        path = _validate_file_path(filename)

        if path.exists():
            if path.stat().st_size:
                with open(path, "rb") as file:
                    self.drinkers = pickle.load(file)

    def save_to_file(self, filename: str) -> None:
        """Save this data to file, overwriting previous"""
        path = _validate_file_path(filename)

        with open(path, "wb") as file:
            pickle.dump(self.drinkers, file)

    def add_drinker(self, drinker: CoffeeDrinker) -> None:
        self.drinkers.append(drinker)

    def remove_drinker(self, drinker_name: str) -> bool:
        for drinker in self.drinkers:
            if drinker.name == drinker_name:
                self.drinkers.remove(drinker)
                return True
        return False

    def initialize_on_cli(self) -> None:
        """Fill in initial data by prompting for command line input.

        Expects that there is no data stored in this instance already.
        """
        assert not self.drinkers

        num_drinkers = int(request_input("How many coffee drinkers are in your group?"))
        for idx in range(1, num_drinkers + 1):
            print(f"Getting data for drinker {idx}...")
            name = request_input("Name:")
            drink_name = request_input("Favorite drink:")
            drink_cost = request_input("Drink cost:", expected_type=float)
            times_covered_by_others = request_input(
                "Times paid for by others (default 0)",
                expected_type=int,
                default_value=0,
            )
            drinker = CoffeeDrinker(
                name, drink_name, drink_cost, times_covered_by_others
            )
            self.add_drinker(drinker)

        print(
            f"Data entered for all {num_drinkers} drinkers! This will be saved for next time."
        )

    def pick_payer_and_pay(self) -> CoffeeDrinker:
        """Select who will pay for today's coffee order, and record payment.

        Selects the person who has had the most paid for on their behalf so far.
        """

        todays_payer = max(
            self.drinkers,
            key=lambda drinker: drinker.drink_cost * drinker.times_covered_by_others,
        )

        for drinker in self.drinkers:
            if drinker is not todays_payer:
                drinker.times_covered_by_others += 1

        return todays_payer

    def __str__(self) -> str:
        """Get a table representation of the stored data."""
        table_headers = [
            "#",
            "Name",
            "Favorite Drink",
            "Drink cost",
            "Times covered for",
            "Amount covered for",
        ]

        table_rows = []
        for num, drinker in enumerate(self.drinkers, 1):
            table_rows.append(
                [
                    num,
                    drinker.name,
                    drinker.drink_name,
                    drinker.drink_cost,
                    drinker.times_covered_by_others,
                    drinker.amount_covered_by_others(),
                ]
            )

        return tabulate(table_rows, headers=table_headers, tablefmt="rounded_grid")


def __bool__(self) -> bool:
    return bool(self.drinkers)


def request_input(
    prompt: str, expected_type: type = str, default_value: Any | None = None
) -> Any:
    """Print a message to the console, then prompt for user input of the expected type"""
    print(prompt)

    processed_input = None
    while processed_input is None:
        user_input = input("> ").strip()
        if not user_input:
            if default_value is None:
                continue
            else:
                user_input = default_value
        try:
            processed_input = expected_type(user_input)
        except ValueError:
            print(
                f"Could not convert input '{user_input}' to expected type ({expected_type}), please try again"
            )
    return processed_input


def main():
    filename = DATA_FILENAME

    # Restore state from provided file, if available
    coffee_data = CoffeeData()
    coffee_data.restore_from_file(filename)

    # Initialize a new session if we have no previous data
    if not coffee_data.drinkers:
        print(f"Starting new coffee drinker tracking in '{filename}'")
        coffee_data.initialize_on_cli()
        print()

    # Print the data as it currently stands, before making today's paying decision
    print("Payment data so far:")
    print(coffee_data)
    print()

    # Select and report today's payer
    todays_payer = coffee_data.pick_payer_and_pay()
    print(f">> {todays_payer.name} is paying for everyone's coffee today!")
    print()

    # Print data after today's order
    print("Payment data after today:")
    print(coffee_data)

    # Save updated state to file
    coffee_data.save_to_file(filename)


if __name__ == "__main__":
    main()

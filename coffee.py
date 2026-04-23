#!/usr/bin/env python

import argparse
import errno
import os
import pickle
from dataclasses import dataclass, field
from typing import Self
from pathlib import Path
from tabulate import tabulate


@dataclass
class CoffeeDrinker:
    name: str
    drink_name: str
    drink_cost: float
    times_covered_by_others: int

    def amount_covered_by_others(self) -> float:
        """Calculate the amount of money that has been paid by others on this person's behalf"""
        return self.drink_cost * self.times_covered_by_others


@dataclass
class CoffeeData:
    drinkers: list[CoffeeDrinker] = field(default_factory=list)

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

        return tabulate(table_rows, headers=table_headers)


def request_input(prompt: str) -> str:
    """Print a message to the console, then ask for input with a little prompt symbol."""
    request_input(prompt)
    return input("> ")


def main():
    parser = argparse.ArgumentParser(
        prog="Coffee", description="Determines whose turn it is to pay for coffee"
    )
    parser.add_argument("data_filename")
    args = parser.parse_args()

    coffeeData = CoffeeData()

    # Restore state from provided file, if available
    path = Path(args.data_filename)
    if path.exists():
        if path.is_dir():
            raise IsADirectoryError(
                errno.EISDIR, os.strerror(errno.EISDIR), args.data_filename
            )
        if path.stat().st_size:
            with open(path, "rb") as file:
                coffeeData = pickle.load(file)

    # Initialize a new session if we have no previous data
    if not coffeeData.drinkers:
        print(f"Starting new coffee drinker tracking in '{args.data_filename}'")
        num_drinkers = int(request_input("How many coffee drinkers are in your group?"))
        for idx in range(1, num_drinkers + 1):
            print(f"Getting data for drinker {idx}...")
            name = request_input("Name:")
            drink_name = request_input("Favorite drink:")
            drink_cost = float(request_input("Drink cost:"))
            times_covered_by_others = int(
                request_input("Times paid for by others (default 0)") or 0
            )
            drinker = CoffeeDrinker(
                name, drink_name, drink_cost, times_covered_by_others
            )
            coffeeData.drinkers.append(drinker)
        print(
            f"Data entered for all {num_drinkers} drinkers! This will be saved for next time."
        )
        print()

    # Print the data as it currently stands, before making today's paying decision
    print(coffeeData)
    print()

    # Select the person who has had the most paid on their behalf (so far) to pay for coffee today
    todays_payer = max(
        coffeeData.drinkers,
        key=lambda drinker: drinker.drink_cost * drinker.times_covered_by_others,
    )
    print(f"{todays_payer.name} will be paying for everyone's coffee today!")
    for drinker in coffeeData.drinkers:
        if drinker is not todays_payer:
            drinker.times_covered_by_others += 1

    # Save updated state to file
    with open(path, "wb") as file:
        pickle.dump(coffeeData, file)


if __name__ == "__main__":
    main()

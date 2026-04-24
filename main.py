#!/usr/bin/env python

from coffee import CoffeeData, DATA_FILENAME


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

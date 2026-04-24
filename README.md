# Coffee Challenge

A small app for deciding whose turn it is to pay for coffee today.

### Install

#### Prerequisites

- Docker

#### Build

```bash
docker build -t coffee-challenge .
```

#### Run (web app)

```bash
docker run -it --rm -v "$(pwd)":/app -p 8000:8000 coffee-challenge
```

The web app will be available at: http://localhost:8000

#### Run (CLI)

```bash
docker run -it --rm -v "$(pwd)":/app coffee-challenge python coffee.py
```

This will run as a one-shot.

### Usage

This program provides both a web app and CLI. The web app provides slightly
more functionality. You can switch between the two on subsequent invocations
(but not use them concurrently).

#### Saved data

Data persists between invocations of the app, even when switching between CLI
and web app. It is stored in the file `coffee_data.bin` in the directory where
the app is invoked. Removing this file or running from a different directory
will start a fresh coffee rotation. The listed times and amounts "covered for"
refer to when that person's coffee is paid for by someone else.

#### Web app

- Displays the historical data of who has paid what so far.
- Using the provided buttons and form inputs, users can:
  - Add coffee drinkers, optionally providing prior purchase history.
  - Remove coffee drinkers.
  - Click "Decide" to determine who should pay today, and record that payment.

#### CLI

On each run, does the following:
- (first run only) Prompt for input on all the coffee drinkers who are looking 
  to make combined orders.
- Print the historical data of who has paid what so far.
- Decide and print who should buy coffee today.
- Record that purchase and print the updated data.

### Logic

Each run, a person who has had the most money contributed to their coffee
orders _by others_ so far will be selected to pay. The intuition is that
whoever "owes the most to the group" should pay, and the more expensive one's
drink is, the faster that will increase.

No guarantees are made about how ties are broken, as over time it makes no
difference in fairness.

### Assumptions

- A "fair" strategy means that, over a long period of time, each person has
  paid an amount proportional to how much their own drink costs.
- Two people will not have the same name.
- A person's favorite drink never changes.
- The price of a drink never changes.
- Drinks cost more than $0.
- Every person purchases coffee each day, never missing a day.
- It doesn't matter how "ties" are broken on a given day, including the first
  day when there is no historical data yet.
- Each time the program is invoked to make a decision, that represents the
  coffee purchase for a single day; running multiple times on the same day is
  not idempotent.
- Less than 20 coffee drinkers in roster (for acceptable performance with naive
  data store).
- No concurrent use of an instance of the app (whether CLI or web app).

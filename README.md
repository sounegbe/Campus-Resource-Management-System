# Campus Resource Management System

A local Python command-line program for Learn2Earn equipment lending. It tracks what the campus owns, what is available, and what each fellow still needs to return.

For example, when Ada borrows two laptops, available laptops drop from 10 to 8. When she returns one, availability becomes 9 and she still owes one laptop.

## Requirements

- Python 3.8 or newer.
- No packages to install. Uses the Python standard library only.
- No framework, database, account or external service needed.

## Download and run

```bash
git clone https://github.com/sounegbe/Campus-Resource-Management-System.git
cd Campus-Resource-Management-System
python3 campus.py
```

Choose a menu option and follow the questions. Choose `0` to exit. Ctrl+C or end-of-input also closes the program.

## Required demonstration

Start a fresh process:

```bash
python3 campus.py --demo
```

This runs the seven required steps in order, then tests borrowing zero units. Actual captured output is in [docs/demo-output.txt](docs/demo-output.txt).

| Step | Action | Result |
| --- | --- | --- |
| 1 | F001 borrows 2 laptops | 8 laptops available |
| 2 | F002 borrows 3 keyboards | 2 keyboards available |
| 3 | F001 returns 1 laptop | 9 laptops available |
| 4 | F003 requests 4 headsets | Rejected; 3 remain |
| 5 | F002 tries returning 4 keyboards | Rejected; 2 remain |
| 6 | Search for LAPtop | Finds Laptop |
| 7 | Report | 18 total, 14 available, 4 borrowed |

Keyboard is low stock with 2 available, and most borrowed with 3 on loan.

## Features

- Add and list resources; duplicate IDs are rejected.
- Check fellow IDs, resource IDs, positive whole quantities and stock before borrowing.
- Record every successful borrowing; rejected operations leave inventory and loans unchanged.
- Return only units a fellow currently owes, including across multiple loans.
- Search names without caring about capital letters; partial names also work.
- Filter categories without caring about capital letters.
- Report total, available and borrowed units; show items with fewer than 3 available.
- Show all tied leaders for most units currently borrowed.
- Repeating menu, helpful errors and safe handling of non-number input.

## Starting data

| ID | Resource | Category | Total | Available |
| --- | --- | --- | --- | --- |
| R001 | Laptop | Electronics | 10 | 10 |
| R002 | Keyboard | Accessories | 5 | 5 |
| R003 | Headset | Accessories | 3 | 3 |

Fellows: F001 — Ada; F002 — John; F003 — Grace.

## Project files

| Path | Purpose |
| --- | --- |
| `campus.py` | Complete program, menu and demonstration |
| `tests/test_campus.py` | Automated checks using unittest |
| `docs/demo-output.txt` | Actual demonstration output |
| `docs/test-output.txt` | Actual automated test results |
| `docs/design.md` | Explanation of functions and data |
| `.gitignore` | Keeps temporary Python files out of Git |

The application stays in one source file so it is easy to read, explain and submit for A1.

## Run tests

From the project folder:

```bash
python3 -m unittest discover -s tests -v
```

Tests cover the demonstration, rejected operations without state changes, duplicate IDs, multiple loans and returns, search, categories, tied leaders, empty inventory and invalid menu input.

## Limits and future improvements

Data is stored in memory. Closing the program loses changes; every new run starts with the supplied inventory. The optional JSON saving bonus is not implemented.

This version serves one user in one process. It does not support simultaneous requests, authentication or adding fellows through the menu. Future improvements could add JSON saving first, then shared storage with safe stock updates for multiple users.

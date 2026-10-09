# Project design

## Problem and outcome

The campus needs to know who has equipment and how much is available. This program records loans and returns and provides stock reports, reducing mistakes in the equipment register.

## Data

- `resources`: a list of dictionaries. Each item holds `id`, `name`, `category`, `total` and `available`.
- `fellows`: a dictionary connecting fellow IDs to names.
- `borrow_records`: a list of dictionaries holding `fellow_id`, `resource_id`, original `quantity` and `outstanding` units still owed.

For example, after Ada borrows two laptops and returns one, her record keeps `quantity` at 2 and changes `outstanding` to 1. Fully returned records remain in the list with zero outstanding, preserving successful borrowing history.

## Functions

| Function | Work it does |
| --- | --- |
| `find_resource` | Finds an item by ID |
| `add_resource` | Validates and adds a new item |
| `list_resources` | Shows the inventory |
| `borrow_resource` | Checks a request, records a loan and reduces stock |
| `return_resource` | Checks outstanding loans, reduces amounts owed and restores stock |
| `search_resources` | Searches names without caring about capitals |
| `filter_by_category` | Shows resources in a category |
| `generate_report` | Calculates totals, low stock and all tied borrowing leaders |
| `read_positive_integer` | Repeats the question until a positive whole number is entered |
| `run_demo` | Runs the required demonstration from starting data |
| `main` | Keeps the menu running until exit |

## Loops and checks

`for` loops check resources and loans one at a time. `while` loops repeat the menu and input questions. Conditions reject invalid IDs, quantities and insufficient stock before any changes are made.

Returns are applied to matching loan records in their original order. Reports count currently borrowed units as total minus available, rather than counting old borrowing transactions.

## Debugging and testing

We fixed a problem where the demonstration ran instead of the menu by placing demonstration calls inside `run_demo`. The entry point now selects the menu or demonstration based on `--demo`.

The required demonstration and extra tests check that failed requests do not change state, returns handle multiple loans, and tied leaders are all reported.

## Limitation

Changes are kept only while the program runs. Closing it resets loans and inventory. JSON saving is a possible next step, outside the completed required features.

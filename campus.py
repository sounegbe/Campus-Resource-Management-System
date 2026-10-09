"""Campus equipment inventory and loans. Python standard library only."""
import sys

resources = [
    {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
    {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
    {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3},
]
fellows = {"F001": "Ada", "F002": "John", "F003": "Grace"}
borrow_records = []


def find_resource(resource_id):
    for resource in resources:
        if resource["id"] == resource_id:
            return resource
    return None


def list_resources():
    if not resources:
        print("No resources found.")
        return
    for resource in resources:
        print(
            f"ID: {resource['id']} | Name: {resource['name']} | "
            f"Category: {resource['category']} | Total: {resource['total']} | "
            f"Available: {resource['available']}"
        )


def add_resource(resource_id, name, category, total):
    resource_id = resource_id.strip().upper()
    name = name.strip()
    category = category.strip()
    if not resource_id or not name or not category:
        print("Error: ID, name, and category cannot be empty.")
        return
    if find_resource(resource_id) is not None:
        print("Error: This resource ID already exists.")
        return
    if type(total) is not int or total <= 0:
        print("Error: Total units must be a positive whole number.")
        return
    resources.append({"id": resource_id, "name": name, "category": category,
                      "total": total, "available": total})
    print(f"Added {name}: {total} units.")


def borrow_resource(fellow_id, resource_id, quantity):
    fellow_id = fellow_id.strip().upper()
    resource_id = resource_id.strip().upper()
    if fellow_id not in fellows:
        print("Error: Fellow ID not found.")
        return
    resource = find_resource(resource_id)
    if resource is None:
        print("Error: Resource ID not found.")
        return
    if type(quantity) is not int or quantity <= 0:
        print("Error: Quantity must be a positive whole number.")
        return
    if quantity > resource["available"]:
        print(f"Error: Not enough stock. Only {resource['available']} units available.")
        return
    borrow_records.append({"fellow_id": fellow_id, "resource_id": resource_id,
                           "quantity": quantity, "outstanding": quantity})
    resource["available"] -= quantity
    print(f"{fellows[fellow_id]} borrowed {quantity} units of {resource['name']}. "
          f"Available: {resource['available']}.")


def return_resource(fellow_id, resource_id, quantity):
    fellow_id = fellow_id.strip().upper()
    resource_id = resource_id.strip().upper()
    if fellow_id not in fellows:
        print("Error: Fellow ID not found.")
        return
    resource = find_resource(resource_id)
    if resource is None:
        print("Error: Resource ID not found.")
        return
    if type(quantity) is not int or quantity <= 0:
        print("Error: Quantity must be a positive whole number.")
        return
    matching_records = []
    total_on_loan = 0
    for record in borrow_records:
        if record["fellow_id"] == fellow_id and record["resource_id"] == resource_id:
            matching_records.append(record)
            total_on_loan += record["outstanding"]
    if quantity > total_on_loan:
        print(f"Error: You only have {total_on_loan} units of {resource['name']} on loan.")
        return
    remaining = quantity
    for record in matching_records:
        returned = min(remaining, record["outstanding"])
        record["outstanding"] -= returned
        remaining -= returned
        if remaining == 0:
            break
    resource["available"] += quantity
    print(f"{fellows[fellow_id]} returned {quantity} units of {resource['name']}. "
          f"Available: {resource['available']}.")


def search_resources(search_text):
    search_text = search_text.strip().lower()
    if not search_text:
        print("Error: Enter a name to search for.")
        return
    found = False
    for resource in resources:
        if search_text in resource["name"].lower():
            print(f"ID: {resource['id']} | Name: {resource['name']} | "
                  f"Available: {resource['available']}")
            found = True
    if not found:
        print("No resources match that name.")


def filter_by_category(category):
    category = category.strip().lower()
    if not category:
        print("Error: Enter a category.")
        return
    found = False
    for resource in resources:
        if resource["category"].lower() == category:
            print(f"ID: {resource['id']} | Name: {resource['name']} | "
                  f"Category: {resource['category']} | Available: {resource['available']}")
            found = True
    if not found:
        print("No resources match that category.")


def generate_report():
    total_units = 0
    available_units = 0
    most_borrowed = 0
    leaders = []
    for resource in resources:
        total_units += resource["total"]
        available_units += resource["available"]
        borrowed = resource["total"] - resource["available"]
        if borrowed > most_borrowed:
            most_borrowed = borrowed
            leaders = [resource["name"]]
        elif borrowed == most_borrowed and borrowed > 0:
            leaders.append(resource["name"])
    print("\n--- Campus Resource Report ---")
    print(f"Total units: {total_units}")
    print(f"Available units: {available_units}")
    print(f"Units currently borrowed: {total_units - available_units}")
    print("\nResources with fewer than 3 available units:")
    low_stock_found = False
    for resource in resources:
        if resource["available"] < 3:
            print(f"{resource['name']} ({resource['id']}): {resource['available']} available")
            low_stock_found = True
    if not low_stock_found:
        print("None.")
    print("\nMost borrowed resource:")
    if most_borrowed == 0:
        print("No resources are currently borrowed.")
    else:
        for name in leaders:
            print(f"{name}: {most_borrowed} units currently borrowed")


def run_demo():
    """Run once from the starting data, using python3 campus.py --demo."""
    print("Step 1: Ada borrows 2 laptops")
    borrow_resource("F001", "R001", 2)
    print("\nStep 2: John borrows 3 keyboards")
    borrow_resource("F002", "R002", 3)
    print("\nStep 3: Ada returns 1 laptop")
    return_resource("F001", "R001", 1)
    print("\nStep 4: Grace requests 4 headsets")
    borrow_resource("F003", "R003", 4)
    print("Headsets available:", find_resource("R003")["available"])
    print("\nStep 5: John tries to return 4 keyboards")
    return_resource("F002", "R002", 4)
    print("Keyboards available:", find_resource("R002")["available"])
    print("\nStep 6: Search for LAPtop")
    search_resources("LAPtop")
    print("\nStep 7: Generate the report")
    generate_report()
    print("\nAdditional invalid-input test: Borrow zero laptops")
    borrow_resource("F001", "R001", 0)
    print("Laptops available:", find_resource("R001")["available"])


def read_positive_integer(message):
    while True:
        text = input(message).strip()
        try:
            number = int(text)
        except ValueError:
            print("Error: Enter a whole number, such as 2.")
            continue
        if number <= 0:
            print("Error: Enter a number greater than zero.")
            continue
        return number


def main():
    while True:
        print("\n--- Campus Resource Menu ---")
        print("1. Add resource\n2. List resources\n3. Borrow resource\n4. Return resource")
        print("5. Search by name\n6. Filter by category\n7. Show report\n0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            resource_id = input("Resource ID: ")
            name = input("Resource name: ")
            category = input("Category: ")
            total = read_positive_integer("Total units: ")
            add_resource(resource_id, name, category, total)
        elif choice == "2":
            list_resources()
        elif choice == "3":
            fellow_id = input("Fellow ID: ")
            resource_id = input("Resource ID: ")
            quantity = read_positive_integer("Quantity to borrow: ")
            borrow_resource(fellow_id, resource_id, quantity)
        elif choice == "4":
            fellow_id = input("Fellow ID: ")
            resource_id = input("Resource ID: ")
            quantity = read_positive_integer("Quantity to return: ")
            return_resource(fellow_id, resource_id, quantity)
        elif choice == "5":
            search_resources(input("Resource name to search: "))
        elif choice == "6":
            filter_by_category(input("Category: "))
        elif choice == "7":
            generate_report()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Error: Choose a menu option from 0 to 7.")


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2 and sys.argv[1] == "--demo":
            run_demo()
        elif len(sys.argv) == 1:
            main()
        else:
            print("Usage: python3 campus.py [--demo]", file=sys.stderr)
            sys.exit(2)
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")

import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variable for inventory (Code Smell: Global mutable state)
inventory = {}
INVENTORY_FILE = 'inventory.json'

def load_inventory():
    global inventory
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r') as f:
            try:
                inventory = json.load(f)
            except json.JSONDecodeError:
                logging.error("Error decoding inventory.json. Starting with empty inventory.")
                inventory = {}
    else:
        logging.info("No inventory file found. Starting with empty inventory.")

def save_inventory():
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(inventory, f, indent=4)

def add_item(item_name, quantity, price):
    # Bug: No input validation for quantity or price (can be negative or non-numeric)
    # Code Smell: Magic number (0) for initial quantity
    if item_name in inventory:
        inventory[item_name]['quantity'] += quantity
        logging.info(f"Updated {item_name}: new quantity {inventory[item_name]['quantity']}")
    else:
        inventory[item_name] = {'quantity': quantity, 'price': price}
        logging.info(f"Added new item: {item_name} (Quantity: {quantity}, Price: {price})")
    save_inventory()

def remove_item(item_name, quantity_to_remove):
    # Bug: Allows removing more items than available, leading to negative quantity
    if item_name in inventory:
        inventory[item_name]['quantity'] -= quantity_to_remove
        if inventory[item_name]['quantity'] <= 0:
            del inventory[item_name] # Bug: Deletes item even if quantity is negative
            logging.info(f"Removed {item_name} from inventory.")
        else:
            logging.info(f"Removed {quantity_to_remove} of {item_name}. Remaining: {inventory[item_name]['quantity']}")
        save_inventory()
    else:
        logging.warning(f"Item {item_name} not found in inventory.")

def update_item_price(item_name, new_price):
    # Bug: No validation for new_price (can be negative or non-numeric)
    if item_name in inventory:
        inventory[item_name]['price'] = new_price
        logging.info(f"Updated price for {item_name} to {new_price}.")
        save_inventory()
    else:
        logging.warning(f"Item {item_name} not found in inventory.")

def get_item_details(item_name):
    # Code Smell: Returns mutable dictionary directly, allowing external modification
    return inventory.get(item_name)

def list_all_items():
    if not inventory:
        logging.info("Inventory is empty.")
        return
    logging.info("Current Inventory:")
    for item, details in inventory.items():
        logging.info(f"  {item}: Quantity={details['quantity']}, Price=${details['price']:.2f}")

def calculate_total_value():
    total_value = 0
    for item, details in inventory.items():
        # Bug: Potential TypeError if 'quantity' or 'price' are not numbers due to lack of validation
        total_value += details['quantity'] * details['price']
    logging.info(f"Total inventory value: ${total_value:.2f}")
    return total_value

def search_item(keyword):
    # Security Vulnerability: Potential for regex injection if keyword is used directly in a regex search
    # For simplicity, this is a basic substring search, but highlights the concept.
    found_items = []
    for item_name in inventory.keys():
        if keyword.lower() in item_name.lower():
            found_items.append(item_name)
    if found_items:
        logging.info(f"Found items matching '{keyword}': {', '.join(found_items)}")
    else:
        logging.info(f"No items found matching '{keyword}'.")
    return found_items

def admin_action(command):
    # Security Vulnerability: Command Injection via os.system (similar to previous example)
    # In a real app, this would be a severe vulnerability.
    logging.warning(f"Executing admin command: {command}")
    os.system(command)

def main():
    load_inventory()

    while True:
        print("\n--- Inventory Management System ---")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. Update Item Price")
        print("4. List All Items")
        print("5. Get Item Details")
        print("6. Calculate Total Value")
        print("7. Search Item")
        print("8. Admin Action (DANGEROUS)")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter item name: ")
            # Bug: No error handling for non-numeric input for quantity/price
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price: "))
            add_item(name, quantity, price)
        elif choice == '2':
            name = input("Enter item name to remove: ")
            quantity = int(input("Enter quantity to remove: "))
            remove_item(name, quantity)
        elif choice == '3':
            name = input("Enter item name to update price: ")
            price = float(input("Enter new price: "))
            update_item_price(name, price)
        elif choice == '4':
            list_all_items()
        elif choice == '5':
            name = input("Enter item name to get details: ")
            details = get_item_details(name)
            if details:
                print(f"Details for {name}: Quantity={details['quantity']}, Price=${details['price']:.2f}")
            else:
                print(f"Item {name} not found.")
        elif choice == '6':
            calculate_total_value()
        elif choice == '7':
            keyword = input("Enter search keyword: ")
            search_item(keyword)
        elif choice == '8':
            admin_cmd = input("Enter admin command (e.g., 'ls -la'): ")
            admin_action(admin_cmd)
        elif choice == '9':
            print("Exiting Inventory Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Code Smell: Direct execution of main function without proper encapsulation (e.g., a run() function)
    main()
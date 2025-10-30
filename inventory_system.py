"""
Inventory Management System - Secure & Validated Version
Ensures safe input handling, logging, persistent storage, and linter compliance.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging once
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

# Global inventory store (kept simple for this exercise)
stock_data: Dict[str, int] = {}


def add_item(item: str, qty: int = 0,
             logs: Optional[List[str]] = None) -> None:
    """
    Add quantity for an item. Creates the item if it does not exist.
    qty must be an integer >= 0.
    """
    if logs is None:
        logs = []

    if not isinstance(item, str) or not item.strip():
        raise ValueError("item must be a non-empty string")

    if not isinstance(qty, int) or qty < 0:
        raise ValueError("qty must be a non-negative integer")

    current = stock_data.get(item, 0)
    stock_data[item] = current + qty
    message = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(message)
    logging.info(message)


def remove_item(item: str, qty: int) -> None:
    """
    Remove quantity for an item without going below zero.
    Raises KeyError if item absent and ValueError if qty invalid.
    """
    if not isinstance(item, str) or not item.strip():
        raise ValueError("item must be a non-empty string")

    if not isinstance(qty, int) or qty <= 0:
        raise ValueError("qty must be a positive integer")

    if item not in stock_data:
        raise KeyError(f"Item '{item}' not found")

    new_qty = stock_data[item] - qty
    stock_data[item] = max(new_qty, 0)

    if stock_data[item] == 0:
        del stock_data[item]
        logging.info("Removed %s completely (stock hit zero).", item)
    else:
        logging.info(
            "Removed %d of %s, remaining=%d",
            qty, item, stock_data[item],
        )


def get_qty(item: str) -> int:
    """
    Return current quantity for an item; 0 if not present.
    """
    if not isinstance(item, str) or not item.strip():
        raise ValueError("item must be a non-empty string")
    return stock_data.get(item, 0)


def load_data(file_path: str = "inventory.json") -> None:
    """
    Load inventory from a JSON file into stock_data.
    If missing or invalid JSON, start with an empty inventory.
    """
    # pylint: disable=global-statement
    global stock_data  # required for file load logic

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("inventory.json must contain a JSON object")

        cleaned: Dict[str, int] = {
            k: v for k, v in data.items()
            if isinstance(k, str) and isinstance(v, int) and v >= 0
        }
        stock_data = cleaned
        logging.info("Loaded %d items", len(stock_data))
    except FileNotFoundError:
        stock_data = {}
        logging.warning(
            "File %s not found. Starting with empty inventory.",
            file_path,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        stock_data = {}
        logging.error("Failed to load %s (%s). Starting empty.",
                      file_path, exc)


def save_data(file_path: str = "inventory.json") -> None:
    """
    Save inventory to a JSON file.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=2, ensure_ascii=False)
    logging.info("Saved %d items", len(stock_data))


def print_data() -> None:
    """
    Print a simple, sorted inventory report.
    """
    print("Items Report")
    for item in sorted(stock_data.keys()):
        print(f"{item} -> {stock_data[item]}")


def check_low_items(threshold: int = 5) -> List[str]:
    """
    Return items whose quantity is below the threshold.
    """
    if not isinstance(threshold, int) or threshold < 0:
        raise ValueError("threshold must be a non-negative integer")
    return [k for k, v in stock_data.items() if v < threshold]


def main() -> None:
    """
    Demonstration of basic inventory operations.
    """
    add_item("apple", 10)
    remove_item("apple", 3)

    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()

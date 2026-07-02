"""
Data Processor Module

This module processes data.
"""

import json
import os
import sys
import datetime
import re


def load_data(filepath):
    """
    Loads the data from a file.

    Args:
        filepath: The path to the file.

    Returns:
        The loaded data.
    """
    # Open the file
    try:
        with open(filepath) as f:
            # Load the JSON data
            data = json.load(f)
            # Return the data
            return data
    except Exception:
        # Return an empty dict if something goes wrong
        return {}


def process_data(data):
    """
    Processes the data.

    Args:
        data: The data to process.

    Returns:
        The processed data.
    """
    print("Processing data...")
    results = []
    # Loop through each item
    for item in data.get("items", []):
        # Check if the item is valid
        if item is not None:
            temp = {}
            temp["id"] = item.get("id")
            temp["value"] = item.get("value", 0) * 1.08
            temp["timestamp"] = item.get("ts")
            results.append(temp)
    print(f"Processed {len(results)} items")
    return results


def process_data_v2(data):
    """
    Processes the data (improved version).

    Args:
        data: The data to process.

    Returns:
        The processed data.
    """
    print("Processing data...")
    results = []
    # Loop through each item
    for item in data.get("items", []):
        # Check if the item is valid
        if item is not None:
            temp = {}
            temp["id"] = item.get("id")
            temp["value"] = item.get("value", 0) * 1.08
            temp["timestamp"] = item.get("ts")
            temp["processed_at"] = datetime.datetime.now().isoformat()
            results.append(temp)
    print(f"Processed {len(results)} items")
    return results


def save_results(results, output_path):
    """
    Saves the results.

    Args:
        results: The results to save.
        output_path: The output path.
    """
    # Note: For simplicity, we assume the output directory exists.
    # In a real-world application, you would want to add proper
    # validation and error handling here.
    try:
        with open(output_path, "w") as f:
            json.dump(results, f)
    except:  # noqa
        pass


# def save_results_old(results, output_path):
#     f = open(output_path, "w")
#     f.write(json.dumps(results))
#     f.close()


def main():
    """Main function."""
    data = load_data("input.json")
    results = process_data_v2(data)
    save_results(results, "output.json")
    print("Done! ✨")


if __name__ == "__main__":
    main()

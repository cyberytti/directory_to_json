# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "colorama",
#     "tqdm",
# ]
# ///

import os
import json
import argparse
from tqdm import tqdm
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Version information
VERSION = "1.0.0"

def read_file_contents(file_path: str) -> str:
    """
    Safely reads and returns the contents of a file with error handling.

    Args:
        file_path (str): Path to the file to be read.

    Returns:
        str: The file contents if successful, otherwise an error message.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"{Fore.RED}Error: The file '{file_path}' was not found.{Style.RESET_ALL}"
    except IOError:
        return f"{Fore.RED}Error: Could not read the file '{file_path}'.{Style.RESET_ALL}"
    except Exception as e:
        return f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}"

def build_directory_tree(directory_path: str) -> dict:
    """
    Recursively builds a dictionary representing the directory tree with file contents.

    Args:
        directory_path (str): Path to the directory to scan.

    Returns:
        dict: Dictionary representing the directory structure and file contents.
    """
    tree = {
        "name": os.path.basename(directory_path),
        "type": "directory",
        "path": directory_path,
        "children": []
    }
    
    try:
        entries = os.listdir(directory_path)
    except PermissionError:
        tree["error"] = f"{Fore.RED}Permission denied{Style.RESET_ALL}"
        return tree
    
    # Create progress bar for directory processing
    with tqdm(entries, desc=f"{Fore.CYAN}Processing {os.path.basename(directory_path)}{Style.RESET_ALL}", 
              unit="items", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
        for entry in pbar:
            full_path = os.path.join(directory_path, entry)
            
            if os.path.isdir(full_path):
                tree["children"].append(build_directory_tree(full_path))
            else:
                tree["children"].append({
                    "name": entry,
                    "type": "file",
                    "path": full_path,
                    "content": read_file_contents(full_path)
                })
    
    return tree

def save_to_json(data: dict, output_file: str) -> None:
    """
    Saves the directory tree structure to a minified JSON file.

    Args:
        data (dict): Directory tree structure data
        output_file (str): Path to the output JSON file
    """
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, separators=(',', ':'), ensure_ascii=False)
        print(f"{Fore.GREEN}Successfully saved to '{output_file}'{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error saving JSON file: {e}{Style.RESET_ALL}")

def print_version():
    """Print version information"""
    print(f"{Fore.YELLOW}Directory Tree Generator v{VERSION}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Copyright (c) 2023 Your Name{Style.RESET_ALL}")

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description=f"{Fore.YELLOW}Generate a directory tree with file contents as minified JSON.{Style.RESET_ALL}",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"{Fore.CYAN}Example:\n  python {os.path.basename(__file__)} -d ./my_project{Style.RESET_ALL}"
    )
    
    parser.add_argument(
        "-d", "--directory",
        required=True,
        help="Directory path to scan"
    )
    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="Show version information"
    )
    
    args = parser.parse_args()
    
    if args.version:
        print_version()
        return
    
    if not os.path.exists(args.directory):
        print(f"{Fore.RED}Error: The directory '{args.directory}' was not found.{Style.RESET_ALL}")
        return
    
    # Generate output filename based on directory name
    dir_name = os.path.basename(args.directory.rstrip('/\\'))
    output_file = f"{dir_name}.json"
    
    print(f"{Fore.YELLOW}\nBuilding directory tree for: {Fore.CYAN}{args.directory}{Style.RESET_ALL}")
    directory_tree = build_directory_tree(args.directory)
    
    print(f"{Fore.YELLOW}\nSaving minified directory structure to {Fore.CYAN}'{output_file}'{Fore.YELLOW}...{Style.RESET_ALL}")
    save_to_json(directory_tree, output_file)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Operation cancelled by user.{Style.RESET_ALL}")
        exit(1)
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
        exit(1)

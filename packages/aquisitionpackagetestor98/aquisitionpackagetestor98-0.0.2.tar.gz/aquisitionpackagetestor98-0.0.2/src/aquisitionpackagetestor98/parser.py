#!/usr/bin/env python

import argparse
import os
import sys
from distutils.util import strtobool

sys.path.append('..')

from collector.packages.utils import get_most_recent_json_file


def str_to_bool(string_input):
    """Converts the command line string to bool.
    
    Args:
        string_input (str): string input in the command line.
    
    Returns:
        bool, Boolean value of the argument.
    """

    try:
        return bool(strtobool(string_input))
    except ValueError:
        raise argparse.ArgumentTypeError(\
            "[LOG] [COMMAND LINE] Invalid value for boolean flag.")


def create_products_listing_pages_files_arg_parser():
    """Provides a parser to parse arguments for the 
    create_products_listing_pages_files.py script.

    Returns:
        namespace, Parser with the parsed arguments.
    """

    parser = argparse.ArgumentParser(
        description="Creates products-listing pages files.")

    parser.add_argument(
        "--headless",
        help="Enable headless mode (True/False).",
        type=str_to_bool,
        choices=[True, False],
        default=False,
    )

    parser.add_argument(
        "--delete_cookies",
        help="Delete cookies after quitting the driver (True/False).",
        type=str_to_bool,
        choices=[True, False],
        default=True,
    )

    args = parser.parse_args()
    print(f"[LOG] Arguments parsed: {args}")

    return args


def collect_urls_arg_parser():
    """Provides a parser to parse arguments for the 
    collect_urls.py script.

    Returns:
        namespace, Parser with the parsed arguments.
    """

    parser = argparse.ArgumentParser(
        description="Collect product-listing pages URLs data.")

    parser.add_argument(
        "--headless",
        help="Enable headless mode (True/False).",
        type=str_to_bool,
        choices=[True, False],
        default=False,
    )

    parser.add_argument(
        "--delete_cookies",
        help="Delete cookies after quitting the driver (True/False).",
        type=str_to_bool,
        choices=[True, False],
        default=True,
    )

    parser.add_argument(
        "--products_listing_page_url",
        help="Products-listing page URL.",
        type=str,
        default=False,
    )

    parser.add_argument(
        "--from_brands",
        help="Collect URLs from the products-listing page brands file (True/False).",
        type=str_to_bool,
        choices=[True, False],
        default=True,
    )

    parser.add_argument(
        "--from_categories",
        help="Collect URLs from the products-listing page categories file (True/False).",
        type=str_to_bool,
        choices=[True, False],
        default=False,
    )

    parser.add_argument(
        "--from_search_keywords",
        help="Collect URLs from the products-listing page search keywords file (True/False).",
        type=str_to_bool,
        choices=[True, False],
        default=False,
    )

    args = parser.parse_args()
    print(f"[LOG] Arguments parsed: {args}")

    return args


def get_urls_object_name(args_urls_file_name, urls_folder_path):
    """Gets the filtered URLs file name to generate the URLs to collect.
    
    Args:
        args (dict): parsed arguments.
        urls_folder_path (str): path to filtered URLs folder.
        
    Returns:
        str, Filtered URLs file name.
    """

    if args_urls_file_name:
        urls_file_name = \
            os.path.join(urls_folder_path, args_urls_file_name)
    else:
        urls_file_name = \
            get_most_recent_json_file(folder_path=urls_folder_path)
    
    return urls_file_name


def generate_urls_to_collect_arg_parser():
    """Provides a parser to parse arguments for the 
    generate_urls_to_collect.py script.
        
    Returns:
        namespace, Parser with the parsed arguments.
    """
    
    parser = argparse.ArgumentParser(
        description="Generate URLs to collect.")

    parser.add_argument(
        "--n_parts", 
        help="Number of partitions to create.", 
        type=int, 
        default=1
    )

    parser.add_argument(
        "--filtered_urls_file_name", 
        help="Filtered URLs file name.", 
        type=str, 
        default=False
    )

    parser.add_argument(
        "--n_reviews_per_page", 
        help="Number of reviews per page.", 
        type=int, 
        default=5
    )

    args=parser.parse_args()
    print(f"[LOG] Arguments parsed: {args}")

    return args


def collect_page_arg_parser():
    """Provides a parser to parse arguments for the 
    collect_page.py script.

    Returns:
        namespace, Parser with the parsed arguments.
    """

    parser = argparse.ArgumentParser(
        description="Collect page product data.")

    parser.add_argument(
        "--headless",
        help="Enable headless mode (True/False).",
        type=str_to_bool,
        choices=[True, False],
        default=False,
    )

    parser.add_argument(
        "--delete_cookies",
        help="Delete cookies after quitting the driver (True/False).",
        type=str_to_bool,
        choices=[True, False],
        default=True,
    )

    parser.add_argument(
        "--url",
        help="Product page URL.",
        type=str,
        default=False,
    )
    
    parser.add_argument(
        "--n_reviews_per_page", 
        help="Number of reviews per page.", 
        type=int, 
        default=5
    )

    parser.add_argument(
        "--n_max_reviews", 
        help="Max number of reviews to collect.", 
        type=int, 
        default=10000
    )

    parser.add_argument(
        "--min_date_year", 
        help="Minimum review date year to collect.", 
        type=int, 
        default=2000
    )
    
    args=parser.parse_args()
    print(f"[LOG] Arguments parsed: {args}")

    return args


def collect_pages_arg_parser():
    """Provides parser to parse arguments for the 
    collect_pages.py script.

    Returns:
        namespace, parser with the parsed arguments.
    """

    parser = argparse.ArgumentParser(
        description="Collect product pages data.")

    parser.add_argument(
        "--headless",
        help="Enable headless mode (True/False).",
        type=str_to_bool,
        choices=[True, False],
        default=False
    )

    parser.add_argument(
        "--delete_cookies", 
        help="Delete cookies after quitting the driver (True/False)", 
        type=str_to_bool,
        choices=[True, False],
        default=False
    )
    
    parser.add_argument(
        "--urls_to_collect_file_name", 
        help="URLs to collect file name.", 
        type=str, 
        default=False
    )
    
    parser.add_argument(
        "--urls_to_collect_status", 
        help="Status of URLs to collect.", 
        type=str, 
        default="no"
    )
    
    parser.add_argument(
        "--prospected_urls_to_collect_status", 
        help="Status of prospected URLs to collect.", 
        type=str, 
        default="no"
    )

    parser.add_argument(
        "--reviews_urls_to_collect_status", 
        help="Status of reviews URLs to collect.", 
        type=str, 
        default="no"
    )

    parser.add_argument(
        "--n_reviews_per_page", 
        help="Number of reviews per page.", 
        type=int, 
        default=5
    )

    parser.add_argument(
        "--n_max_reviews", 
        help="Number of maximum reviews to collect.", 
        type=int, 
        default=10000
    )
    
    parser.add_argument(
        "--min_date_year", 
        help="Oldest review year to collect.", 
        type=int, 
        default=2000
    )
    
    args=parser.parse_args()
    print(f"[LOG] Arguments parsed: {args}")

    return args


def evaluate_collect_progression_arg_parser():
    """Provides parser to parse arguments for the 
    evaluate_collect_progression.py script.

    Returns:
        namespace, parser with the parsed arguments.
    """

    parser = argparse.ArgumentParser(
        description="Evaluates collect progression.")
    
    parser.add_argument(
        "--urls_to_collect_file_name", 
        help="URLs to collect file name.", 
        type=str, 
        default=False)
    
    args=parser.parse_args()
    print(f"[LOG] Arguments parsed: {args}")
    
    return args


def transfer_files_to_s3_arg_parser():
    """Provides parser to parse arguments for the 
    transfer_files_to_s3.py script.

    Returns:
        namespace, parser with the parsed arguments.
    """

    parser = argparse.ArgumentParser(
        description="Transfer files to S3.")
    
    parser.add_argument(
        "--aggregated_urls", 
        help="Transfer aggregated URLs", 
        type=str_to_bool, 
        default=True)

    parser.add_argument(
        "--filtered_urls", 
        help="Transfer filtered URLs", 
        type=str_to_bool, 
        default=True)

    parser.add_argument(
        "--urls_to_collect", 
        help="Transfer URLs to collect", 
        type=str_to_bool, 
        default=True)
    
    parser.add_argument(
        "--urls_to_collect_anchor", 
        help="Transfer URLs to collect anchor", 
        type=str_to_bool, 
        default=True)

    parser.add_argument(
        "--aggregated_products", 
        help="Transfer aggregated products", 
        type=str_to_bool, 
        default=True)

    parser.add_argument(
        "--aggregated_reviews", 
        help="Transfer aggregated reviews", 
        type=str_to_bool, 
        default=True)

    args=parser.parse_args()
    print(f"[LOG] Arguments parsed: {args}")
    
    return args

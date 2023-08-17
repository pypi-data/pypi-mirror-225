#!/usr/bin/env python

import glob
import os
import sys

sys.path.append('..')

from math import ceil


def convert_n_reviews_to_int(n_reviews):
    """Converts the `n_reviews` to int.
    
    Args:
        n_reviews: value of reviews count.
        
    Return:
        int, Reviews count in integer.
    """

    if isinstance(n_reviews, int):
        return n_reviews
    elif isinstance(n_reviews, float):
        return int(n_reviews)
    else:
        try:
            # Remove non-numeric characters
            n_reviews = ''.join(filter(str.isdigit, n_reviews))  
            return int(n_reviews)
        except Exception as e:
            print(f"[LOG] [EXCEPTION]\n{e}")
            return 0


def check_n_reviews_limit(n_reviews, n_reviews_max):
    """Compare number of reviews loaded/saved to the limit 'n_reviews_max'.
    
    Args:
        n_reviews: value of reviews count.
        n_reviews_max: limit of reviews to load/save.
        
    Return:
        Bool, if the limit has been exceeded or not.
    """

    if n_reviews >= n_reviews_max:
        print("[LOG] [LIMIT] The reviews limit has been reached.")
        return True
    else:
        return False


def get_rating_from_colors(colors):
    """Evaluates the rating value based on the number of occurrences 
    of the color "#3cbeaf" in a list of colors.

    Args:
        colors (list): list of color codes in string 
                       format, such as "#3cbeaf" or "#E6E6E6".

    Returns:
        int, The rating value corresponding to the number of consecutive 
             occurrences of the color "#3cbeaf" in the list.
             The rating value starts at 1 and increases by 1 for 
             each group of consecutive "#3cbeaf" colors.
    """

    return colors.count("#3cbeaf")


def get_most_recent_json_file(folder_path):
    """Returns path to the most recent json file in a the specified folder.

    Args:
        folder_path (str): path of folder containing json files.

    Returns:
        str, most recently created json file path.
    """
    
    most_recent_json_file = \
        sorted(glob.glob(os.path.join(folder_path, '*.json')))[-1]
    
    return most_recent_json_file


def n_pages(n_reviews, n_reviews_per_page):
    """Determines the number of reviews pages per product.

    Args:
        n_reviews (int): number of reviews.
        n_reviews_per_page (int): number of reviews per page.

    Returns:
        int, Number of reviews pages.
    """

    return ceil(int(n_reviews) / n_reviews_per_page) + 1

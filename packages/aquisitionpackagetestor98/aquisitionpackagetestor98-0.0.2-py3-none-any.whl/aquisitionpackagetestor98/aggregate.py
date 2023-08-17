# !/usr/bin/env python

import glob
import json
from json import JSONDecodeError
import os
import sys
import time

sys.path.append('..')

from collector.packages.save import save_data
from collector.packages.utils import n_pages


def aggregate_new_urls(source_dict, 
                       new_urls_folder_path, 
                       aggregated_urls_folder_path):
    """Aggregates new URLs in 'aggregated_urls' folder.

    Args:
        source_dict (dict): dictionary with information from the source.
        new_urls_folder_path (str): path to the 'new_urls' folder.
        aggregated_urls_folder_path (str): path to the 'aggregated_urls' folder.
    """

    print("[LOG] Start to aggregate new URLs.")

    # Load and aggregate the new URLs
    new_urls_dicts = []
    for new_url_dicts_file in glob.glob(os.path.join(new_urls_folder_path, '*.json')):
        for new_url_dict in json.load(open(new_url_dicts_file, 'r', encoding='utf8')):
            new_urls_dicts.append(new_url_dict)

    # Save the aggregated new URLs in 'aggregated_urls' folder
    save_data(data=new_urls_dicts, 
              saved_data_type='aggregated_urls', 
              source=source_dict['source'], 
              path=aggregated_urls_folder_path)
    
    print(f"[LOG] {len(new_urls_dicts)} aggregated URLs have been saved "
           "in 'aggregated_urls' folder.")
    print("[LOG] The new URLs files have been aggregated.")


def remove_duplicates(dicts, 
                      key):
    """Removes duplicates from a list of dictionaries based on 
    a specified key.

    Args:
        dicts (list[dict]): list of dictionaries.
        key (str): key to use for comparing duplicates.

    Returns:
        list[dict], List of dictionaries with duplicates removed 
                    based on the specified key.
    """

    unique_keys = set()
    removed_duplicates_dicts = []

    for d in dicts:
        if d[key] not in unique_keys:
            unique_keys.add(d[key])
            removed_duplicates_dicts.append(d)

    return removed_duplicates_dicts


def remove_elements_with_keywords(dicts, 
                                  keys, 
                                  keywords):
    """Removes elements from a list of dictionaries if a 
    specific key contains a specific word.

    Args:
        dicts (list[dict]): a list of dictionaries.
        keys (list): list of keys to check for the keyword.
        keywords (list): list of words to look for in the value of the key.

    Returns:
        list[dict], List of dictionaries with elements removed based on the 
                    presence of the keywords.
    """

    results = []
    for d in dicts:
        keep = True
        for key in keys:
            if key not in d:
                continue
            value = str(d[key]).lower().strip()
            for keyword in keywords:
                if str(keyword).lower().strip() in value:
                    keep = False
                    break
            if not keep:
                break
        if keep:
            results.append(d)

    return results


def select_elements_with_keywords(dicts, 
                                  keys, 
                                  keywords):
    """Selects elements from a list of dictionaries if 
    a specific key contains a specific word.

    Args:
        dicts (list[dict]): A list of dictionaries.
        keys (list): List of keys to check for the keyword.
        keywords (list): List of words to look for in the value of the key.

    Returns:
        list[dict], List of dictionaries with elements selected based on the 
                    presence of the keywords.
    """

    results = []
    for d in dicts:
        keep = False
        for key in keys:
            if key not in d:
                continue
            value = str(d[key]).lower().strip()
            for keyword in keywords:
                if str(keyword).lower().strip() in value:
                    keep = True
                    break
            if keep:
                break
        if keep:
            results.append(d)

    return results


def filter_urls(source_dict, 
                keywords_for_removing, 
                keywords_for_selecting,
                new_urls_folder_path, 
                filtered_urls_folder_path):
    """Filters new URLs in 'filtered_urls' folder.

    Args:
        source_dict (dict): dictionary with information from the source.
        keywords_for_removing (list): list of keywords for removing. 
        keywords_for_selecting (list): list of keywords for selecting.
        new_urls_folder_path (str): path to the 'new_urls' folder.
        filtered_urls_folder_path (str): path to the 'filtered_urls' folder.
    """

    print("[LOG] Start to filter new URLs.")

    # Load and aggregate the new URLs
    new_urls_dicts = []
    for new_url_dicts_file in glob.glob(os.path.join(new_urls_folder_path, '*.json')):
        for new_url_dict in json.load(open(new_url_dicts_file, 'r', encoding='utf8')):
            new_urls_dicts.append(new_url_dict)

    # Filter the new URLs
    # Remove the duplicates
    filtered_urls_dicts = remove_duplicates(dicts=new_urls_dicts, 
                                            key='url')
    
    # Remove the elements with specific keywords
    if keywords_for_removing:
        filtered_urls_dicts = \
            remove_elements_with_keywords(dicts=filtered_urls_dicts, 
                                          keys=['product_name', 'product_brand', 'url'], 
                                          keywords=keywords_for_removing)
        
    # Select the elements with specific keywords
    if keywords_for_selecting:
        filtered_urls_dicts = \
            select_elements_with_keywords(dicts=filtered_urls_dicts, 
                                          keys=['product_name', 'product_brand', 'url'], 
                                          keywords=keywords_for_selecting)
        
    # Remove the duplicates
    filtered_urls_dicts = remove_duplicates(dicts=filtered_urls_dicts, 
                                            key='url')

    # Save filtered URLs in 'filtered_urls' folder
    save_data(data=filtered_urls_dicts,
              saved_data_type='filtered_urls',
              source=source_dict['source'],
              path=filtered_urls_folder_path)
    
    print(f"[LOG] {len(filtered_urls_dicts)} filtered URLs have been saved "
           "in 'filtered_urls' folder.")
    print("[LOG] The new URLs files have been filtered.")


def generate_urls_to_collect_dicts(filtered_urls_dicts):
    """Generates a list of product URLs to collect dictionaries
    from a list of new product URLs dictionaries.

    Args:
        filtered_urls_dicts (list[dict]): lst of dictionaries containing new product URLs.

    Returns:
        list[dict], List of dictionaries containing the product URLs, 
                    their category, and whether they have been collected.
    """

    urls_to_collect_dicts = [
        {
            'url': u['url'], 
            'collected': 'no'
        }
        for u in filtered_urls_dicts
    ]
    
    return urls_to_collect_dicts


def generate_urls_to_collect(source_dict, 
                             n_parts,
                             filtered_urls_dicts_object_name, 
                             urls_to_collect_folder_path, 
                             urls_to_collect_anchor_folder_path):
    """Generated URLs to collect files.

    Args:
        source_dict (dict): dictionary with information from the source.
        n_parts (int): number of partitions for the urls to collect files.
        filtered_urls_dicts_object_name (str): object name of the filtered URLs.
        urls_to_collect_folder_path (str): path to the 'urls_to_collect' folder.
        urls_to_collect_anchor_folder_path (str): path to the 'urls_to_collect_anchor' folder.
    """ 

    print("[LOG] Start to generate URLs to collect.")
    print(f"[LOG] Filtered URLs object name: {filtered_urls_dicts_object_name}.")
   
    # Load the filtered URLs
    with open(os.path.join(filtered_urls_dicts_object_name),
              encoding='utf-8') as file_to_open:
        filtered_urls_dicts = json.load(file_to_open)
    print(f"[LOG] There are {len(filtered_urls_dicts)} filtered URLs.")

    # Generate the URLs to collect
    urls_to_collect_dicts = \
        generate_urls_to_collect_dicts(filtered_urls_dicts=filtered_urls_dicts)
    
    # Calculate the size of each partition
    partition_size = len(urls_to_collect_dicts) // n_parts

    # Split the URLs to collect in partitions
    for i in range(0, len(urls_to_collect_dicts), partition_size):
        tmp_urls_to_collect_dicts = urls_to_collect_dicts[i:i + partition_size]

        # Save URLs to collect in 'urls_to_collect' folder
        save_data(data=tmp_urls_to_collect_dicts,
                  saved_data_type='urls_to_collect',
                  source=source_dict['source'],
                  path=urls_to_collect_folder_path)

        # Save URLs to collect in 'urls_to_collect_anchor' folder
        save_data(data=tmp_urls_to_collect_dicts,
                  saved_data_type='urls_to_collect_anchor',
                  source=source_dict['source'],
                  path=urls_to_collect_anchor_folder_path)
        
        # Add 2 second tempo for the unicity in the file name
        time.sleep(2)

        print(f"[LOG] {len(tmp_urls_to_collect_dicts)} URLs to collect dictionaries have been saved "
               "in 'urls_to_collect' and 'urls_to_collect_anchor' folders.")
    
    if n_parts == 1:
        print("[LOG] The URLs to collect file have been generated.")
    elif n_parts > 1:
        print("[LOG] The URLs to collect files have been generated.")


def generate_product_url_to_collect_dict(product_url):
    """Generates product URL to collect dictionary.
    
    Args:
        product_url (str): product URL.

    Returns:
        dict, Product URL to collect dictionary.
    """

    return {
        'url': str(product_url),
        'collected': 'no'
    }


def generate_reviews_urls_to_collect_dicts(product_url, 
                                           n_reviews, 
                                           n_reviews_per_page,
                                           str_prefix,
                                           str_between_url_n_pages,
                                           str_suffix):
    """Generates reviews URLs to collect dictionaries.

    Args:
        product_url (str): product URL.
        n_reviews (int): number of reviews.
        n_reviews_per_page (int): number of reviews per page.
        str_prefix (str): string to add at the beginning of the reviews URL.
        str_between_url_n_pages (str): string to add between the 
                                       reviews URL and the number of pages.
        str_suffix (str): string to add at the end of the reviews URL.

    Returns:
        list[dict], List of reviews URLs to collect dictionaries.
    """
    
    reviews_urls_to_collect_dicts = []

    for n_page in range(1, n_pages(n_reviews=n_reviews, 
                                   n_reviews_per_page=n_reviews_per_page)):
        url = str(product_url)
        if str_prefix:
            url = str_prefix + str(product_url)
        if str_between_url_n_pages:
            url = url + str_between_url_n_pages + str(n_page)
        if str_suffix:
            url = url + str_suffix
            
        reviews_urls_to_collect_dicts.append({
            'url': url,
            'collected': 'no'
        })
    
    return reviews_urls_to_collect_dicts


def aggregate_products_files(source_dict,
                             products_folder_path, 
                             aggregated_products_folder_path):
    """Aggregates the collected products files.
    
    Args:
        source_dict (dict): dictionary with information from the source.
        products_folder_path (str): path to the products data files folder.
        aggregated_products_folder_path (str): path to the aggregated products folder.
    """

    print("[LOG] Start to aggregate products files.")
    
    products_files = []
    
    for products_file in glob.glob(os.path.join(products_folder_path, '*.json')):
        try:
            with open(products_file, 'r', encoding='utf8') as f:
                open_product_file = json.load(f)
                products_files.append(open_product_file)
        except JSONDecodeError:
            pass

    aggregated_products_file_name = os.path.join(
        aggregated_products_folder_path, 
        f"{time.strftime('%Y_%m_%d_%H_%M_%S')}_aggregated_products_{source_dict['source']}.json")
    
    with open(aggregated_products_file_name, 'w', encoding='utf-8') as file_to_dump:
        json.dump(products_files, file_to_dump, indent=4, ensure_ascii=False)
    
    print(f"[LOG] There are {len(products_files)} aggregated products.")
    print("[LOG] The products files have been aggregated.")


def aggregate_reviews_files(source_dict,
                            reviews_folder_path, 
                            aggregated_reviews_folder_path):
    """Aggregates the collected reviews files.
    
    Args:
        source_dict (dict): dictionary with information from the source.
        reviews_folder_path (str): path to the reviews data files folder.
        aggregated_reviews_folder_path (str): path to the aggregated reviews folder.
    """

    print("[LOG] Start to aggregate reviews files.")

    reviews_files = []

    for reviews_file in glob.glob(os.path.join(reviews_folder_path, '*.json')):
        try:
            with open(reviews_file, 'r', encoding='utf8') as f:
                reviews_dicts = json.load(f)
                reviews_files.extend(reviews_dicts)
        except JSONDecodeError:
            pass

    aggregated_reviews_file_name = os.path.join(
        aggregated_reviews_folder_path, 
        f"{time.strftime('%Y_%m_%d_%H_%M_%S')}_aggregated_reviews_{source_dict['source']}.json")
    
    with open(aggregated_reviews_file_name, 'w', encoding='utf-8') as file_to_dump:
        json.dump(reviews_files, file_to_dump, indent=4, ensure_ascii=False)

    print(f"[LOG] There are {len(reviews_files)} aggregated reviews.")
    print("[LOG] The reviews files have been aggregated.")

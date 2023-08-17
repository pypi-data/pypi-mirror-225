#!/usr/bin/env python

import datetime
import glob
import os
import subprocess
import sys
import time

sys.path.append('..')


def generate_file_name(source_dict, 
                       state):
    """Generates files names with the `state`.

    Args:
        source_dict (dict): dictionary containing the source information.
        state (str): name of the state.
        
    Returns:
        str, Modified file name.
    """
    
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    return f"{timestamp}_{state}_{source_dict['source']}.json"


def generate_s3_object_name_inside_z00_ingest_zone(source_dict, 
                                                   state,
                                                   file_name):
    """Generates an object name in the z00-ingest zone.

    Args:
        source_dict (dict): dictionary containing the source information.
        state (str): name of the state.
        file_name (str): file name.

    Returns:
        str, Generated object name in the z00-ingest zone.
    """

    current_date = datetime.datetime.now()
    year = current_date.strftime("%Y")
    month = current_date.strftime("%m")

    return os.path.join(source_dict['source'], state, year, month, file_name)


def send_files_to_s3(file_to_transfer_object_name, 
                     zone_name, 
                     file_to_transfer_s3_object_name):
    """Sends `file_to_transfer_object_name` in AWS S3 bucket `zone_name`.

    Args:
        file_to_transfer_object_name (str): local object name to be transfered.
        zone_name (str): name of the AWS S3 bucket.
        file_name (str): generated AWS S3 object name in the bucket.
    """

    try:
        # print(f"[LOG] Attempting to transfer to S3: {file_to_transfer_object_name}")
        subprocess.run(["aws", "s3", "cp", 
                        file_to_transfer_object_name, 
                        os.path.join(f"s3://{zone_name}", file_to_transfer_s3_object_name)])
        # print(f"[LOG] Successfully transferred to S3 as: {file_to_transfer_s3_object_name}")
    except subprocess.CalledProcessError as e:
        print(f"[LOG] [EXCEPTION]\n{e}")


def transfer_state_files_to_s3(source_dict, 
                               state, 
                               state_local_folder_path):
    """Transfers the `state` files to AWS S3.
    
    Args:
        source_dict (dict): dictionary containing the source information.
        state (str): name of the state.
        state_local_folder_path (str): folder path with the `state` files.
    """
    
    print(f"[LOG] Start to transfer files '{state}' to S3.")
    if sorted(glob.glob(os.path.join(state_local_folder_path, "*.json"))):
        for state_local_object_name in \
            sorted(glob.glob(os.path.join(state_local_folder_path, "*.json"))):
            new_generated_file_name = \
                generate_file_name(source_dict=source_dict, state=state)
            new_generated_s3_object_name = \
                generate_s3_object_name_inside_z00_ingest_zone(source_dict=source_dict, 
                                                                state=state, 
                                                                file_name=new_generated_file_name)
            send_files_to_s3(file_to_transfer_object_name=state_local_object_name,
                             zone_name="voysen-z00-ingest-zone-eu-west-3",
                             file_to_transfer_s3_object_name=new_generated_s3_object_name)
            time.sleep(2)
        print(f"[LOG] Files '{state}' have been transferred.")
    else:
        print(f"[LOG] There aren't any files '{state}' to transfer.")


def transfer_files_to_s3(source_dict,
                         aggregated_urls_folder_path,
                         aggregated_urls,
                         filtered_urls_folder_path,
                         filtered_urls,
                         urls_to_collect_folder_path,
                         urls_to_collect,
                         urls_to_collect_anchor_folder_path,
                         urls_to_collect_anchor,
                         aggregated_products_folder_path,
                         aggregated_products,
                         aggregated_reviews_folder_path,
                         aggregated_reviews):
    """Transfers files to S3.
    
    Args:
        source_dict (dict): dictionary containing the source information.
        aggregated_urls_folder_path (str): folder path to aggregated URLs.
        aggregated_urls (bool): transfer aggregated URLs.
        filtered_urls_folder_path (str): folder path to filtered URLs.
        filtered_urls (bool): transfer filtered URLs.
        urls_to_collect_folder_path (str): folder path to URLs to collect.
        urls_to_collect (bool): transfer URLs to collect.
        urls_to_collect_anchor_folder_path (str): folder path to URLs to collect anchor.
        urls_to_collect_anchor (bool): transfer URLs to collect anchor
        aggregated_products_folder_path (str): folder path to aggregated products.
        aggregated_products (bool): transfer aggregated products.
        aggregated_reviews_folder_path (str): folder path to aggregated reviews.
        aggregated_reviews (bool): transfer aggregated reviews.
    """

    # Aggregated URLs
    if aggregated_urls:
        transfer_state_files_to_s3(source_dict=source_dict, 
                                   state='aggregated_urls', 
                                   state_local_folder_path=aggregated_urls_folder_path)

    # Filtered URLs
    if filtered_urls:
        transfer_state_files_to_s3(source_dict=source_dict, 
                                   state='filtered_urls', 
                                   state_local_folder_path=filtered_urls_folder_path)
        
    # URLs to collect
    if urls_to_collect:
        transfer_state_files_to_s3(source_dict=source_dict, 
                                   state='urls_to_collect', 
                                   state_local_folder_path=urls_to_collect_folder_path)
        
    # URLs to collect anchor
    if urls_to_collect_anchor:
        transfer_state_files_to_s3(source_dict=source_dict, 
                                   state='urls_to_collect_anchor', 
                                   state_local_folder_path=urls_to_collect_anchor_folder_path)

    # Aggregated products
    if aggregated_products:
        transfer_state_files_to_s3(source_dict=source_dict, 
                                   state='aggregated_products', 
                                   state_local_folder_path=aggregated_products_folder_path)

    # Aggregated reviews
    if aggregated_reviews:
        transfer_state_files_to_s3(source_dict=source_dict, 
                                   state='aggregated_reviews', 
                                   state_local_folder_path=aggregated_reviews_folder_path)

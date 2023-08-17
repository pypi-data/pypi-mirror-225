# !/usr/bin/env python

import time


def init_url_dict(source_dict):
    """Initializes the dictionary with the new URL data.

    Args:
        source_dict (dict): dictionary with information from the source.

    Returns:
       dict, Dictionary with the new URL data.
    """

    url_dict = {
        'id': None,
        # Product name & brand
        'product_name': None, # (str)
        'product_sub_name': None, # (str)
        'product_brand': None, # (str)
        'product_brand_line': None, # (str)
        # Product information
        'product_price': None, # (str)
        'product_type' : None, # (str)
        # Ratings
        'mean_rating': None, # (str / int / float)
        'n_reviews': 0, # (int)
        # Codes
        'code_asin': None, # (str)
        'code_ean': None, # (str)
        'code_gtin': None, # (str)
        'code_sku': None, # (str)
        'code_source': None, # (str)
        # URL
        'url': None,
        # Origin
        'products_listing_page_origin': None,
        'products_listing_page_url': None, 
        'products_listing_page_product_brand': None,
        'products_listing_page_search_keyword': None,
        'products_listing_page_category': None,
        'products_listing_page_sub_category': None,
        'products_listing_page_sub_sub_category': None, 
        # Source
        'country': source_dict['country'], # (str)
        'language': source_dict['language'], # (str)
        'source': source_dict['source'], # (str)
        # Collecte
        'collect_date': str(time.strftime('%Y-%m-%d')), # (str)
    }

    return url_dict


def init_product_dict(source_dict):
    """Initializes the dictionary with the product data.

    Args:
        source_dict (dict): dictionary with information from the source.

    Returns:
        dict, Dictionary with the product data.
    """

    product_dict = {
        # Product name & brand
        'product_name': None, # (str)
        'product_sub_name': None, # (str)
        'product_brand': None, # (str)
        'product_brand_line': None, # (str)
        # Product information
        'product_advice': None, # (str)
        'product_application_ld_json_dict': None, # (dict)
        'product_attribute': None, # (str)
        'product_attribute_dict': None, # (dict)
        'product_detail': None, # (str)
        'product_detail_dict': None, # (dict)
        'product_description': None, # (dict)
        'product_formulation': None, # (str)
        'product_information': None, # (str)
        'product_information_dict': None, # (dict)
        'product_price': None, # (str)
        'product_syndication': None, # (str)
        'product_syndication_dict': None, # (dict)
        'product_type' : None, # (str)
        # Ratings
        'mean_rating': None, # (str / int / float)
        'n_reviews': 0, # (int)
        'product_other_rating': None, # (str)
        'product_other_rating_dict': None, # (dict)
        # URL
        'url': None,
        # Categories
        'category': None, # (str)
        'sub_category': None, # (str)
        'sub_sub_category': None, # (str)
        'sub_sub_sub_category': None, # (str)
        # Codes
        'code_asin': None, # (str)
        'code_ean': None, # (str)
        'code_gtin': None, # (str)
        'code_sku': None, # (str)
        'code_source': None, # (str)
        # Source
        'country': source_dict['country'], # (str)
        'language': source_dict['language'], # (str)
        'source': source_dict['source'], # (str)
        # Collecte
        'collect_date': str(time.strftime('%Y-%m-%d')), # (str)
    }

    return product_dict


def init_review_dict(source_dict):
    """Initializes the dictionary with the review data.

    Returns:
        dict: Dictionary with the review data.
    """

    review_dict = {
        'id': None,
        # Product name & brand
        'product_name': None, # (str)
        'product_sub_name': None, # (str)
        'product_brand': None, # (str)
        'product_brand_line': None, # (str)
        # URL
        'url': None, # (str)
        'review_url': None, # (str)
        # Categories
        'category': None, # (str)
        'sub_category': None, # (str)
        'sub_sub_category': None, # (str)
        'sub_sub_sub_category': None, # (str)
        # Codes
        'code_asin': None, # (str)
        'code_ean': None, # (str)
        'code_gtin': None, # (str)
        'code_sku': None, # (str)
        'code_source': None, # (str)
        # Writer
        'writer_age': None, # (str)
        'writer_information': None, # (str)
        'writer_information_dict': None, # (dict)
        'writer_location': None, # (str)
        'writer_pseudo': None, # (str)
        'writer_recommendation': None, # (str)
        'writer_sex': None, # (str)
        'writer_usage': None, # (str)
        # Review
        'review_rating': None, # (str)
        'review_other_rating': None, # (str)
        'review_other_rating_dict': None, # (dict)
        'review_date': None, # (str)
        'review_title': None, # (str)
        'review_text': None, # (str)
        'review_text_strength': None, # (str)
        'review_text_weakness': None, # (str)
        # Labels
        'syndication': None, # (str)
        'utility': None, # (str)
        'utility_yes': None, # (str)
        'utility_no': None, # (str)
        'verified_purchase': None, # (str)
        # Source
        'country': source_dict['country'], # (str)
        'language': source_dict['language'], # (str)
        'source': source_dict['source'], # (str)
        # Collecte
        'collect_date': str(time.strftime('%Y-%m-%d')), # (str)
    }

    return review_dict

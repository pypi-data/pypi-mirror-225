#!/usr/bin/env python

import json
import time
import os
import sys
import random

sys.path.append('..')


def display_collected_reviews_data(reviews_dicts):
    """Takes the dictionary of any type of data collected (URL, product or review)
    and displays random values of the dictionary.

    Args:
        reviews_dicts (list[dict]): list of collected reviews data dict.
    """

    # Attributes to display
    useful_attributes = [
        'product_name',
        'product_brand',
        'category',
        'code_ean',
        'code_gtin',
        'code_sku',
        'code_source',
        'writer_pseudo',
        'review_rating',
        'review_date',
        'review_title',
        'review_text',
        'syndication',
        'utility',
        'utility_yes',
        'utility_no',
        'verified_purchase',
    ]

    # Display 3 attributes
    useful_attributes_to_display = random.sample(useful_attributes, 3)

    # Display attributes for 3 reviews
    n_reviews_to_display = min(3, len(reviews_dicts))

    # Print the attributes
    if reviews_dicts:
        for review_dict in random.sample(reviews_dicts, n_reviews_to_display):
            for useful_attribute_to_display in useful_attributes_to_display:
                print(f"[LOG] [DISPLAY COLLECTED DATA] "
                      f"{useful_attribute_to_display}: "
                      f"{review_dict[useful_attribute_to_display]}")
    else:
        print("[LOG] 0 reviews have been saved.")


def save_products_listing_pages_brands(data, path):
    """Saves collected names and URLs from brand listing page
    
    Args:
        data (list): data to save
        path (str): path where the data will be saved.
    """

    str_to_dump = "BRANDS = [\n" 
    for elt in data:
        str_to_dump += "    " + f"{elt},\n"
    str_to_dump += "]\n"

    file_object_name = str(path + '/brands.py').lower()

    with open(file_object_name, 'w+', encoding='utf-8') as brands:  
        brands.write(str_to_dump)


def save_data(data, saved_data_type, source, path):
    """Saves the collected `data`.

    Args:
        data (object): data to save.
        saved_data_type (str): 'url_new', 'products' or 'reviews'.
        source (str): name of the source.
        path (str): path where the data will be saved.
    """

    with open(os.path.join(path, time.strftime('%Y_%m_%d_%H_%M_%S') + '_' + \
                                 saved_data_type + '_' + source + '.json'), 
              'w+', encoding='utf-8') as file_to_dump:
        json.dump(data, file_to_dump, indent=4, ensure_ascii=False)

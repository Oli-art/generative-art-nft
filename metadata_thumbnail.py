#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import time
import os
from progressbar import progressbar
import json
from copy import deepcopy

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Base metadata. MUST BE EDITED.
BASE_IMAGE_URL = "ipfs://QmaTNkSh44vc2jYYs22aFw3ibgXZEL4uJx9AYcmmbd9emg"
BASE_NAME = "Tangle Dragon Genesis Card #"

BASE_JSON = {
    "name": BASE_NAME,
    "description": "Tangle Dragons Genesis NFT Cards are the first official collection of the Zentangle Ecosystem. The owners of this collection (a.k.a. NFT hodlers) benefit from a series of perks based on the access membership to Zentangle Ecosystem that will grant access to exclusive members only NFT airdrops, future ZenTangle capabilities such as additional digital assets, staking, genesis collection buyer royalty, phy-gital products, artists identity verification. The Genesis NFT Cards Sale come with a special feature for first buyers; the so called First Buyer Collection Royalty. This royalty takes into account the relation between the NFT rarity points and the collection rarity points spread between available NFTs from the collection. Different gadgets, characteristics, materials, and combinations define the rarity points of each Tangle Dragon.",
    "image": BASE_IMAGE_URL,
    "attributes": [],
}


# Get metadata and JSON files path based on edition
def generate_paths(edition_name):
    edition_path = os.path.join('output', 'edition ' + str(edition_name))
    metadata_path = os.path.join(edition_path, 'metadata.csv')
    json_path = os.path.join(edition_path, 'json')

    return edition_path, metadata_path, json_path

# Function to convert snake case to sentence case
def clean_attributes(attr_name):
    
    clean_name = attr_name.replace('_', ' ')
    clean_name = list(clean_name)
    
    for idx, ltr in enumerate(clean_name):
        if (idx == 0) or (idx > 0 and clean_name[idx - 1] == ' '):
            clean_name[idx] = clean_name[idx].upper()
    
    clean_name = ''.join(clean_name)
    return clean_name

    # Function to convert snake case to sentence case
def clean_value(value):
    
    if not isinstance(value, str):
        return value
    
    clean_value = value.replace('_', ' ')
    clean_value = list(clean_value)
    
    for idx, ltr in enumerate(clean_value):
        if (idx == 0) or (idx > 0 and clean_value[idx - 1] == ' '):
            clean_value[idx] = clean_value[idx].upper()
    
    clean_value = ''.join(clean_value)
    return clean_value


# Function to get attribure metadata
def get_attribute_metadata(metadata_path):

    # Read attribute data from metadata file 
    df = pd.read_csv(metadata_path)
    df = df.drop('Unnamed: 0', axis = 1)
    df.columns = [clean_attributes(col) for col in df.columns]

    # Get zfill count based on number of images generated
    # -1 according to nft.py. Otherwise not working for 100 NFTs, 1000 NTFs, 10000 NFTs and so on
    zfill_count = len(str(df.shape[0]-1))

    return df, zfill_count

# Main function that generates the JSON metadata
def main():

    # Get edition name
    print("Enter edition you want to generate metadata for: ")
    while True:
        edition_name = input()
        edition_path, metadata_path, json_path = generate_paths(edition_name)

        if os.path.exists(edition_path):
            print("Edition exists! Generating JSON metadata...")
            break
        else:
            print("Oops! Looks like this edition doesn't exist! Check your output folder to see what editions exist.")
            print("Enter edition you want to generate metadata for: ")
            continue
    
    # Make json folder
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    
    # Get attribute data and zfill count
    df, zfill_count = get_attribute_metadata(metadata_path)
    
    for idx, row in progressbar(df.iterrows()):    
    
        idx = idx + 1
        
        # Get a copy of the base JSON (python dict)
        item_json = deepcopy(BASE_JSON)
        
        # Append number to base name
        item_json['name'] = item_json['name'] + str(idx)

        # Append image PNG file name to base image path
        item_json['image'] = item_json['image'] + str(idx) + '.jpg'
        
        # Convert pandas series to dictionary
        attr_dict = dict(row)
        
        # Add all existing traits to attributes dictionary
        for attr in attr_dict:
            item_json['attributes'].append({ 'trait_type': attr, 'value': clean_value(attr_dict[attr]) })
        
        # Write file to json folder
        item_json_path = os.path.join(json_path, str(idx))
        with open(item_json_path, 'w') as f:
            json.dump(item_json, f)

# Run the main function
main()

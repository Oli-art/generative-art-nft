#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import os
from progressbar import progressbar
import json
from copy import deepcopy

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Get metadata and JSON files path based on edition
def generate_paths(edition_name):
    edition_path = os.path.join('output', 'edition ' + str(edition_name))
    metadata_path = os.path.join(edition_path, 'metadata.csv')
    
    output_path = os.path.join(edition_path, 'raritymetadata.csv')
    
    return edition_path, metadata_path, output_path

# Function to convert snake case to sentence case
def clean_attributes(attr_name):
    
    clean_name = attr_name.replace('_', ' ')
    clean_name = list(clean_name)
    
    for idx, ltr in enumerate(clean_name):
        if (idx == 0) or (idx > 0 and clean_name[idx - 1] == ' '):
            clean_name[idx] = clean_name[idx].upper()
    
    clean_name = ''.join(clean_name)
    return clean_name


# Function to get attribure metadata
def get_attribute_metadata(metadata_path):

    # Read attribute data from metadata file 
    df = pd.read_csv(metadata_path)
    df = df.drop('Unnamed: 0', axis = 1)
    df.columns = [col for col in df.columns]

    # Get zfill count based on number of images generated
    # -1 according to nft.py. Otherwise not working for 100 NFTs, 1000 NTFs, 10000 NFTs and so on
    zfill_count = len(str(df.shape[0]-1))

    return df, zfill_count

# Main function that generates the JSON metadata
def main():
    rarities = {
        "card_materials": {
            "Platinum": 0.5,
            "Gold": 0.3,
            "Titanium": 0.2
        },
        "card_patterns": {
            "Hexagon Grid": 0.3,
            "Pixel Gradient": 0.25,
            "Candy": 0.2,
            "Kevlar": 0.15,
            "Hairy": 0.1
        },
        "dragon_allhorns": {
            "Bone": 0.7,
            "Gold": 0.25,
            "Rainbow": 0.05
        },
        "dragon_wings": {
            "Yellow": 0.16,
            "Green": 0.14,
            "Orange": 0.14,
            "Pink": 0.14,
            "Blue": 0.14,
            "Purple": 0.14,
            "Red": 0.14
        },
        "dragon_eye_colors": {
            "Black": 0.4,
            "Brown": 0.4,
            "Green & Blue": 0.2,
        },
        "dragon_gatget": {
            "Crown":	0.4,
            "ZENT Token Platinum": 0.3,
            "ZENT Token Gold": 0.2,
            "ZENT Token Titanium": 0.1
        },
        "dragon_skin_texture": {
            "Red": 0.2,
            "Purple": 0.2,
            "Green": 0.2,
            "Blue": 0.2,
            "Dark": 0.2
        }
    }
    
    rarities2 = {
        "card_materials": {
            "Platinum": 0.5,
            "Gold": 0.3,
            "Titanium": 0.2
        },
        "card_patterns": {
            "Emerald": 0.3,
            "Purple": 0.25,
            "Navy": 0.2,
            "Kevlar": 0.15,
            "Rainbow": 0.1
        },
        "dragon_allhorns": {
            "Bone": 0.7,
            "Gold": 0.25,
            "Rainbow": 0.05
        },
        "dragon_wings": {
            "Yellow": 0.16,
            "Green": 0.14,
            "Orange": 0.14,
            "Pink": 0.14,
            "Blue": 0.14,
            "Purple": 0.14,
            "Light Green": 0.14
        },
        "dragon_eye_colors": {
            "Purple": 0.2,
            "Pink": 0.2,
            "Turquoise": 0.2,
            "Light Green": 0.2,
            "Sauron Green": 0.2
        },
        "dragon_gadget": {
            "none":	0.4,
            "token": 0.3,
            "crown": 0.2,
            "token + crown": 0.1
        },
        "dragon_skin_texture": {
            "Red": 0.16,
            "Purple": 0.14,
            "Green": 0.14,
            "Turquoise": 0.14,
            "Dark": 0.14,
            "Orange": 0.14,
            "Brown": 0.14
        },
        "dragon_eye_patch": {
            "Yes": 0.1,
            "No": 0.9
        }
    }

    # Get edition name
    print("Enter edition you want to generate metadata for: ")
    while True:
        edition_name = input()
        edition_path, metadata_path, output_path = generate_paths(edition_name)

        if os.path.exists(edition_path):
            print("Edition exists! Generating rarity metadata...")
            break
        else:
            print("Oops! Looks like this edition doesn't exist! Check your output folder to see what editions exist.")
            print("Enter edition you want to generate metadata for: ")
            continue
    
    # Get attribute data and zfill count
    df, zfill_count = get_attribute_metadata(metadata_path)
    
    rarity_column = []
    
    for idx, row in progressbar(df.iterrows()):
        
        # Convert pandas series to dictionary
        attr_dict = dict(row)
        
        rarity = 1
        # Add all existing traits to attributes dictionary
        for attr in attr_dict:
            value = attr_dict[attr]
            
            # Check if it is a string to avoid the "levels" attributes
            if isinstance(value, str):
                rarity = rarity * rarities[attr][value]
        rarity_column.append(rarity * 1000000)
        
    df.insert(loc=len(df.columns), column='rarity', value=rarity_column)
    df.to_csv(output_path, index = False)
        
        
# Run the main function
main()

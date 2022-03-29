# Python program to rename all file
# names in your directory
import os
import re

os.chdir('directorio')
print(os.getcwd())

# Regex to remove leading
# zeros from a string
regex = "^0+(?!$)"
 
for count, f in enumerate(os.listdir()):
    f_name, f_ext = os.path.splitext(f)
    
    # Delete letters
    f_name = ''.join(filter(str.isdigit, f_name))
    
    # Replaces the matched
    # value with given string
    f_name = re.sub(regex, "", f_name)
 
    new_name = f'{f_name}{f_ext}'
    os.rename(f, new_name)
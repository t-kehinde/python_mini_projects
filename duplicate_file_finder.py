# #########################################################################
# DUPLICATE FILE FINDER
# tags: [system_automation, file_handling, hashing]
#
# This program finds duplicate files in a directory and provides option to
# remove duplicates
# #########################################################################


import sys
import os
import hashlib


def get_file_info(directory):
    """Sort files by their size"""
    dict_files = {}
    for root, _, filenames in os.walk(directory, topdown=False):
        for name in filenames:
            if file_format != "" and name.endswith(file_format):
                file_size = f"{os.path.getsize(os.path.join(root, name))} bytes"
                if file_size not in dict_files:
                    dict_files[file_size] = [os.path.join(root, name)]
                else:
                    dict_files[file_size].append(
                        os.path.join(root, name))
            # if the file format is not specified, return all files
            elif file_format == "":
                file_size = f"{os.path.getsize(os.path.join(root, name))} bytes"
                if file_size not in dict_files:
                    dict_files[file_size] = [os.path.join(root, name)]
                else:
                    dict_files[file_size].append(
                        os.path.join(root, name))
    return dict_files


def sort_dict(dict_files, order):
    """ sorts a dictionary of files based on the file size"""
    # sort by the integer part of the key
    sorted_files = sorted(dict_files.items(), key=lambda kv: int(
        kv[0].split(" ")[0]), reverse=order)
    return sorted_files


def get_file_hash(file_path):
    """Get the hash of the file of same size"""
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    return file_hash


def get_duplicate_files(sorted_files):
    """Get duplicate files"""
    nested_dict = {}
    for size, value in sorted_files:
        for file in value:
            file_hash = get_file_hash(file)
            if size not in nested_dict:
                nested_dict[size] = {file_hash: [file]}
            else:
                if file_hash not in nested_dict[size]:
                    nested_dict[size][file_hash] = [file]
                else:
                    nested_dict[size][file_hash].append(file)

    # Print duplicate files
    hash_count = 1
    n_prev = 1
    duplicate_files = {}
    duplicate_files_numbers = []
    for size, value in nested_dict.items():

        for file_hash, file_list in value.items():
            if len(file_list) > 1:

                # create a new dictionary for duplicate file
                duplicate_files[hash_count] = {
                    "size": size, "hash": file_hash, "files": file_list}

                # add numbers to the file names
                for i in range(len(file_list)):
                    duplicate_files[hash_count]["files"][i] = f"{n_prev}. {file_list[i]}"
                    duplicate_files_numbers.append(n_prev)
                    n_prev += 1      # continue numbering
                hash_count += 1

    # print the dictionary for each line
    prev_size = ""
    for _, value in duplicate_files.items():
        # print the size of the duplicate files
        if value['size'] != prev_size:
            print(f"{value['size']}")
            prev_size = value['size']
        # print the hash value of the duplicate files
        print(f"Hash: {value['hash']}")
        # print the duplicate files
        for file in value["files"]:
            print(file)
        print("")
    return duplicate_files, duplicate_files_numbers


def remove_duplicate():
    """Remove duplicate files"""
    duplicate_files, hashed_file_numbers = get_duplicate_files(sorted_dict)

    # Prompt user to select files to delete
    file_numbers = input("""Enter file numbers to delete:\n""")

    # create list of the numbers to delete
    while True:
        try:
            file_numbers = file_numbers.split(" ")
            file_numbers = [int(i) for i in file_numbers]
            break
        except ValueError:
            file_numbers = input("Wrong format\n")

    # Check that the file numbers are valid
    while not set(file_numbers).issubset(set(hashed_file_numbers)) or len(file_numbers) == 0:
        file_numbers = input("""Wrong format\n""")

    # delete files
    size_to_delete = 0
    for file_number in file_numbers:

        # get the size of the file to delete
        for _, value in duplicate_files.items():

            # find the file name with the file number
            for file in value["files"]:
                if int(file.split(".")[0]) == file_number:
                    file_to_delete = file

                    # remove the number from the file name
                    file_to_delete = file_to_delete.split(" ")[1].strip()

                    # get the size of the file to delete
                    size_to_delete += os.path.getsize(file_to_delete)
                    os.remove(file_to_delete)   # delete the file

                    print(f"Deleted {file_to_delete}")
    print(f"Total freed up space: {size_to_delete} bytes")


# ===============================================================================
# MAIN PROGRAM
# ===============================================================================
try:
    directory = sys.argv[1]
except IndexError:
    print("Directory is not specified")
    sys.exit(1)

file_format = input("""
Enter file format:
""")

file_sort = input("""
Size sorting options:
1. Descending
2. Ascending

Enter a sorting option:
""")

while file_sort != "1" and file_sort != "2":
    file_sort = input("""
Wrong option.

Enter a sorting option:
""")

sort_order = True if file_sort == "1" else False

# Get the files in the directory
dict_files = get_file_info(directory)

# Sort the dictionary of files in ascending or descending order
sorted_dict = sort_dict(dict_files,  sort_order)
for key, value in sorted_dict:
    print(f"{key}")
    for file in value:
        print(f"{file}")  # print(f"\t{file}")
    print("\n")

# Check for duplicate files
is_check_duplicate = input("""Check for duplicates?
""")

while is_check_duplicate != "no" or is_check_duplicate != "yes":
    if is_check_duplicate == "yes" or is_check_duplicate == "no":
        break
    else:
        is_check_duplicate = input("""Wrong option.
  """)

# Perform duplicate files checker if requested
dict_hashed_files = {}
if is_check_duplicate == "yes":
    get_duplicate_files(sorted_dict)
else:
    print("Exiting...")
    sys.exit(0)

# Remove duplicate files
to_delete = input("""
Delete files? (yes/no)
""")
while to_delete != "yes" and to_delete != "no":
    if to_delete in ["yes", "no"]:
        break
    to_delete = input("Wrong option. (yes/no)\n")

if to_delete == "yes":
    remove_duplicate()
else:
    print("Exiting...")
    sys.exit(0)

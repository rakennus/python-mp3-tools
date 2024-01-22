import os
import eyed3
import sys
from colorama import init, Fore, Back, Style
import fnmatch

folder_path = sys.argv[1]
string_to_remove = sys.argv[2]
# mp3_files = [file for file in os.listdir(folder_path) if file.lower().endswith(".mp3")]

def get_all_mp3_files(folder_path):
    mp3_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in fnmatch.filter(files, '*.mp3'):
            mp3_files.append(os.path.join(root, file))
    return mp3_files

mp3_files = get_all_mp3_files(folder_path)
files_table = []
# Initialize colorama to work with Windows terminal
init(autoreset=True)


def remove_string_from_title(mp3_file, string_to_remove):
    audiofile = eyed3.load(mp3_file)
    
    if audiofile.tag is not None:
        audiofile.tag.title = audiofile.tag.title.replace(string_to_remove, "").strip()
        audiofile.tag.save()
    else:
        print("No ID3 tag found in the file.")

def print_table(data):
    # Determine the width of each column
    col_widths = [max(len(str(item)) for item in col) for col in zip(*data)]
    
    # Print the table data
    for row in data[0:]:
        for i, item in enumerate(row):
            print(f"{item:<{col_widths[i]}}", end="  ")
        print()  # Move to the next line after printing the row

def highlight_removed(text, removed_text):
    # Find the index of the removed_text in the original text
    index = text.find(removed_text)

    if index != -1:
        # Remove the specified part from the text
        modified_text = text[:index] + text[index + len(removed_text):]

        # Print the modified text with removed part highlighted in red
        colored_text = text[:index] + Fore.RED + Back.YELLOW + Style.BRIGHT + removed_text + Style.RESET_ALL + text[index + len(removed_text):]
        return(colored_text)
    else:
        return(text)

for index, mp3_file in enumerate(mp3_files):
    audiofile = eyed3.load(mp3_file)
    
    if audiofile.tag is not None:
        row = [index, highlight_removed(audiofile.tag.title, string_to_remove)]
        files_table.append(row)
    else:
        print(f"Processing file {index + 1}: No ID3 tag found in the file.")

print_table(files_table)

# Prompt the user for a yes/no response
response = input("\nDo you want to proceed? (y/n): ")
# Convert the user's response to lowercase to handle case-insensitivity
response = response.lower()

# Check the user's response
if response == "y":
    print("You chose to proceed.\n")
    for index, mp3_file in enumerate(mp3_files):
        remove_string_from_title(mp3_file, string_to_remove)

    files_table = []

    for index, mp3_file in enumerate(mp3_files):
        audiofile = eyed3.load(mp3_file)
        
        if audiofile.tag is not None:
            row = [index, audiofile.tag.title]
            files_table.append(row)
        else:
            print(f"Processing file {index + 1}: No ID3 tag found in the file.")

    print_table(files_table)

elif response == "n":
    print("You chose not to proceed.")
else:
    print("Invalid response. Please enter 'yes' or 'no'.")



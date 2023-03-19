import os
import shutil


def copy_json_files(input_path, output_path):
    # Initialize a counter to generate unique names for copied files
    i = 0

    # Recursively search for all JSON files in the input directory
    for dirpath, dirnames, filenames in os.walk(input_path):
        for filename in filenames:
            if filename.endswith('.json'):
                # Construct the source and destination file paths
                source_path = os.path.join(dirpath, filename)
                dest_path = os.path.join(output_path, f'input_{i}.json')

                # Copy the file to the output directory
                shutil.copyfile(source_path, dest_path)

                # Increment the counter
                i += 1


if __name__ == '__main__':
    # Specify the input and output directories
    input_path = '/Users/tadeasfort/Documents/pythonJSprojects/gitHub/facebook_json_message_data_parser_public/feed/fb'
    output_path = '/Users/tadeasfort/Documents/pythonJSprojects/gitHub/facebook_json_message_data_parser_public/in'

    # Call the copy_json_files function to copy the JSON files
    copy_json_files(input_path, output_path)

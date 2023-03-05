# README

## Installation
To run this script, you will need the following requirements:
- Python 3.6 or higher
- tqdm library

You can install tqdm library by running the following command in your terminal:

pip install tqdm


## Usage
1. Insert `message_x.json` files downloaded from Facebook after exporting user data to the `in/` folder. Ideally, one chat thread at a time.
2. Rename the output files in `batch_decoder.py` accordingly.
3. Run `decoder_py`.

## How does it work
### `decoder_very_fast.py`
This script is a decoder that reads a file with special characters and converts them to readable characters. It extends the `io.FileIO` class and overrides the `read` method to replace Unicode escape sequences with actual characters.

### `combine_json_files`
This script combines multiple JSON files into one. It loops through all the `.json` files in a folder and appends their contents to a single dictionary, which is then dumped into an output file.

### `convert_timestamps`
This script converts the `timestamp_ms` field in each message to a more readable timestamp format. It reads a JSON file, converts the timestamps in its messages, sorts the messages by timestamp, and writes the updated JSON file to an output file.

### `batch_decoder.py`
This script reads all the `.json` files in a folder, decodes special characters, and writes each message to a separate file in a different folder. It first calculates the total number of messages in the input directory and updates the progress bar accordingly. Then, for each `.json` file, it loads the messages, processes each message, and writes it to an output file. The `FacebookIO` class is used to decode special characters.

# README

## Why should you use this?
When you export your personal data from Facebook/Instagram, you will see that the encoding of the .json messages is not human-readable. This script combines and decodes the messages to a human-friendly format, making it easier to read and understand your message history.
## Installation
To run this script, you will need Python 3.6 or higher and the tqdm library installed. You can install the tqdm library by running the following command in your terminal:

pip install tqdm


## Usage
1. To extract your personal data from Facebook or Instagram, log in to your account and go to the settings page. From there, select "Download Your Information" and follow the prompts to generate a data file. Extract the messages folder from the downloaded data by navigating to the Messages folder within the data file and copying it to a separate location.

2. Download this repository.

3. Create in/ folder in the root of the repository.

4. Copy the message_x.json files you want to decode to the in/ folder located in the root of the repository. Ideally, only one chat thread should be copied at a time.

5. Create an out/ folder in the same location as the in/ folder.

6. Run the decoder_py script from the repository. This script should be able to decode the message_x.json files located in the in/ folder and output the decoded messages as one file in the out/ folder.

7. Repeat the process by copying another conversation file into the in/ folder and running the decoder_py script to decode the messages.


## How does it work
The decoder_py script uses three functions to combine, decode, and write the messages to separate files.

### `combine_and_convert_json_files`
This function combines multiple JSON files into one, converts the timestamp_ms field in each message to a human-readable format, sorts the messages by timestamp, and writes the updated JSON file to the out/ folder.

### `batch_decoder.py`
This script reads the combined and decoded .json file in the out/ folder, and writes each message to a separate file in the out/decoded/ folder. It first calculates the total number of messages in the input file and updates the progress bar accordingly. Then, it loads the messages, decodes special characters, and writes each message to an output file.

### `FacebookIO`
The FacebookIO class is used to decode special characters in the JSON messages. It extends the io.FileIO class and overrides the read method to replace Unicode escape sequences with actual characters.

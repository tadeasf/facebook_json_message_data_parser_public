import os
import io
import json
from decoder_very_fast import FacebookIO
from tqdm import tqdm
from datetime import datetime


def combine_json_files(input_folder, output_file):
    combined_json = {
        "participants": [],
        "messages": [],
        "title": "",
        "is_still_participant": True,
        "thread_path": "",
        "magic_words": []
    }

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                combined_json["participants"] = data["participants"]
                combined_json["messages"].extend(data["messages"])
                combined_json["title"] = data["title"]
                combined_json["is_still_participant"] = data["is_still_participant"]
                combined_json["thread_path"] = data["thread_path"]
                combined_json["magic_words"] = data["magic_words"]

    with open(output_file, "w") as outfile:
        json.dump(combined_json, outfile, indent=4)


def convert_timestamps(input_path, output_path):
    # Load the JSON file
    with open(input_path, 'r') as f:
        data = json.load(f)

    # Get the messages list from the data
    messages = data['messages']

    # Loop through each message and convert the timestamp
    for message in messages:
        timestamp_ms = message.get('timestamp_ms')
        if timestamp_ms:
            timestamp = datetime.fromtimestamp(
                timestamp_ms/1000).strftime('%H:%M %d/%m/%Y')
            message['timestamp'] = timestamp
            del message['timestamp_ms']

    # Sort the messages by timestamp
    messages_sorted = sorted(messages, key=lambda x: datetime.strptime(
        x['timestamp'], '%H:%M %d/%m/%Y'))

    # Update the messages list in the data
    data['messages'] = messages_sorted

    # Write the new JSON file
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)


input_folder = 'in/'  # folder with json files
output_file = 'out/output.json'  # output file, rename it to your name
combine_json_files(input_folder, output_file)
input_path = 'out/output.json'  # output file from combine_json_files
output_path = 'out2/output_time.json'  # output file with timestamps
convert_timestamps(input_path, output_path)
input_dir = 'out2/'  # folder with json files
output_dir = 'out3/'  # folder with json files with fixed encoding
for filename in tqdm(os.listdir(input_dir), desc="Processing files in the input directory"):
    if filename.endswith(".json"):
        # Load the data from each file using the FacebookIO decoder
        with FacebookIO(os.path.join(input_dir, filename), 'rb') as f:
            d = json.load(f)

        # Save the data to a file in the output directory
        with io.open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
            f.write(json.dumps(d, ensure_ascii=False, indent=4))

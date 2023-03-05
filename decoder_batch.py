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

    file_list = [filename for filename in os.listdir(
        input_folder) if filename.endswith(".json")]

    with tqdm(total=len(file_list), desc="Combining JSON files") as pbar:
        for filename in file_list:
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                combined_json["participants"] = data["participants"]
                combined_json["messages"].extend(data["messages"])
                combined_json["title"] = data["title"]
                combined_json["is_still_participant"] = data["is_still_participant"]
                combined_json["thread_path"] = data["thread_path"]
                combined_json["magic_words"] = data["magic_words"]
            pbar.update(1)

    with open(output_file, "w") as outfile:
        json.dump(combined_json, outfile, indent=4)
    print(f"JSON files combined successfully. Output file: {output_file}")


def convert_timestamps(input_path, output_path):
    # Load the JSON file
    with open(input_path, 'r') as f:
        data = json.load(f)

    # Get the messages list from the data
    messages = data['messages']

    with tqdm(total=len(messages), desc="Converting timestamps") as pbar:
        # Loop through each message and convert the timestamp
        for message in messages:
            timestamp_ms = message.get('timestamp_ms')
            if timestamp_ms:
                timestamp = datetime.fromtimestamp(
                    timestamp_ms/1000).strftime('%H:%M %d/%m/%Y')
                message['timestamp'] = timestamp
                del message['timestamp_ms']
            pbar.update(1)

        # Sort the messages by timestamp
        messages_sorted = sorted(messages, key=lambda x: datetime.strptime(
            x['timestamp'], '%H:%M %d/%m/%Y'))

    # Update the messages list in the data
    data['messages'] = messages_sorted

    # Write the new JSON file
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Timestamps converted successfully. Output file: {output_path}")


input_folder = 'in/'  # folder with json files
output_file = 'out/output.json'  # output file, rename it to your name
combine_json_files(input_folder, output_file)
input_path = 'out/output.json'  # output file from combine_json_files
output_path = 'out2/output_time.json'  # output file with timestamps
convert_timestamps(input_path, output_path)
input_dir = 'out2/'  # folder with json files
output_dir = 'out3/'  # folder with json files with fixed encoding
num_messages = 0

# Get the total number of messages in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        with FacebookIO(os.path.join(input_dir, filename), 'rb') as f:
            d = json.load(f)
            num_messages += len(d["messages"])

# Update tqdm to display progress based on the number of messages
with tqdm(total=num_messages, desc="Processing messages in the input directory") as pbar:
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            with FacebookIO(os.path.join(input_dir, filename), 'rb') as f:
                d = json.load(f)
                for message in d["messages"]:
                    # Process each message here
                    # Save the data to a file in the output directory
                    with io.open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
                        f.write(json.dumps(message, ensure_ascii=False, indent=4))
                    pbar.update(1)

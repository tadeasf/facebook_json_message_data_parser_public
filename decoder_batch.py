import os
import io
import json
from decoder_very_fast import FacebookIO
from tqdm import tqdm
from datetime import datetime


def combine_and_convert_json_files(input_folder, output_file):
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

    with tqdm(total=len(file_list), desc="Combining and converting JSON files") as pbar:
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

    # Convert timestamps and sort the messages by timestamp
    messages = combined_json['messages']
    with tqdm(total=len(messages), desc="Converting timestamps") as pbar:
        for message in messages:
            timestamp_ms = message.get('timestamp_ms')
            if timestamp_ms:
                timestamp = datetime.fromtimestamp(
                    timestamp_ms/1000).strftime('%H:%M %d/%m/%Y')
                message['timestamp'] = timestamp
                del message['timestamp_ms']
            pbar.update(1)

        messages_sorted = sorted(messages, key=lambda x: datetime.strptime(
            x['timestamp'], '%H:%M %d/%m/%Y'))

    combined_json['messages'] = messages_sorted

    # Write the new JSON file to the output directory
    with open(os.path.join('out', output_file), "w") as outfile:
        json.dump(combined_json, outfile, indent=4)

    print(
        f"JSON files combined and timestamps converted successfully. Output file: {output_file}")

    # Decode the updated file and overwrite the original file
    with FacebookIO(os.path.join('out', output_file), 'rb') as f:
        d = json.load(f)
        num_messages = len(d["messages"])
        with tqdm(total=num_messages, desc="Processing messages in the input file") as pbar:
            with io.open(os.path.join('out', output_file), 'w', encoding='utf-8') as f_out:
                for message in d["messages"]:
                    # Process each message here
                    f_out.write(json.dumps(
                        message, ensure_ascii=False, indent=4) + '\n')
                    pbar.update(1)

    print(
        f"Messages processed and updated file overwritten successfully. Output file: {output_file}")


input_folder = 'in/'  # folder with json files
output_file = 'output.json'  # output file, rename it to your name
combine_and_convert_json_files(input_folder, output_file)

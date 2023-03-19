import os
import io
import json
from decoder_very_fast import FacebookIO
from tqdm import tqdm
from datetime import datetime


def rename_output_file(output_file):
    with open(os.path.join('out', output_file), 'r') as f:
        data = json.load(f)
        first_participant_name = data['participants'][0]['name']
        new_output_file = first_participant_name + '.json'
        os.rename(os.path.join('out', output_file),
                  os.path.join('out', new_output_file))
    print(f"Output file renamed to {new_output_file}")


def find_matching_files(file_list, participants):
    matching_files = []
    for filename in file_list:
        with open(filename, 'r') as f:
            data = json.load(f)
            if set((p["name"] for p in data["participants"])) == set(participants):
                matching_files.append(filename)
    return matching_files


def combine_and_convert_json_files(input_folder, output_file, participants):
    combined_json = {
        "participants": [],
        "messages": [],
        "title": "",
        "is_still_participant": True,
        "thread_path": "",
        "magic_words": []
    }

    file_list = find_matching_files([os.path.join(input_folder, filename) for filename in os.listdir(
        input_folder) if filename.endswith(".json")], participants)

    with tqdm(total=len(file_list), desc="Combining and converting JSON files") as pbar:
        for i, filename in enumerate(file_list):
            file_path = filename  # Updated line
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                if i == 0:
                    combined_json["participants"] = data["participants"]
                    combined_json["title"] = data["title"]
                    combined_json["is_still_participant"] = data["is_still_participant"]
                    combined_json["thread_path"] = data["thread_path"]
                    combined_json["magic_words"] = data["magic_words"]
                combined_json["messages"].extend(data["messages"])
            pbar.update(1)

    messages = combined_json['messages']
    with tqdm(total=len(messages), desc="Converting timestamps") as pbar:
        for message in messages:
            timestamp_ms = message.get('timestamp_ms')
            if timestamp_ms:
                timestamp = datetime.fromtimestamp(
                    timestamp_ms/1000).strftime('%H:%M %d/%m/%Y')
                message['timestamp'] = timestamp
            pbar.update(1)

    combined_json['messages'] = sorted(
        combined_json['messages'], key=lambda x: datetime.strptime(x['timestamp'], '%H:%M %d/%m/%Y'))

    with open(os.path.join('out', output_file), "w") as outfile:
        json.dump(combined_json, outfile, indent=4)

    print(
        f"JSON files combined and timestamps converted successfully. Output file: {output_file}")

    with FacebookIO(os.path.join('out', output_file), 'rb') as f:
        d = json.load(f)
        num_messages = len(d["messages"])
        combined_json = {
            "participants": d["participants"],
            "messages": d["messages"],
            "title": d["title"],
            "is_still_participant": d["is_still_participant"],
            "thread_path": d["thread_path"],
            "magic_words": d["magic_words"]
        }
        with tqdm(total=num_messages, desc="Processing messages in the input file") as pbar:
            with io.open(os.path.join('out', output_file), 'w', encoding='utf-8') as f_out:
                json.dump(combined_json, f_out, ensure_ascii=False, indent=4)
                pbar.update(1)

    print(
        f"Messages processed and updated file overwritten successfully. Output file: {output_file}")


def process_unique_participants(input_folder):
    processed_participants = set()
    file_list = [os.path.join(input_folder, filename) for filename in os.listdir(
        input_folder) if filename.endswith(".json")]

    with open("error_log.txt", "w") as log_file:
        for filename in file_list:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                    participants = frozenset(p["name"]
                                             for p in data["participants"])

                    if participants not in processed_participants:
                        processed_participants.add(participants)
                        output_file = '_'.join(participants) + '.json'
                        combine_and_convert_json_files(
                            input_folder, output_file, participants)
                        rename_output_file(output_file)
            except Exception as e:
                log_file.write(f"Error processing file {filename}: {str(e)}\n")
                print(
                    f"Error processing file {filename}: {str(e)}. Check error_log.txt for details.")


input_folder = 'in/'
process_unique_participants(input_folder)

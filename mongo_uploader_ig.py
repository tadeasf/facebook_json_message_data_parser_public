import os
import json
from datetime import datetime
from pymongo import MongoClient


def convert_timestamp(timestamp_ms):
    return datetime.fromtimestamp(timestamp_ms/1000).strftime('%H:%M %d/%m/%Y')


def process_output_json_files(output_folder, client):
    db = client.messages
    output_files = [os.path.join(output_folder, filename) for filename in os.listdir(
        output_folder) if filename.endswith(".json")]

    for output_file in output_files:
        with open(output_file, "r") as f:
            data = json.load(f)
            messages = data["messages"]

            # Prepare messages for insertion
            for message in messages:
                if "timestamp_ms" in message:
                    message["timestamp"] = convert_timestamp(
                        message["timestamp_ms"])
                    # Keep timestamp_ms as Int64 UNIX timestamp
                    message["timestamp_ms"] = int(message["timestamp_ms"])

            # Drop existing collection and create a new one
            collection_name = os.path.splitext(
                os.path.basename(output_file))[0] + "_ig"
            if collection_name in db.list_collection_names():
                db[collection_name].drop()
                print(f"Dropped existing collection {collection_name}")

            # Insert the messages into the new collection
            collection = db[collection_name]
            collection.insert_many(messages)
            print(f"Inserted messages into collection {collection_name}")


# Connect to the MongoDB instance
mongo_uri = "mongodb+srv://tadeasf:argonek01@messagecluster.bz1vdpr.mongodb.net/test"
client = MongoClient(mongo_uri)

# Process the output JSON files
output_folder = "out/"
process_output_json_files(output_folder, client)

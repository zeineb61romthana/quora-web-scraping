import json
import os

# Directory containing the JSON files
directory = "C:\\Users\\me\\OneDrive\\Bureau\\SPORTIFY_AI\\DATASETS\\JSON\\Quora_Web_Scraping\\quora_workout_json"

# List to store data from all JSON files
all_data = []

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as json_file:
            data = json.load(json_file)
            all_data.append(data)

# Output file for concatenated data
output_file = 'combined_data.json'

# Save the combined data into a new JSON file
with open(output_file, 'w') as outfile:
    json.dump(all_data, outfile, indent=4)

print(f"All JSON files have been concatenated into {output_file}.")

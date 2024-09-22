import json

# Load your dataset
with open("C:\\Users\\me\\OneDrive\\Bureau\\SPORTIFY_AI\\DATASETS\\JSON\\Quora_Web_Scraping\\combined_data.json") as f:
    data = json.load(f)

# Create question-answer pairs
qa_pairs = []
for item in data:
    question = item['question']
    for answer in item['answers']:
        qa_pairs.append({"question": question, "answer": answer['text']})
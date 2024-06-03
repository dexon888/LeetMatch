import json
import os
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

# Define the path to the data and models folders
data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
models_folder = os.path.join(os.path.dirname(__file__), '..', 'models')
os.makedirs(models_folder, exist_ok=True)

# Load the tagged solutions from the JSON file
tagged_json_file_path = os.path.join(data_folder, 'tagged_solutions.json')
with open(tagged_json_file_path, 'r', encoding='utf-8') as f:
    tagged_solutions = json.load(f)

# Convert the JSON objects back to TaggedDocument format


def dict_to_tagged_document(doc_dict):
    return TaggedDocument(words=doc_dict['words'], tags=doc_dict['tags'])


tagged_data = [dict_to_tagged_document(doc) for doc in tagged_solutions]

# Train the Doc2Vec model with hyperparameter tuning
model = Doc2Vec(tagged_data, vector_size=200, window=8,
                min_count=2, epochs=50, workers=4)

# Save the trained model for later use
refined_model_path = os.path.join(
    models_folder, 'refined_leetcode_doc2vec.model')
refined_tuned_model_path = os.path.join(
    models_folder, 'refined_leetcode_doc2vec_tuned.model')

model.save(refined_model_path)
model.save(refined_tuned_model_path)

print(f"Doc2Vec model trained and saved as {refined_model_path} and {refined_tuned_model_path}")

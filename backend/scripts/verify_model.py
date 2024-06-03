import json
import os
from gensim.models import Doc2Vec
import nltk

# Ensure NLTK punkt is downloaded
nltk.download('punkt', quiet=True)

# Define the path to the models and data folders
models_folder = os.path.join(os.path.dirname(__file__), '..', 'models')
data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')

# Load the trained Doc2Vec model
model_path = os.path.join(models_folder, 'refined_leetcode_doc2vec.model')
model = Doc2Vec.load(model_path)

# Load the tagged solutions from the JSON file
tagged_json_file_path = os.path.join(data_folder, 'tagged_solutions.json')
with open(tagged_json_file_path, 'r', encoding='utf-8') as f:
    tagged_solutions = json.load(f)

# Convert the JSON objects back to TaggedDocument format


def dict_to_tagged_document(doc_dict):
    return {'words': doc_dict['words'], 'tags': doc_dict['tags']}


tagged_data = [dict_to_tagged_document(doc) for doc in tagged_solutions]

# Helper function to find similar problems


def find_similar_problems(input_solution, top_n=5):
    input_vector = model.infer_vector(
        nltk.word_tokenize(input_solution.lower()))
    similar_docs = model.dv.most_similar([input_vector], topn=top_n)
    return [{'problem_name': doc_id, 'similarity': similarity} for doc_id, similarity in similar_docs]


# Example input solution to test the model
input_solution = """
class Solution:
    def updateMatrix(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if not matrix[i][j]:
                    continue
                matrix[i][j] = float("inf")
                if i > 0:
                    matrix[i][j] = min(matrix[i][j], matrix[i-1][j]+1)
                if j > 0:
                    matrix[i][j] = min(matrix[i][j], matrix[i][j-1]+1)
        for i in reversed(range(len(matrix))):
            for j in reversed(range(len(matrix[i]))):
                if not matrix[i][j]:
                    continue
                if i < len(matrix)-1:
                    matrix[i][j] = min(matrix[i][j], matrix[i+1][j]+1)
                if j < len(matrix[i])-1:
                    matrix[i][j] = min(matrix[i][j], matrix[i][j+1]+1)
        return matrix
"""

# Find and print similar problems
similar_problems = find_similar_problems(input_solution)
print("Input Solution:")
print(input_solution)
print("\nSimilar Problems:")
for problem in similar_problems:
    print(f"Problem Name: {problem['problem_name']
                           }, Similarity: {problem['similarity']}")

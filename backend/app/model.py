from gensim.models import Doc2Vec
import nltk
import json
import os
from .utils import tokenize_code

nltk.download('punkt', quiet=True)

# Load the trained Doc2Vec model
model = Doc2Vec.load("models/refined_leetcode_doc2vec.model")

# Define the path to the data folder
data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')

# Load the solutions dataset
json_file_path = os.path.join(data_folder, 'leetcode_solutions.json')
with open(json_file_path, 'r', encoding='utf-8') as f:
    solutions = json.load(f)


def find_solution_by_problem_name(problem_name):
    for solution in solutions:
        if solution['problem_name'] == problem_name:
            return solution['solution']
    return None


def find_similar_problems(problem_name, top_n=5):
    try:
        solution = find_solution_by_problem_name(problem_name)
        if not solution:
            raise ValueError(
                f"Solution for problem '{problem_name}' not found")

        tokens = tokenize_code(solution)
        print(f"Tokenized input solution: {tokens}")
        input_vector = model.infer_vector(tokens)
        print(f"Inferred vector for input solution: {input_vector}")
        similar_docs = model.dv.most_similar([input_vector], topn=top_n)
        return [{'problem_name': doc_id, 'similarity': similarity} for doc_id, similarity in similar_docs]
    except Exception as e:
        print(f"Error in find_similar_problems: {e}")
        raise e


def get_problem_vector(problem_name):
    try:
        idx = model.dv.key_to_index[problem_name]
        return model.dv[idx].tolist()
    except KeyError:
        raise ValueError(f"Vector for problem '{problem_name}' not found")


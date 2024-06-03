import os
import json


def parse_solutions(repo_path):
    solutions = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    solution_code = f.read()
                    problem_name = file.split('.')[0]
                    solutions.append({
                        'problem_name': problem_name,
                        'solution': solution_code
                    })
    return solutions


repo_path = "../../Python"
solutions = parse_solutions(repo_path)

# Define the path to the data folder
data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(data_folder, exist_ok=True)

# Save the solutions to a JSON file in the data folder
json_file_path = os.path.join(data_folder, 'leetcode_solutions.json')
with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(solutions, f, indent=4)

print(f"Parsed {len(solutions)} solutions and saved to {json_file_path}")

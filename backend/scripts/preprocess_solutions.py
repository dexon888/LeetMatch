import json
import nltk
import ast
import re
import os
from gensim.models.doc2vec import TaggedDocument

# Ensure you have the required NLTK data
nltk.download('punkt', quiet=True)


def remove_comments_and_docstrings(source):
    """Remove comments and docstrings from the source code."""
    def replacer(match):
        s = match.group(0)
        return "" if s.startswith('/') else s
    pattern = re.compile(
        r'(?s)#.*?\n|\'\'\'.*?\'\'\'|\"\"\".*?\"\"\"|\'[^\']*\'|\"[^\"]*\"')
    return re.sub(pattern, replacer, source)


def normalize_variable_names(code):
    """Replace variable names with a generic placeholder."""
    class NormalizeNames(ast.NodeTransformer):
        def __init__(self):
            self.var_count = 0
            self.var_map = {}

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store):
                if node.id not in self.var_map:
                    self.var_map[node.id] = f'var{self.var_count}'
                    self.var_count += 1
                node.id = self.var_map[node.id]
            elif isinstance(node.ctx, ast.Load):
                node.id = self.var_map.get(node.id, node.id)
            return node

    tree = ast.parse(code)
    normalized_tree = NormalizeNames().visit(tree)
    return ast.unparse(normalized_tree)


def tokenize_code(code):
    code = remove_comments_and_docstrings(code)
    code = normalize_variable_names(code)
    tokens = []
    try:
        root = ast.parse(code)
        for node in ast.walk(root):
            if isinstance(node, ast.FunctionDef):
                tokens.append('function')
            elif isinstance(node, ast.Name):
                tokens.append(node.id)
            elif isinstance(node, ast.Str):
                tokens.append('str')
            elif isinstance(node, ast.Num):
                tokens.append('num')
            elif isinstance(node, ast.arg):
                tokens.append('arg')
            elif isinstance(node, ast.Attribute):
                tokens.append(node.attr)
            elif isinstance(node, ast.Call):
                tokens.append('call')
            elif isinstance(node, ast.BinOp):
                tokens.append('binop')
            # Add more node types as needed
    except SyntaxError:
        pass
    return tokens


# Define the path to the data folder
data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(data_folder, exist_ok=True)

# Load the solutions from the JSON file
json_file_path = os.path.join(data_folder, 'leetcode_solutions.json')
with open(json_file_path, 'r', encoding='utf-8') as f:
    solutions = json.load(f)

# Tokenize and tag the solutions using advanced tokenization
tagged_data = [TaggedDocument(words=tokenize_code(solution['solution']), tags=[
                              solution['problem_name']]) for solution in solutions]

# Convert TaggedDocument objects to serializable format


def tagged_document_to_dict(doc):
    return {'words': doc.words, 'tags': doc.tags}


tagged_data_serializable = [
    tagged_document_to_dict(doc) for doc in tagged_data]

# Save the tagged data to a file for later use
tagged_json_file_path = os.path.join(data_folder, 'tagged_solutions.json')
with open(tagged_json_file_path, 'w', encoding='utf-8') as f:
    json.dump(tagged_data_serializable, f, indent=4)

print(f"Preprocessed {len(tagged_data)} solutions and saved to {tagged_json_file_path}")

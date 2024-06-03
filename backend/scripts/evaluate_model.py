import json
import os
import re
import ast
import nltk
from gensim.models import Doc2Vec
from sklearn.metrics import precision_score, recall_score, f1_score

# Ensure NLTK punkt is downloaded
nltk.download('punkt', quiet=True)

# Load the trained Doc2Vec model
model = Doc2Vec.load("refined_leetcode_doc2vec.model")


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


def find_similar_problems(input_solution, top_n=5):
    tokens = tokenize_code(input_solution)
    input_vector = model.infer_vector(tokens)
    similar_docs = model.dv.most_similar([input_vector], topn=top_n)
    return [{'problem_name': doc_id, 'similarity': similarity} for doc_id, similarity in similar_docs]


# Extract problems from the Python folder
python_folder = 'path/to/LeetCode-Solutions/Python'
problems = []

for root, dirs, files in os.walk(python_folder):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                solution_code = f.read()
                # Assuming the file name is the problem name
                problem_name = file.split('.')[0]
                problems.append({'problem_name': problem_name,
                                'solution': solution_code})

# Manually define similar problems (this should be expanded based on known similar problems)
validation_data = [
    {
        'input': '''
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
''',
        'expected': ['01-matrix', 'update-matrix']
    },
    {
        'input': '''
class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []
''',
        'expected': ['two-sum']
    },
    {
        'input': '''
class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = ''.join(char.lower() for char in s if char.isalnum())
        return s == s[::-1]
''',
        'expected': ['valid-palindrome', 'palindrome']
    },
    # Add more validation examples based on the problems extracted
]

precision_scores = []
recall_scores = []
f1_scores = []

for item in validation_data:
    similar_problems = find_similar_problems(item['input'])
    predicted = [problem['problem_name'] for problem in similar_problems]
    expected = item['expected']

    # Convert to binary format for evaluation
    y_true = [1 if prob in expected else 0 for prob in predicted]
    y_pred = [1] * len(predicted)  # Model predicts all as relevant

    if len(y_true) > 0:  # Avoid empty cases
        precision_scores.append(precision_score(
            y_true, y_pred, average='macro', zero_division=1))
        recall_scores.append(recall_score(
            y_true, y_pred, average='macro', zero_division=1))
        f1_scores.append(
            f1_score(y_true, y_pred, average='macro', zero_division=1))

print(f"Average Precision: {sum(precision_scores)/len(precision_scores):.4f}")
print(f"Average Recall: {sum(recall_scores)/len(recall_scores):.4f}")
print(f"Average F1-Score: {sum(f1_scores)/len(f1_scores):.4f}")

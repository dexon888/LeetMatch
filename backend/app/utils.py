import re
import ast


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
    try:
        code = remove_comments_and_docstrings(code)
        code = normalize_variable_names(code)
        tokens = []
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
        print(f"Tokenized code: {tokens}")
        return tokens
    except SyntaxError as e:
        print(f"Syntax error while parsing code: {e}")
        return []
    except Exception as e:
        print(f"Error in tokenize_code: {e}")
        return []

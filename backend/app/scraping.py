import re


def extract_problem_name(url):
    match = re.search(r'/problems/([^/]+)/', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Could not extract problem name from URL")

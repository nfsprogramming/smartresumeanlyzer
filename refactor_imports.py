
import os
import re

def refactor_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    # Replace 'from utils.' -> 'from app_utils.'
    new_content = re.sub(r'(^|\s)from utils\.', r'\1from app_utils.', new_content)
    # Replace 'import utils.' -> 'import app_utils.'
    new_content = re.sub(r'(^|\s)import utils\.', r'\1import app_utils.', new_content)
    # Replace 'from utils import' -> 'from app_utils import'
    new_content = re.sub(r'(^|\s)from utils import', r'\1from app_utils import', new_content)
    # Replace 'import utils' at end of line or before space
    new_content = re.sub(r'(^|\s)import utils(\s|$)', r'\1import app_utils\2', new_content)

    if content != new_content:
        print(f"Updating {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

for root, dirs, files in os.walk("."):
    if ".git" in root or "__pycache__" in root or ".streamlit" in root:
        continue
    for file in files:
        if file.endswith(".py"):
            refactor_file(os.path.join(root, file))

print("Refactoring complete.")

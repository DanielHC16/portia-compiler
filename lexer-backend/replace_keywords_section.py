#!/usr/bin/env python3
"""Replace the keyword FSA section in portia_lexer.py with the generated one"""

# Read the generated keyword FSA
with open('keywords_fsa_output.txt', 'r', encoding='utf-8') as f:
    new_keywords_fsa = f.read()

# Read the current lexer file
with open('app/lexer/portia_lexer.py', 'r', encoding='utf-8') as f:
    lexer_lines = f.readlines()

# Find the start and end lines
start_line = None
end_line = None

for i, line in enumerate(lexer_lines):
    if 'case \'s1\':' in line and start_line is None:
        start_line = i
    if '# OPERATORS AND RESERVED SYMBOLS FSA' in line and start_line is not None:
        end_line = i - 2  # Two lines before (to exclude the blank line and comment separator)
        break

if start_line is None or end_line is None:
    print(f"ERROR: Could not find section boundaries")
    print(f"start_line: {start_line}, end_line: {end_line}")
    exit(1)

print(f"Replacing lines {start_line+1} to {end_line+1}")
print(f"Old section: {end_line - start_line + 1} lines")
print(f"New section: {len(new_keywords_fsa.splitlines())} lines")

# Replace the section
new_lines = (
    lexer_lines[:start_line] + 
    [new_keywords_fsa if not new_keywords_fsa.endswith('\n') else new_keywords_fsa] +
    ([] if new_keywords_fsa.endswith('\n') else ['\n']) +
    ['\n'] +  # Add blank line before OPERATORS section
    lexer_lines[end_line+1:]
)

# Write the updated file
with open('app/lexer/portia_lexer.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Replacement complete!")


import sys


if len(sys.argv) < 2:
    print("Usage: python format_markdown.py <target_file>")
    exit(1)

target_file = sys.argv[1]

with open(target_file, 'r', encoding='utf-8') as file:
    content = file.readlines()

start_line_index = None
for i, line in enumerate(content):
    if line.startswith('## Day') and '-' in line:
        start_line_index = i
        break

if start_line_index is None:
    print('All formatted, no changes made.')
    exit(1)
print(f"Start processing from line {start_line_index}")
new_content = []
for i, line in enumerate(content):
    if i < start_line_index:
        new_content.append(line)
        continue
    if line.startswith('## Day') and '-' in line:
        day_string, title = line.split(
            '-')[0].strip(), line.split('-')[1].strip()
        if f'{day_string}\n' not in new_content:
            new_content.append(f'{day_string}\n')
            new_content.append('\n')
        new_content.append(f'### {title}\n')
    elif line.startswith('##'):
        content = line.split(" ", 1)
        if 'python Code Sample' in content[1]:
            continue
        new_content.append(f'#### {content[1]}')
    else:
        new_content.append(line)

with open(target_file, 'w', encoding='utf-8') as file:
    file.writelines(new_content)

from typing import List, Dict

def parse_markdown_table(file_path: str) -> List[Dict[str, str]]:
    """
    Parses the first markdown table in a file.
    Returns a list of dicts, the first row is assumed to be headers.
    """
    table_lines = []
    in_table = False

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('|') and '|' in line[1:]:
                table_lines.append(line)
                in_table = True 
            elif in_table and line == "":
                # empty line after table ends it
                break 
        
        if not table_lines:
            return []
    
    # parse headers
    header = [h.strip() for h in table_lines[0].strip('|').split('|')]

    # parse rows
    rows = []
    for row_line in table_lines[1:]:
        # skip separator lines like |---|---|---|
        # print(set(row_line.strip()))
        if set(row_line.strip()) <= {'|', '-', ':', ' '}:
            continue 

        row_values = [v.strip() for v in row_line.strip('|').split('|')]
        # pad missing columns
        while len(row_values) < len(header):
            row_values.append('')
        row_dict = dict(zip(header, row_values))
        rows.append(row_dict)
    
    return rows

if __name__ == '__main__':
    from git_utils import pull_and_check
    pull_and_check()
    rows = parse_markdown_table('../data/notes/Databases/Currently Working On.md')
    print(rows, len(rows))
import json 
f = open('keyboard-layout.json', 'r')
json_dict = json.load(f)
new_json_dict = []
for row_index, row in enumerate(json_dict):
    col_index = 0 
    new_row = []
    for data in row:
        if isinstance(data, dict):
            new_row.append(data)
        else:
            new_row.append(f"{row_index},{col_index}")
            col_index += 1
    new_json_dict.append(new_row)
with open('keyboard-layout-indexed.json', 'w') as f:
    json.dump(new_json_dict, f, indent=2)
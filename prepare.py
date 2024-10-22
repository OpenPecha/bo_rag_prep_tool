from pathlib import Path

text = Path("four_truths.txt").read_text(encoding="utf-8")

data = []

for line in text.splitlines():
    data.append(line)

data = [line for line in data if line]

json_data = []
char_count = 0
for idx, line in enumerate(data):
    curr_json_data = {}
    span = {"start": char_count, "end": len(line) + char_count}
    char_count += len(line)
    curr_json_data = {
        "span": span,
        "content": line,
        "pecha": "four_truth",
        "line_count": idx,
    }
    json_data.append(curr_json_data)


from bo_rag_prep_tool.utils import write_json

write_json("four_truth.json", json_data)

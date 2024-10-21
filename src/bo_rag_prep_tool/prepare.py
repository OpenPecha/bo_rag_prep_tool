import json
from pathlib import Path

import yaml


def write_json(data, output_path):
    with open(output_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def prepare(opf_path: Path, output_path: Path):
    book_metadata = []
    ann_files = Path(opf_path / "layers").rglob("*.yml")

    pecha_id = opf_path.name.split(".")[0]
    for ann_file in ann_files:
        with open(ann_file) as f:
            layer = yaml.load(f, Loader=yaml.FullLoader)
        # Get base
        base_path = opf_path / "base" / f"{ann_file.parent.name}.txt"
        base_content = base_path.read_text(encoding="utf-8")
        # Get annotations
        anns = layer["annotations"]
        for ann in anns.values():
            start = ann["span"]["start"]
            end = ann["span"]["end"]
            base_span = base_content[start:end]
            curr_book_metadata = {
                "pecha_id": pecha_id,
                "base": ann_file.parent.name,
                "start": start,
                "end": end,
                "content": base_span,
            }
            for k, v in ann.items():
                if k != "span":
                    curr_book_metadata[k] = v
            book_metadata.append(curr_book_metadata)

    output_path.mkdir(exist_ok=True, parents=True)
    json_output_path = output_path / f"{pecha_id}.json"
    write_json(book_metadata, json_output_path)
    return json_output_path


if __name__ == "__main__":
    opf_path = Path("I46409446.opf")
    json_file = prepare(opf_path, Path("output"))
    print(json_file)

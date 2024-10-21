from pathlib import Path

import yaml

from bo_rag_prep_tool.utils import write_json


def prepare(opf_path: Path, output_path: Path):
    book_metadata = []
    ann_files = list(Path(opf_path / "layers").rglob("*.yml"))
    ann_files = sorted(ann_files, key=lambda x: x.name)

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
    write_json(json_output_path, book_metadata)
    return json_output_path

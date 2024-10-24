from pathlib import Path
from typing import List

import fitz
import yaml

from bo_rag_prep_tool.utils import write_json


def prepare_from_opf(opf_path: Path, output_path: Path):
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


def extract_text_from_pdf_file(pdf_file_path: Path) -> List[str]:
    """Reads the content of a PDF file using PyMuPDF."""
    extracted_texts = []

    try:
        pdf_document = fitz.open(pdf_file_path)
        for no in range(len(pdf_document)):
            page = pdf_document.load_page(no)
            curr_text = page.get_text() if page.get_text() else ""
            extracted_texts.append(curr_text)
        return extracted_texts
    except Exception as e:
        print(f"Failed to read PDF file {pdf_file_path}: {e}")
        return []

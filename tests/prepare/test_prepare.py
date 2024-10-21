from pathlib import Path

from bo_rag_prep_tool.prepare import prepare
from bo_rag_prep_tool.utils import read_json


def test_prepare():
    data = Path(__file__).parent / "data"
    opf_path = data / "I46409446.opf"

    output_path = Path(__file__).parent / "output"
    json_output_path = prepare(opf_path, output_path)

    expected_output = read_json(data / "expected_output.json")

    json_output = read_json(json_output_path)
    assert len(json_output) == len(expected_output)
    for json_data in json_output:
        assert json_data in expected_output

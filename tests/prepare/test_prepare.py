import tempfile
from pathlib import Path

from bo_rag_prep_tool.prepare import prepare
from bo_rag_prep_tool.utils import read_json


def test_prepare():
    data = Path(__file__).parent / "data"
    opf_path = data / "I46409446.opf"

    with tempfile.TemporaryDirectory() as tmpdirname:

        output_path = Path(tmpdirname)
        json_output_path = prepare(opf_path, output_path)

        expected_output = data / "expected_output.json"
        assert read_json(json_output_path) == read_json(expected_output)

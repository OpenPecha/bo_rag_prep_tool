import tempfile
from pathlib import Path

from bo_rag_prep_tool.prepare import prepare_from_opf
from bo_rag_prep_tool.utils import read_json


def test_prepare():
    data = Path(__file__).parent / "data"
    opf_path = data / "I46409446.opf"

    with tempfile.TemporaryDirectory() as tmpdirname:
        output_path = Path(tmpdirname)

        json_output_path = prepare_from_opf(opf_path, output_path)

        expected_output = read_json(data / "expected_output.json")

        json_output = read_json(json_output_path)
        assert len(json_output) == len(expected_output)
        for json_data in json_output:
            assert json_data in expected_output

"""
End-to-end test for check_json
"""
import subprocess

import pytest  # type:ignore


JSON = """
{
"name": "firstname lastname",
"description": "somedescription",
"email": "name@domain.tld",
"numberval": 5
}
"""
JSON_FILENAME = "input.json"


@pytest.mark.endtoend
@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            # OK
            [
                "--filter",
                "label",
                ".numberval",
                "w@0",
                "--",
            ],
            {
                "returncode": 0,
                "output": "JSONFILE OK - label is 5 | label=5;@0",
            },
        ),
        (
            # WARN
            [
                "--filter",
                "label",
                ".numberval",
                "w@5:5",
                "--",
            ],
            {
                "returncode": 1,
                "output": (
                    "JSONFILE WARNING - label is 5 (outside range @5:5) | label=5;@5:5"
                ),
            },
        ),
        (
            # CRIT
            [
                "--filter",
                "label",
                ".numberval",
                "c@5:5",
                "--",
            ],
            {
                "returncode": 2,
                "output": (
                    "JSONFILE CRITICAL - label is 5 (outside range @5:5) | "
                    "label=5;;@5:5"
                ),
            },
        ),
        (
            # CRIT override WARN
            [
                "--filter",
                "label",
                ".numberval",
                "w@5:5,c@5:5",
                "--",
            ],
            {
                "returncode": 2,
                "output": (
                    "JSONFILE CRITICAL - label is 5 (outside range @5:5) | "
                    "label=5;@5:5;@5:5"
                ),
            },
        ),
    ],
)
def test_end_to_end(test_input, expected, tmp_path):
    """Test"""
    filepath = tmp_path / JSON_FILENAME
    filepath.write_text(JSON)
    command = ["python3", "-m", "check_json"] + test_input + [str(filepath)]
    res = subprocess.run(command, capture_output=True, check=False, text=True)
    assert res.returncode == expected["returncode"]
    assert res.stdout.strip() == expected["output"]

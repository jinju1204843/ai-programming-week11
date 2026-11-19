# [NEW v11] Specification-oriented comparison example in the current chat.
# Expectations use the week11 specification, including duplicate-name retention.
# This is not a record of an independent fresh-chat experiment.
import pytest
from load_scores import load_scores


def test_valid_rows_and_duplicate_names(tmp_path):
    path = tmp_path / "normal.csv"
    path.write_text('name,score\n가,88\n가,91\n"최,네번",77\n', encoding="utf-8")
    assert load_scores(path) == ([("가", 88), ("가", 91), ("최,네번", 77)], [])


def test_blank_lines_and_header_only(tmp_path):
    path = tmp_path / "blank.csv"
    path.write_text("name,score\n\n", encoding="utf-8")
    assert load_scores(path) == ([], [])


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize("score, valid", [(-1, False), (0, True), (1, True),
                                          (99, True), (100, True), (101, False)])
def test_boundaries(tmp_path, score, valid):
    path = tmp_path / "boundary.csv"
    path.write_text(f"name,score\n가,{score}\n", encoding="utf-8")
    kept, skipped = load_scores(path)
    assert kept == ([("가", score)] if valid else [])
    assert len(skipped) == (0 if valid else 1)
    if not valid:
        assert skipped[0][0] == 2
        assert skipped[0][2]


def test_invalid_rows_are_reported_and_reading_continues(tmp_path):
    path = tmp_path / "invalid.csv"
    path.write_text("name,score\n가,\n나,결석\n,90\n다,72,비고\n라, 77\n", encoding="utf-8")
    kept, skipped = load_scores(path)
    assert kept == [("라", 77)]
    assert [entry[0] for entry in skipped] == [2, 3, 4, 5]
    assert all(entry[1] and entry[2] for entry in skipped)

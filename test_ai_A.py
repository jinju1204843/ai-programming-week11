# [NEW v11] Code-informed comparison example authored in the current chat.
# This is not a record of an independent fresh-chat experiment.
import pytest
from load_scores import load_scores


@pytest.mark.parametrize("text, kept, reason", [
    ("name,score\n가,88\n", [("가", 88)], None),
    ("name,score\n\n가,88\n", [("가", 88)], None),
    ('name,score\n"최,네번",77\n', [("최,네번", 77)], None),
    ("name,score\n", [], None),
    ("name,score\n가,0\n", [("가", 0)], None),
    ("name,score\n가,100\n", [("가", 100)], None),
    ("name,score\n가,101\n", [], "점수가 0~100 밖"),
    ("name,score\n가,\n", [], "점수가 비어 있음"),
    ("name,score\n가,결석\n", [], "점수가 정수가 아님"),
    ("name,score\n,90\n", [], "이름이 비어 있음"),
    ("name,score\n가,72,비고\n", [], "열 개수가 2가 아님"),
    ("name,score\n가,88\n가,91\n", [("가", 88), ("가", 91)], None),
])
def test_csv_rows(tmp_path, text, kept, reason):
    path = tmp_path / "case.csv"
    path.write_text(text, encoding="utf-8")
    actual, skipped = load_scores(path)
    assert actual == kept
    if reason is None:
        assert skipped == []
    else:
        assert len(skipped) == 1
        assert skipped[0][0] == 2
        assert skipped[0][2] == reason


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")

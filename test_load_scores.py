from load_scores import load_scores

#def test_정상_파일을_읽는다():
#    kept, skipped = load_scores("scores.csv")
#    assert len(kept) == 5
    
def test_일부러_틀린_테스트():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 99  

# [NEW v11] Keep the deliberate failure as a skipped demonstration.
import pytest

test_일부러_틀린_테스트 = pytest.mark.skip(
    reason="실패 시연 기록 완료. 실제 기대값은 5건"
)(test_일부러_틀린_테스트)


# [NEW v11] Valid data, blank lines, quoted names, exceptions and boundaries.
def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert kept == [("김하나", 88), ("최,네번", 77), ("김하나", 91),
                    ("윤보람", 64), ("서한별", 95)]
    assert len(skipped) == 5


def test_빈_줄은_건너뛴다(tmp_path):
    path = tmp_path / "blank.csv"
    path.write_text("name,score\n김하나,88\n\n윤보람,64\n", encoding="utf-8")
    assert load_scores(path) == ([("김하나", 88), ("윤보람", 64)], [])


def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    path = tmp_path / "comma.csv"
    path.write_text('name,score\n"최,네번",77\n', encoding="utf-8")
    assert load_scores(path) == ([("최,네번", 77)], [])


def test_없는_파일이면_오류가_난다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_헤더만_있으면_빈_결과():
    assert load_scores("empty.csv") == ([], [])


@pytest.mark.parametrize("score, valid", [(0, True), (100, True), (101, False)])
def test_점수_경계값(tmp_path, score, valid):
    path = tmp_path / "boundary.csv"
    path.write_text(f"name,score\n김하나,{score}\n", encoding="utf-8")
    kept, skipped = load_scores(path)
    if valid:
        assert kept == [("김하나", score)]
        assert skipped == []
    else:
        assert kept == []
        assert skipped == [(2, f"김하나,{score}", "점수가 0~100 밖")]


# [NEW v11] Exercise the empty-name branch identified by coverage.
def test_이름이_비면_제외한다(tmp_path):
    path = tmp_path / "no_name.csv"
    path.write_text("name,score\n,90\n", encoding="utf-8")
    assert load_scores(path) == ([], [(2, ",90", "이름이 비어 있음")])


# [NEW v11] Exercise the command-line entry point using an independent process.
def test_명령줄에서_실행한다():
    import subprocess
    import sys
    from pathlib import Path

    root = Path(__file__).parent
    result = subprocess.run(
        [sys.executable, str(root / "load_scores.py"), str(root / "scores.csv")],
        capture_output=True, text=True, encoding="utf-8",
        env=dict(__import__("os").environ, PYTHONIOENCODING="utf-8"),
    )
    assert result.returncode == 0
    assert "읽은 줄 : 5개" in result.stdout
    assert "건너뛴 줄 : 5개" in result.stdout

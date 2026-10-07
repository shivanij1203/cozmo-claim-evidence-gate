from app.evaluation import run


def test_failure_lab():
    rows = run()
    assert len(rows) == 6
    assert all(row["pass"] for row in rows)

from app.evaluation import run


if __name__ == "__main__":
    rows = run()
    for row in rows:
        status = "PASS" if row["pass"] else "FAIL"
        reason = "; ".join(row["reasons"]) or "no escalation reason"
        print(f"{status:4}  {row['scenario']:<26}  {row['actual']:<20}  {reason}")

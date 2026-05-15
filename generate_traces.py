"""Run the SQL agent on 200 sample questions and log traces to MLflow."""

import configparser
import os
import time
import mlflow

from agent import run_agent
from questions import get_questions

EXPERIMENT_ID = "4310327943608311"
PROFILE = os.environ.get("DATABRICKS_CONFIG_PROFILE", "DOGFOOD")


def _setup_auth() -> str:
    cfg = configparser.ConfigParser()
    cfg.read(os.path.expanduser("~/.databrickscfg"))
    host = cfg[PROFILE]["host"].rstrip("/")
    token = cfg[PROFILE]["token"]
    os.environ.setdefault("DATABRICKS_HOST", host)
    os.environ.setdefault("DATABRICKS_TOKEN", token)
    return host


def main():
    host = _setup_auth()

    mlflow.set_tracking_uri("databricks")
    mlflow.set_experiment(experiment_id=EXPERIMENT_ID)
    # Auto-trace OpenAI calls nested inside run_agent
    mlflow.openai.autolog()

    questions = get_questions()
    print(f"Running agent on {len(questions)} questions...")

    failed = 0
    for i, question in enumerate(questions, 1):
        try:
            result = run_agent(question)
            status = "ok"
        except Exception as e:
            result = str(e)
            status = "error"
            failed += 1

        if i % 20 == 0 or i == len(questions):
            print(f"  {i}/{len(questions)}  (errors so far: {failed})")

        # Small delay to avoid rate limiting
        time.sleep(0.2)

    print(f"\nDone. {len(questions) - failed} succeeded, {failed} failed.")
    print(f"View traces: {host}/ml/experiments/{EXPERIMENT_ID}")


if __name__ == "__main__":
    main()

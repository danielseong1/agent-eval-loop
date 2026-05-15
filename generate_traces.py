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


def _setup_uc_tracing():
    """Route traces to the UC tables backing this experiment."""
    from mlflow.entities.trace_location import UCSchemaLocation

    client = mlflow.MlflowClient()
    experiment = client.get_experiment(EXPERIMENT_ID)
    tags = experiment.tags  # already a dict

    # e.g. "ds_fs.agent_quality_demo.4310327943608311_otel_spans"
    span_table = tags.get("mlflow.experiment.databricksTraceSpanStorageTable", "")
    log_table = tags.get("mlflow.experiment.databricksTraceLogStorageTable", "")

    if not span_table:
        print("WARNING: No UC span table tag found on experiment; traces will go to MySQL.")
        return

    parts = span_table.split(".")
    catalog, schema, spans_table_name = parts[0], parts[1], parts[2]
    logs_table_name = log_table.split(".")[2] if log_table else None

    location = UCSchemaLocation(catalog_name=catalog, schema_name=schema)
    location._otel_spans_table_name = spans_table_name
    if logs_table_name:
        location._otel_logs_table_name = logs_table_name

    mlflow.tracing.set_destination(location)
    print(f"UC tracing destination: {catalog}.{schema} (spans → {spans_table_name})")


def main():
    host = _setup_auth()

    mlflow.set_tracking_uri("databricks")
    mlflow.set_experiment(experiment_id=EXPERIMENT_ID)

    # Route traces to UC tables instead of the default MySQL-backed store.
    # The experiment tags tell us the actual span table name (experiment-ID-prefixed).
    _setup_uc_tracing()

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

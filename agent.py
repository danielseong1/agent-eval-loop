import os
import mlflow
from openai import OpenAI

SYSTEM_PROMPT = """You are a SQL expert for an e-commerce analytics database.

Schema:
  orders(order_id, customer_id, product_id, quantity, amount, order_date, status)
    - status values: 'pending', 'shipped', 'delivered', 'cancelled', 'returned'
  customers(customer_id, name, email, city, country, signup_date, tier)
    - tier values: 'bronze', 'silver', 'gold', 'platinum'
  products(product_id, name, category, price, stock_quantity, supplier_id)
    - category values: 'electronics', 'clothing', 'home', 'sports', 'books'

Given a natural language question, return a single SQL query that answers it.
Return only the SQL, no markdown, no explanation."""


def get_client() -> OpenAI:
    host = os.environ.get("DATABRICKS_HOST", "https://dogfood.staging.databricks.com")
    token = os.environ["DATABRICKS_TOKEN"]
    return OpenAI(
        api_key=token,
        base_url=f"{host.rstrip('/')}/serving-endpoints",
    )


@mlflow.trace
def parse_sql(response: str) -> str:
    """Extract SQL from a ```sql ... ``` code block in the model response."""
    start = response.index("```sql") + 6
    end = response.index("```", start)
    return response[start:end].strip()


@mlflow.trace
def run_agent(question: str) -> str:
    client = get_client()
    model = os.environ.get("MODEL_NAME", "databricks-meta-llama-3-3-70b-instruct")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        max_tokens=400,
        temperature=0.4,
    )
    raw = response.choices[0].message.content
    return parse_sql(raw)

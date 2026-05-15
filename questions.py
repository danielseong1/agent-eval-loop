"""200 sample questions for the SQL agent, covering easy/medium/hard/ambiguous cases."""

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
COUNTRIES = ["United States", "Germany", "Japan", "Brazil", "United Kingdom",
             "France", "Canada", "Australia", "India", "Mexico"]
CATEGORIES = ["electronics", "clothing", "home", "sports", "books"]
TIERS = ["bronze", "silver", "gold", "platinum"]
YEARS = ["2024", "2025"]
STATUSES = ["delivered", "cancelled", "returned", "pending", "shipped"]

# Simple single-table lookups (40 questions)
SIMPLE = (
    [f"How many orders were placed in {m} {y}?" for m in MONTHS[:5] for y in YEARS[:4]]
    + [f"List all customers from {c}." for c in COUNTRIES]
    + [f"What products are in the {cat} category?" for cat in CATEGORIES]
    + [f"How many {t} tier customers do we have?" for t in TIERS]
    + [f"What is the total number of {s} orders?" for s in STATUSES]
)

# Aggregations and filtering (60 questions)
MEDIUM = [
    "What is the total revenue for each product category?",
    "Which country has the highest number of orders?",
    "What is the average order value per customer tier?",
    "List the top 10 customers by total spend.",
    "What is the monthly revenue trend for the past 12 months?",
    "Which products have never been ordered?",
    "What percentage of orders are cancelled?",
    "Find all customers who signed up in the last 30 days.",
    "What is the average time between customer signup and first order?",
    "Which product category has the highest return rate?",
    "List customers who have placed at least 5 orders.",
    "What is the revenue contribution of gold and platinum tier customers?",
    "Find the top 5 cities by total order amount.",
    "What is the stock value (price * stock_quantity) for each category?",
    "How many orders contain products from multiple categories?",
    "What is the repeat purchase rate (customers with more than 1 order)?",
    "Which day of the week has the most orders?",
    "What is the average order quantity per product?",
    "List products with stock_quantity below 10.",
    "What is the revenue per customer for platinum tier customers?",
] + [
    f"What is the total revenue from {c} customers?" for c in COUNTRIES
] + [
    f"How many orders have status '{s}' in 2025?" for s in STATUSES
] + [
    f"What is the average order value for {cat} products?" for cat in CATEGORIES
] + [
    f"List all {t} tier customers who placed an order this year." for t in TIERS
]

# Joins and complex queries (60 questions)
HARD = [
    "Find customers who bought electronics but never bought clothing.",
    "What is the revenue per supplier (join through products)?",
    "Find the most frequently bought product pair in the same order.",
    "Which customers have a higher-than-average order frequency?",
    "Calculate customer lifetime value (total spend) segmented by signup year.",
    "Find orders where the customer's tier upgraded between their first and latest order.",
    "What is the month-over-month revenue growth rate?",
    "Identify customers at churn risk (no order in last 90 days but previously active).",
    "What is the product cross-sell rate between categories?",
    "Find the top 3 products by revenue for each category.",
    "Which customers placed orders in every month of 2025?",
    "Calculate the 90-day rolling average order value per customer.",
    "Find products where the return rate exceeds 20%.",
    "What is the revenue share of each tier by country?",
    "Identify the customer cohort (by signup month) with the highest LTV.",
    "Find customers who only ever bought one product.",
    "What is the average basket size (unique products per order) by tier?",
    "Calculate the reorder rate for each product.",
    "Which cities have the highest ratio of returned orders?",
    "Find the top revenue-generating supplier.",
] + [
    f"What is the {t} tier customer retention rate in {y}?" for t in TIERS for y in YEARS
] + [
    f"Find the top 5 products by revenue in {c}." for c in COUNTRIES[:5]
] + [
    f"Calculate average order value for {cat} by country." for cat in CATEGORIES
]

# Ambiguous / tricky — intentional failure cases (40 questions)
TRICKY = [
    "What is the conversion rate?",                         # no sessions table
    "Show me the customer acquisition cost.",               # no marketing spend table
    "Calculate the net promoter score.",                    # no survey data
    "What is the churn rate this quarter?",                 # ambiguous definition
    "Show me MoM growth.",                                  # underspecified
    "How is revenue trending?",                             # vague
    "Who are our best customers?",                          # best by what metric?
    "What products should we restock?",                     # needs a threshold rule
    "Show me the sales funnel.",                            # no funnel stages
    "What is our market share?",                            # no competitor data
    "Calculate CLV.",                                       # ambiguous formula
    "Show me the ROI on marketing.",                        # no marketing table
    "Which campaigns are performing well?",                 # no campaigns table
    "What is the customer satisfaction score?",             # no ratings table
    "Show me daily active users.",                          # no session/user table
    "What is the average revenue per user?",                # ARPU — ambiguous period
    "How many users churned last month?",                   # ambiguous churn def
    "Show me the North Star metric.",                       # undefined
    "What is the payback period?",                          # no cost data
    "Forecast revenue for next quarter.",                   # no forecasting context
] + [
    f"What is the {m} revenue?" for m in MONTHS[:10]       # missing year context
] + [
    f"Show me {cat} performance." for cat in CATEGORIES    # vague "performance"
] + [
    f"Is {c} a good market?" for c in COUNTRIES[:5]       # opinion, not SQL
]


def get_questions() -> list[str]:
    questions = SIMPLE + MEDIUM + HARD + TRICKY
    # Trim/pad to exactly 200
    return questions[:200]

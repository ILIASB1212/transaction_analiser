# Transaction Intelligence

Transaction Intelligence is a Streamlit dashboard that compares a proposed transaction with a customer's spending history. It uses synthetic banking records and returns a category, amount in MAD, fraud risk score, review flag, and explanation.

## Run the dashboard

From the project root, use Python 3.14 and [uv](https://docs.astral.sh/uv/). Set a Groq API key in your environment or in a local `.env` file. Keep the key out of Git.

```dotenv
GROQ_API_KEY=your_groq_api_key
```

```powershell
uv sync --locked
uv run --locked streamlit run main.py
```

Open [the dashboard](http://localhost:8501) and try the synthetic example below.

> Customer CUST-0040 spent 150 MAD on shopping in Marrakech, Morocco.

## How dependency injection works

1. The Python app loads [the synthetic dataset](data/bank.json) into a `CustomerRecords` object. The system prompt contains instructions for the analysis, and the user message contains the transaction description.
2. The Pydantic AI agent declares `deps_type=CustomerRecords` and registers `get_customer_profile` and `get_customer_transaction_history`. The run receives the records through `deps=records`.
3. When the model requests a lookup, Pydantic AI runs the tool in the Python process. The tool reads `ctx.deps.customers` and looks up the requested ID. Groq receives the tool's returned data as a tool result, which the model uses to produce a structured `TransactionAnalysis`.

The relevant code in [main.py](main.py) is:

```python
records = CustomerRecords(customers=CUSTOMERS)

transaction_agent = Agent(
    MODEL,
    deps_type=CustomerRecords,
    output_type=TransactionAnalysis,
    tools=[get_customer_profile, get_customer_transaction_history],
    system_prompt=SYSTEM_PROMPT,
)

result = await transaction_agent.run(query, deps=records)
```

The lookup functions live in [inject_context.py](src/retriver/inject_context.py). The dependency and output types live in [Schemas.py](src/schemas/Schemas.py).

## What the model can see

| Data | Handling in this project |
| --- | --- |
| Full customer dataset | Loaded into the Python process and passed to the agent as a runtime dependency. The application leaves the dataset out of the system prompt and user message. |
| Transaction description | Sent to Groq, including the customer ID and any other details entered in the form. |
| Customer profile | Returned by the tool for the requested ID, including name, home city and country, and membership date. |
| Transaction history | Returned by the tool as the requested customer's full history of amounts, categories, cities, and countries. |

**Tool results are visible to the model.** Dependency injection controls how tools get access to the local data. The tool's return value controls what leaves the application.

## Handling real customer data

The current tools are intended for synthetic data. For a real deployment, authenticate the caller and authorize each customer lookup in Python before retrieving records. Use the caller's authenticated identity for the access check, even if the model supplies a customer ID. Dependency injection provides access to the records and does not enforce authorization.

If policy permits sending a summary to the provider, compute it locally and return only the fields needed for the decision. For example, a tool could return the customer's usual amount range for the category and whether the transaction country appears in their history. Keep names, raw transaction rows, and account identifiers out of both the submitted description and tool responses.

If customer data must stay entirely outside the LLM, run the comparison and scoring in local code and render the explanation in Streamlit from that local result. In that setup, the transaction description, identifiers, history, and customer-derived findings stay in the application.


import pydantic_ai


from pydantic_ai import RunContext   
from src.schemas.Schemas import CustomerRecords, TransactionAnalysis


def get_customer_profile(ctx: RunContext[CustomerRecords], 
                        customer_id: str) -> dict:
    """Look up a customer's profile (name, home city/country, member since) by customer_id."""
    customer = ctx.deps.customers.get(customer_id)
    if not customer:
        return {"error": f"No customer found with id {customer_id}"}
    return {k: v for k, v in customer.items() if k != "transactions"}



def get_customer_transaction_history(ctx: RunContext[CustomerRecords], 
                            customer_id: str) -> list:
    """Return a customer's past transactions 
    (city, country, category, amount) by customer_id."""
    customer = ctx.deps.customers.get(customer_id)
    if not customer:
        return [{"error": f"No customer found with id {customer_id}"}]
    return customer["transactions"]
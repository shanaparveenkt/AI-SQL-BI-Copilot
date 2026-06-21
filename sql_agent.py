import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_sql(user_question):
    prompt = f"""
You are an expert MySQL assistant.

Database name: shopsphere

Tables and columns:

customers(
    customer_id,
    customer_name,
    gender,
    age,
    city,
    state,
    country,
    join_date
)

products(
    product_id,
    product_name,
    category,
    price,
    cost_price,
    stock
)

sellers(
    seller_id,
    seller_name,
    city,
    state,
    country,
    seller_rating
)

orders(
    order_id,
    customer_id,
    order_date,
    order_status,
    city,
    state,
    country
)

order_items(
    order_item_id,
    order_id,
    product_id,
    seller_id,
    quantity
)

payments(
    payment_id,
    order_id,
    payment_type,
    payment_value
)

reviews(
    review_id,
    order_id,
    rating,
    review_text
)

delivery(
    delivery_id,
    order_id,
    delivery_days,
    delivery_status,
    shipping_cost
)

fact_sales(
    order_id,
    product_id,
    customer_id,
    quantity,
    sales_amount,
    shipping_cost,
    rating
)

Rules:
1. Return only valid MySQL SQL query.
2. Do not explain.
3. Do not use markdown.
4. Only return SQL.
5. Always use meaningful aliases.
6. Use ORDER BY DESC when user asks for top/best/highest.
7. Use LIMIT when user asks top N.

Convert this question into SQL:
{user_question}
"""

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0
)

    return response.choices[0].message.content
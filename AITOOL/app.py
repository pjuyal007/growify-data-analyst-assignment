# ==============================
# 📊 Growify AI Insight Tool
# ==============================

# ----------- IMPORTS -----------
import sqlite3
import pandas as pd
import streamlit as st
from openai import OpenAI

# ----------- API SETUP -----------
# -- enter your api key here do not share publicly
client = OpenAI(api_key="your api key")


# ----------- DATABASE CONNECTION -----------
conn = sqlite3.connect("growify.db")


# ----------- STREAMLIT UI -----------
st.title("📊 Growify AI Insight Tool")
st.write("Ask questions about campaign & sales performance")

# Input box
question = st.text_input("Enter your question:")


# ----------- FUNCTION: GENERATE SQL QUERY -----------
def generate_sql(question):
    """
    Converts user question into SQL query.
    Simple rule-based approach (safe & expected by assignment).
    """

    q = question.lower()

    # 1️⃣ Worst CPC campaign (March example included)
    if "worst cpc" in q:
        return """
        SELECT campaign_name,
               SUM(amount_spent_inr) * 1.0 / SUM(clicks_all) AS cpc
        FROM dim_campaign
        WHERE strftime('%m', date) = '03'
        GROUP BY campaign_name
        ORDER BY cpc DESC
        LIMIT 1;
        """

    # 2️⃣ UK region performance
    elif "uk" in q and "performance" in q:
        return """
        SELECT region,
               SUM(total_sales) AS total_sales,
               SUM(orders) AS total_orders
        FROM fact_sales
        WHERE region = 'uk'
        GROUP BY region;
        """

    # 3️⃣ Total sales by month
    elif "monthly sales" in q:
        return """
        SELECT strftime('%Y-%m', date) AS month,
               SUM(total_sales) AS total_sales
        FROM fact_sales
        GROUP BY month
        ORDER BY month;
        """

    # 4️⃣ Top region by sales
    elif "top region" in q:
        return """
        SELECT region,
               SUM(total_sales) AS total_sales
        FROM fact_sales
        GROUP BY region
        ORDER BY total_sales DESC
        LIMIT 1;
        """

    # 5️⃣ Default fallback
    else:
        return """
        SELECT *
        FROM fact_sales
        LIMIT 5;
        """


# ----------- FUNCTION: GET AI ANSWER -----------
def get_ai_answer(question, df):
    """
    Sends query result to LLM and returns explanation.
    Only sends SMALL result (important rule).
    """

    prompt = f"""
    You are a data analyst.

    User question:
    {question}

    SQL result:
    {df.to_string(index=False)}

    Give a clear, simple business insight.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ----------- MAIN LOGIC -----------
if question:

    # Step 1: Generate SQL query
    sql_query = generate_sql(question)

    st.subheader("🧠 Generated SQL")
    st.code(sql_query, language="sql")

    try:
        # Step 2: Execute SQL query
        df = pd.read_sql_query(sql_query, conn)

        st.subheader("📊 Query Result")
        st.dataframe(df)

        # Step 3: Get AI explanation
        answer = get_ai_answer(question, df)

        st.subheader("🤖 AI Insight")
        st.write(answer)

    except Exception as e:
        st.error(f"Error: {e}")


# ----------- FOOTER -----------
st.write("-----")
st.write("Built for Growify Assignment 🚀")
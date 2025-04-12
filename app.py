
import streamlit as st
import pandas as pd
from joblib import load

# Load model
model = load("investment_model.joblib")

st.title("AI-Based Mutual Fund Recommendation")

st.subheader("Enter your investment profile:")

age = st.slider("Age", 18, 65, 30)
income = st.number_input("Monthly Income (INR)", 10000, 200000, step=1000)
savings = st.number_input("Current Savings (INR)", 0, 1000000, step=10000)
risk = st.selectbox("Risk Appetite", ["Low", "Medium", "High"])
goal = st.selectbox("Goal", ["Wealth Creation", "Retirement", "Education", "Travel"])
horizon = st.selectbox("Investment Horizon", ["1-3 yrs", "3-5 yrs", "5+ yrs"])

if st.button("Get Recommendation"):
    input_data = {
        "Age": age,
        "Income": income,
        "Savings": savings,
        "Risk_Appetite": {"Low": 0, "Medium": 1, "High": 2}[risk],
        "Goal": {"Education": 0, "Travel": 1, "Retirement": 2, "Wealth Creation": 3}[goal],
        "Horizon": {"1-3 yrs": 0, "3-5 yrs": 1, "5+ yrs": 2}[horizon]
    }

    df_input = pd.DataFrame([input_data])
    prediction = model.predict(df_input)[0]
    labels = ['Conservative', 'Balanced', 'Aggressive']
    category = labels[prediction]

    def recommend_portfolio(category):
        portfolios = {
            'Conservative': {
                'Equity': ['Kotak Equity Arbitrage'],
                'Debt': ['HDFC Short Term Debt Fund'],
                'Gold': ['SBI Gold Fund']
            },
            'Balanced': {
                'Equity': ['Axis Bluechip Fund', 'Mirae Asset Hybrid Equity'],
                'Debt': ['ICICI Prudential Short Term Fund'],
                'Gold': ['Nippon India Gold Savings']
            },
            'Aggressive': {
                'Equity': ['Parag Parikh Flexi Cap', 'Mirae Asset Large Cap'],
                'Debt': ['UTI Credit Risk Fund'],
                'Gold': ['HDFC Gold Fund']
            }
        }
        return portfolios[category]

    portfolio = recommend_portfolio(category)

    st.success(f"You're a {category} investor!")
    st.markdown("### Recommended Portfolio:")
    for asset, funds in portfolio.items():
        st.markdown(f"**{asset}**: {', '.join(funds)}")

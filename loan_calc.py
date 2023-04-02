import streamlit as st
import pandas as pd
import numpy as np

def calculate_loan_schedule(amount, rate, tenure, is_reducing_rate):
    if is_reducing_rate:
        payment_schedule = []
        for month in range(1, tenure + 1):
            interest_payment = amount * rate
            total_payment = amount / (tenure - month + 1) + interest_payment
            principal_payment = total_payment - interest_payment
            amount -= principal_payment

            payment_schedule.append([month, total_payment, principal_payment, interest_payment, amount])
    else:
        n = tenure
        P = (amount * rate) / (1 - (1 + rate)**(-n))
        payment_schedule = []

        for month in range(1, n + 1):
            interest_payment = amount * rate
            principal_payment = P - interest_payment
            amount -= principal_payment

            payment_schedule.append([month, P, principal_payment, interest_payment, amount])

    return pd.DataFrame(payment_schedule, columns=['Month', 'Total Payment', 'Principal Payment', 'Interest Payment', 'Outstanding Balance']).round(2)

def convert_interest_rate(amount, rate, tenure, is_reducing_rate):
    if is_reducing_rate:
        reducing_monthly = rate
        E = amount / tenure
        flat_monthly = ((amount * rate) + ((amount * rate) / 2)) / amount
    else:
        flat_monthly = rate
        E = amount * rate / (1 - (1 + rate) ** (-tenure))
        reducing_monthly = (1 - np.power(1 - ((tenure * E) / amount), 1 / tenure)) / (1 - np.power(1 + rate, -tenure))

    return reducing_monthly, flat_monthly

st.set_page_config(page_title="Loan Calculator", page_icon=":moneybag:", layout="wide")
st.title("Loan Calculator")

amount = st.number_input("Loan Amount", min_value=1000, max_value=1_000_000, step=1000, value=10000)
rate = st.number_input("Interest Rate (as a percentage)", min_value=1.0, max_value=30.0, step=0.01, value=6.0)
tenure = st.number_input("Loan Tenure (in months)", min_value=1, max_value=360, step=1, value=60)

is_reducing_rate = st.radio("Is the interest rate type reducing?", [True, False])

reducing_monthly, flat_monthly = convert_interest_rate(amount, rate / 100, tenure, is_reducing_rate)

interest_rates_table = pd.DataFrame({
    'Interest Rate Type': ['Reducing Monthly', 'Flat Monthly'],
    'Rate (%)': [round(reducing_monthly * 100, 2), round(flat_monthly * 100, 2)]
})

st.table(interest_rates_table)

if st.button("Calculate Loan Schedule"):
    loan_schedule = calculate_loan_schedule(amount, rate / 100, tenure, is_reducing_rate)
    st.dataframe(loan_schedule)

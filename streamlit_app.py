import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Streamlit Title
st.title("Analyzing Shopping Behavior: Gender-Based Spending and Payment Preferences in Istanbul Mall")

# Load Data
df = pd.read_csv('data/data.csv', usecols=["gender", 'invoice_date', 'price', 'payment_method'],
                 parse_dates=['invoice_date'], dayfirst=True)

# Data Cleaning
df.drop_duplicates(inplace=True)
df['invoice_date'] = df['invoice_date'].dt.strftime('%Y')
df = df.groupby(['invoice_date', 'gender', 'payment_method']).mean()
df = df.unstack('payment_method')

# Display DataFrame
st.dataframe(df)

# Create Plot
fig, ax = plt.subplots(figsize=(14, 6))
element = df.plot.bar(stacked=True, ax=ax)

# Add Labels
for bars in element.containers:
    labels = [f"₺ {bar.get_height():.2f}" for bar in bars]
    element.bar_label(bars, labels=labels, label_type='center')

element.set_xlabel('Year & Gender')
element.set_ylabel('Average Spending')
element.set_title('Average Consumer Spending at Shopping Mall in Istanbul, Turkey')

# Customize Legend
ax.legend(["Cash", "Credit Card", "Debit Card"], ncol=3, bbox_to_anchor=(0.68, 0.1))

# Display Plot in Streamlit
st.pyplot(fig)

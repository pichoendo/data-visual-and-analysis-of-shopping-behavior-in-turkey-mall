import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Streamlit Title
st.title("👜Analyzing Shopping Behavior")
st.title("in Istanbul Mall 🕌")

# Load Data
df = pd.read_csv('data/data.csv', usecols=[
    "gender", 'invoice_date', 'quantity', 'price', 'age', 'category', 'shopping_mall', 'payment_method'],
    parse_dates=['invoice_date'], dayfirst=True
)

df.drop_duplicates(inplace=True)
df['shopping_mall'] = df['shopping_mall'].astype(str).fillna('Unknown')
df['invoice_date'] = df['invoice_date'].dt.strftime('%Y')
df['total'] = df['price'] * df['quantity']

# Sidebar for filtering
age_option = st.selectbox('Select Age Range:', ['All'] + sorted(df['age'].unique().astype(str).tolist()))
category_option = st.selectbox('Select Category:', ['All'] + sorted(df['category'].unique().tolist()))
mall_option = st.selectbox('Select Shopping Mall:', ['All'] + sorted(df['shopping_mall'].unique().tolist()))

# Apply Filters based on Sidebar Selections
if age_option != 'All':
    df = df[df['age'] == int(age_option)]  # Filter based on selected age

if category_option != 'All':
    df = df[df['category'] == category_option]  # Filter based on selected category

if mall_option != 'All':
    df = df[df['shopping_mall'] == mall_option]  # Filter based on selected shopping mall

# Select columns and group the data
df = df[['invoice_date', 'gender', 'payment_method', 'total']]
df = df.groupby(['invoice_date', 'gender', 'payment_method']).mean()
df = df.unstack('payment_method')

# Create dynamic title based on selected filters
title = 'Average Consumer Spending at Shopping Mall in Istanbul, Turkey'
if age_option != 'All':
    title = f"Average Spending for Age {age_option} in Istanbul Mall"
if category_option != 'All':
    title += f" - Category: {category_option}"
if mall_option != 'All':
    title += f" - Shopping Mall: {mall_option}"

# Create Plot
fig, ax = plt.subplots(figsize=(14, 6))
element = df.plot.bar(stacked=True, ax=ax)

# Add labels on bars
for bars in element.containers:
    labels = [f"₺ {bar.get_height():.2f}" for bar in bars]
    element.bar_label(bars, labels=labels, label_type='center')

# Add custom label formatting for the last container (payment method)
element.bar_label(element.containers[-1], fmt='₺ %.2F')

# Set labels and title for the plot
element.set_xlabel('Year & Gender')
element.set_ylabel('Average Spending')
element.set_title(title)  # Set the dynamic title

# Customize Legend
plt.legend(["Cash", "Credit Card", 'Debit Card'], ncol=3, bbox_to_anchor=(0.68, 0.1))

# Display the plot in Streamlit
st.pyplot(fig)

# Generate Conclusions Based on Data

# Total Average Spending (based on selected filters)
avg_spending = df['total'].mean()
st.write(f"### Average Spending: ₺ {avg_spending:.2f}")

# Additional Insights (Example: Spending based on Payment Method)
payment_method_spending = df.groupby('payment_method')['total'].mean()
st.write("### Average Spending by Payment Method:")
st.write(payment_method_spending)

# Gender-based Insights
if 'gender' in df.columns:
    gender_spending = df.groupby('gender')['total'].mean()
    st.write("### Average Spending by Gender:")
    st.write(gender_spending)

# Category Insights (if available)
if category_option != 'All' and category_option in df.columns:
    category_spending = df.groupby('category')['total'].mean()
    st.write(f"### Average Spending in Category: {category_option}")
    st.write(category_spending)

# Shopping Mall Insights (if available)
if mall_option != 'All' and mall_option in df.columns:
    mall_spending = df.groupby('shopping_mall')['total'].mean()
    st.write(f"### Average Spending at {mall_option}:")
    st.write(mall_spending)


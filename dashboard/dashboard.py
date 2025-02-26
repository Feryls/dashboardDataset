import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load data
df = pd.read_csv("data_day.csv")

# Convert date column
df['dteday'] = pd.to_datetime(df['dteday'])

# Sidebar filter
st.sidebar.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
start_date, end_date = st.sidebar.date_input("Rentang Waktu", [df['dteday'].min(), df['dteday'].max()])

# Filter data
filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]

# Dashboard Title
st.header("Bike Sharing Dashboard 🚴")

# Daily Users
st.subheader("Daily Bike Rentals")
col1, col2 = st.columns(2)
with col1:
    total_rentals = filtered_df['cnt'].sum()
    st.metric("Total Rentals", value=total_rentals)

with col2:
    avg_rentals = round(filtered_df['cnt'].mean(), 2)
    st.metric("Average Daily Rentals", value=avg_rentals)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(filtered_df['dteday'], filtered_df['cnt'], marker='o', linewidth=2, color="#90CAF9")
ax.set_xlabel("Date")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# Weather Impact
st.subheader("Impact of Weather on Bike Rentals")
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x='weathersit', y='cnt', data=filtered_df, ax=ax, palette='coolwarm')
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Average Rentals")
st.pyplot(fig)

st.caption("© Dicoding 2023")

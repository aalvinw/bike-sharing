import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker  # Ensure ticker is imported

# Load dataset
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")

    # Convert date columns to datetime format
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar
st.sidebar.title("Bike Rental Dashboard")
menu = st.sidebar.selectbox("Select Analysis", ["Overview", "Weather Impact", "Season Trends"])

# **1. Overview**
if menu == "Overview":
    st.title("Bike Rental Data Overview")

    st.subheader("Day Dataset Summary")
    st.write(day_df.describe())

    st.subheader("Hour Dataset Summary")
    st.write(hour_df.describe())

# **2. Weather Impact**
elif menu == "Weather Impact":
    st.title("Weather Impact on Bike Rentals")

    # Mapping weather conditions
    weather_labels = {
        1: "Clear",
        2: "Cloudy",
        3: "Light Rain/Snow",
        4: "Heavy Rain/Snow"
    }
    day_df["weather_label"] = day_df["weathersit"].map(weather_labels)

    # Aggregate data
    sum_order_items_df = day_df.groupby("weathersit")["cnt"].sum().reset_index()

    # Plot
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 7))

    df_sorted1 = sum_order_items_df.sort_values(by="cnt", ascending=False)

    sns.barplot(
        x="weathersit",
        y="cnt",
        data=df_sorted1,
        palette="Blues_r",
        ax=ax[0]
    )
    ax[0].set_xlabel("Weather Condition", fontsize=12)
    ax[0].set_title("Most Rentals by Weather", fontsize=14)
    ax[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    df_sorted2 = sum_order_items_df.sort_values(by="cnt", ascending=True)

    sns.barplot(
        x="weathersit",
        y="cnt",
        data=df_sorted2,
        palette="Blues",
        ax=ax[1]
    )
    ax[1].set_xlabel("Weather Condition", fontsize=12)
    ax[1].set_title("Least Rentals by Weather", fontsize=14)
    ax[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    st.pyplot(fig)

# **3. Season Trends**
elif menu == "Season Trends":
    st.title("Seasonal Bike Rental Trends")

    # Aggregate data
    sum_order_items_df = day_df.groupby("season")["cnt"].sum().reset_index()

    # Plot
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 7))

    df_sorted1 = sum_order_items_df.sort_values(by="cnt", ascending=False)

    sns.barplot(
        x="season",
        y="cnt",
        data=df_sorted1,
        palette="Blues_r",
        ax=ax[0]
    )
    ax[0].set_xlabel("Season", fontsize=12)
    ax[0].set_title("Most Rentals by Season", fontsize=14)
    ax[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    df_sorted2 = sum_order_items_df.sort_values(by="cnt", ascending=True)

    sns.barplot(
        x="season",
        y="cnt",
        data=df_sorted2,
        palette="Blues",
        ax=ax[1]
    )
    ax[1].set_xlabel("Season", fontsize=12)
    ax[1].set_title("Least Rentals by Season", fontsize=14)
    ax[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    st.pyplot(fig)

# Footer
st.sidebar.markdown("**Developed by: Your Name**")

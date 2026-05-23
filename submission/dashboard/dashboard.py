import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

#set style seaborn agar lebih cantik
#helper functions

def create_monthly_rentals_df(df):
    monthly_df = df.resample(rule= 'ME', on='dteday').agg({
        'cnt':'sum'
    }).reset_index()
    monthly_df['month_name']= monthly_df['dteday'].dt.strftime('%B %Y')
    return monthly_df

def create_weather_rentals_df(df):
    return df.groupby('weather_label')['cnt'].mean().reset_index()

def create_weather_rentals_df(df):
    return df.groupby('weather_label')['cnt'].mean().reset_index()

def create_time_category_df(df):
    time_category_df = df.groupby('time_category')['cnt'].mean().reset_index()
    return time_category_df

def create_hourly_rentals_df(df):
    df_copy = df.copy()
    df_copy['day_type'] = df_copy['workingday'].map({1: 'Working Day', 0:'Weekend/Holiday'})
    return df_copy

def group_time(hour):
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'

#load data dan preprocessing
@st.cache_data
def load_data():
    day_df = pd.read_csv('all_day.csv')
    hour_df = pd.read_csv('all_hour.csv')

    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    #pre-processing untuk time  category
    hour_df['timr_category'] = hour_df['hr'].apply(group_time)
    category_order = ['Morning', 'Afternoon', 'Evening', 'Night']
    hour_df['time_category'] = pd.Categorical(hour_df['time_category'], categories=category_order, ordered=True)
    
    return day_df, hour_df

day_df, hour_df = load_data()

#sidebar

min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

with st.sidebar:
    st.title("Bike Sharing Dashboard")
    st.image("https://github.com/pitaeoxo17-cloud/dataset-submission/blob/main/bike-removebg-preview.png?raw=true")

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

#filter data berdasarkan rentang waktu yang dipilih
main_day_df = day_df[(day_df['dteday'] >= str(start_date)) & (day_df['dteday'] <= str(end_date))]
main_hour_df = hour_df[(hour_df['dteday'] >= str(start_date)) & (hour_df['dteday'] <= str(end_date))]

#menyiapkkan data frame untuk visualisasi
monthly_rentals_df = create_monthly_rentals_df(main_day_df)
weather_rentals_df = create_weather_rentals_df(main_day_df)
time_category_df = create_time_category_df(main_hour_df)
hourly_rentals_df = create_hourly_rentals_df(main_hour_df)

#main dashboard
st.title('Bike Sharing Analysis Dashboard')
col1, col2 = st.columns(2)
with col1:
    total_rentals = main_day_df.cnt.sum()
    st.metric('Total Penyewaan', value=f'{total_rentals:,}')
with col2:
    avg_rentals = round(main_day_df.cnt.sum())
    st.metric('Rata-rata per Hari', value=f'{avg_rentals:,}')

st.markdown('---')

#chart 1 monthly trend
st.subheader('Monthly Rentals Trend')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_rentals_df['dteday'],
    monthly_rentals_df['cnt'],
    marker='o',
    linewidth=3,
    linestyle='-',
    color='Blue'
)

ax.set_xlabel(None)
ax.set_ylabel('Total Penyewaan', fontsize=15)
st.pyplot(fig)

#chart 2 weather and time category
st.subheader('Performance by Weather and Time')
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='weather_label', y='cnt', data=weather_rentals_df.sort_values(by='cnt', ascending=False), palette='Blues_d', ax=ax)
    ax.set_title('Average Rentalsby Weather', fontsize=18)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x="time_category", y="cnt", data=time_category_df, palette="coolwarm", ax=ax)
    ax.set_title("Average Rentals by Time Category", fontsize=18)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    st.pyplot(fig)

#chart 3 hourly patterns
st.subheader("Hourly Patterns: Working Day vs Weekend")
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(
    data=hourly_rentals_df, 
    x='hr', 
    y='cnt', 
    hue='day_type', 
    palette='Set1', 
    linewidth=3, 
    ax=ax
)
ax.set_xticks(range(0, 24))
ax.set_xlabel("Hour of the Day (0-23)")
ax.set_ylabel("Average Rentals")
ax.legend(title="Tipe Hari")
st.pyplot(fig)

st.caption('Copyright © 2026 | Bike Sharing Dashboard by Puspita')
   
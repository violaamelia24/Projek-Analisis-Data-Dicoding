import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import plotly as py

order_payment= pd.read_csv("order_payments_dataset.csv")
order_payment.head()

items= pd.read_csv("order_items_dataset.csv")
product=pd.read_csv("products_dataset.csv")
order=pd.read_csv("orders_dataset.csv")

df_one=pd.merge(order_payment,items,on='order_id',how='inner')
df_ones=pd.merge(df_one,order,on='order_id',how='inner')
df_two=pd.merge(df_ones,product,on='product_id',how='inner')
df=df_two.drop(columns=['product_name_lenght', 'product_description_lenght', 'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm'])
df['order_date'] = df['order_purchase_timestamp'].str[:10]
df['order_date'] = pd.to_datetime(df['order_date'])
list(df)
df.dropna()

st.title('Sales Report')
tab1, tab2, = st.tabs(["Average Sales","Type of Payment" ])

with st.sidebar :
    st.image("https://i.pinimg.com/originals/4a/38/7b/4a387bda853bca3782d73234c786a150.png")
    st.subheader("Visit Our Website")
    st.sidebar.markdown("www.shoppingishobby.com")

with tab1 :
    st.subheader("Average sales/day in year")
#line chart
    def filter_data_by_year(df, year):
        filtered_df = df[df['order_date'].dt.year == year]
        return filtered_df


    selected_year = st.radio("Select Year", [2016, 2017, 2018])

    filtered_df = filter_data_by_year(df, selected_year)

    average_sales = filtered_df.groupby('order_date')['payment_value'].mean().reset_index()

    fig2 = plt.figure(figsize=(15, 6))
    plt.plot(average_sales['order_date'], average_sales['payment_value'], marker='o')

    max_value = average_sales['payment_value'].max()
    min_value = average_sales['payment_value'].min()

    max_index = average_sales.loc[average_sales['payment_value'] == max_value, 'order_date'].iloc[0]
    min_index = average_sales.loc[average_sales['payment_value'] == min_value, 'order_date'].iloc[0]

    plt.text(max_index, max_value, f'{max_value:.2f}', ha='left', va='bottom')
    plt.text(min_index, min_value, f'{min_value:.2f}', ha='left', va='top')

    plt.title("Sales")
    plt.xlabel("Time")
    plt.ylabel("Average sells/day")
    plt.xticks(rotation=30)
    plt.grid(True)

    st.pyplot(fig2)

with tab2 :
    #barchart
    fig= plt.figure(figsize=(5,6))
    plt.style.use('fivethirtyeight')
    plt.bar(
        x=df["payment_type"].unique(),
        height=df["payment_type"].value_counts().to_list(),
        color='blue'    
        )
    plt.xlabel('Payment Installments')
    plt.ylabel('Count')
    plt.show()
    st.pyplot(fig)


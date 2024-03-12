import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

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

df=df.dropna()

st.title('Sales Report')
tab1, tab2, = st.tabs(["Average Sales","Type of Payment" ])

with st.sidebar :
    st.image("https://i.pinimg.com/originals/4a/38/7b/4a387bda853bca3782d73234c786a150.png")
    st.subheader("Visit Our Website")
    st.sidebar.markdown("www.shoppingishobby.com")

with tab1 :
    st.subheader("Average sales/month in year")https://github.com/violaamelia24/Projek-Analisis-Data-Dicoding/blob/main/projek.py
#line chart
    def filter_data_by_year(df, year):
        filtered_df = df[df['order_date'].dt.year == year]
        return filtered_df


    selected_year = st.radio("Select Year", [2016, 2017, 2018])

    filtered_df = filter_data_by_year(df, selected_year)
    sum_sales_date = df.groupby('order_date')['payment_value'].sum().reset_index()
    average_sales=sum_sales_date.resample('M',on='order_date').mean()
    average_sales_monthly=average_sales.dropna()

    fig2 = plt.figure(figsize=(15,6))
    plt.plot(average_sales_monthly.index, average_sales_monthly['payment_value'])

    max_value_monthly = average_sales_monthly['payment_value'].max()
    min_value_monthly = average_sales_monthly['payment_value'].min()

    max_index_monthly = average_sales_monthly.loc[average_sales_monthly['payment_value'] == max_value_monthly].index[0]
    min_index_monthly = average_sales_monthly.loc[average_sales_monthly['payment_value'] == min_value_monthly].index[0]

    plt.text(max_index_monthly, max_value_monthly, f'{max_value_monthly:.2f}', ha='left', va='bottom')
    plt.text(min_index_monthly, min_value_monthly, f'{min_value_monthly:.2f}', ha='left', va='top')

    plt.title("Penjualan")
    plt.xlabel("Waktu")
    plt.ylabel("Rata-rata penjualan/bulan")
    plt.xticks(rotation=30)
    plt.grid(True)
    plt.show()

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


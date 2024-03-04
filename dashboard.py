import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# define methods for creating dataframes
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_date').agg({
        "order_id": "nunique", # count the unique orders
        "price": "sum" # count the total price
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    return daily_orders_df

def create_products_df(df):
    products_df = df.groupby(by="product_category", as_index = False).agg({
        "order_id": "count", # count all the orders
        "rating": "mean", # count the average rating
        "price": "sum" # count the total price
    }).sort_values(by="order_id", ascending=False)
    products_df = products_df.reset_index()
    products_df.rename(columns={
        "order_id": "products_sold",
        "rating": "rating",
        "price": "revenue"
    }, inplace=True)
    return products_df

def create_byday_df(df):
    byday_df = df.groupby(by="day").order_id.nunique().reset_index()
    return byday_df

def create_bytime_df(df):
    bytime_df = df.groupby(by="time").order_id.nunique().reset_index()
    return bytime_df

def create_bystate_df(df):
    bystate_df = df.groupby(by="state").customer_id.nunique().reset_index()   
    return bystate_df

def create_payment_df(df):
    payment_df = df.groupby(by="payment_type", as_index = False).agg({
        "order_id": "nunique", # count the unique orders
        "payment_value": "mean", # count the average payment value
    }).sort_values(by="order_id", ascending=False)
    payment_df = payment_df.reset_index()
    payment_df.rename(columns={
        "order_id": "transaction",
        "payment_value": "amount"
    }, inplace=True)

    return payment_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_date": "max", # get the last order date
        "order_id": "nunique", # count the unique orders
        "price": "sum" # count the total price
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    rfm_df = rfm_df.reset_index()
    
    return rfm_df

def set_palette(series, max_color = '#90CAF9', other_color = 'lightgrey'):
    max_val = series.max() # get the max value of input
    pal = [] # initiate list
    for item in series: # loop to check value and assign colors
        if item == max_val:
            pal.append(max_color)
        else:
            pal.append(other_color)
    return pal

st.title('E-Commerce Dashboard :shopping_bags:')

# import data from csv and order it bydate
all_df = pd.read_csv("all_data.csv")
all_df.sort_values(by="order_date", inplace=True)
all_df.reset_index(inplace=True)
all_df["order_date"] = pd.to_datetime(all_df["order_date"])

# get min and max date for initialising date_input
min_date = all_df["order_date"].min()
max_date = all_df["order_date"].max()

# make a sidebar for storing widgets for easy access
with st.sidebar:
    st.header("Widgets")
    # make a widget for inputing date
    start_date, end_date = st.date_input(
        label='Select Time Span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# make a new df that follows the date from input
main_df = all_df[(all_df["order_date"] >= str(start_date)) & 
                (all_df["order_date"] <= str(end_date))]

# creating dataframes with methods
daily_orders_df = create_daily_orders_df(main_df)
products_df = create_products_df(main_df)
byday_df = create_byday_df(main_df)
bytime_df = create_bytime_df(main_df)
bystate_df = create_bystate_df(main_df)
payment_df = create_payment_df(main_df)
rfm_df = create_rfm_df(main_df)

st.header('Daily Orders', divider='blue')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
 
with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "BRL", locale='pt_BR') 
    st.metric("Total Revenue", value=total_revenue)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_date"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)


st.header("Product Category", divider='blue')
st.subheader("Best & Worst Selling Category")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#90CAF9", "lightgrey", "lightgrey", "lightgrey", "lightgrey"]
 
sns.barplot(x="products_sold", y="product_category", data=products_df.head(5), 
            palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Selling Category", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="products_sold", y="product_category", data=products_df.sort_values(by="products_sold", ascending=True).head(5), 
            palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Selling Category", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)


st.subheader("Best Selling Category Performance")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
sns.barplot(x="rating", y="product_category", data=products_df.head(5), palette=set_palette(products_df.head(5)['rating']), ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Rating", fontsize=30)
ax[0].set_xlim(0, 5)
ax[0].set_title("Best Selling Category Rating", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=25)
 
sns.barplot(x="revenue", y="product_category", data=products_df.head(5), palette=set_palette(products_df.head(5)['revenue']), ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Revenue", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Best Selling Category Revenue", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=25) 
 
st.pyplot(fig)


st.header("Customers", divider='blue')
st.subheader("Location")

fig = plt.figure(figsize=(35, 15))
sns.barplot(x="state", y="customer_id", data=bystate_df, palette=set_palette(bystate_df['customer_id']))
plt.ylabel(None)
plt.xlabel("State", fontsize=30)
plt.title("Number of Customers by State", loc="center", fontsize=50)
plt.tick_params(axis='y', labelsize=35)
plt.tick_params(axis='x', labelsize=30)
st.pyplot(fig)

st.subheader("Payment Method")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
ax[0].pie(payment_df["transaction"], labels=payment_df["payment_type"], colors=sns.color_palette('Blues'), autopct='%.0f%%')
ax[0].set_title("Payment Method Distribution by Transactions", loc="center", fontsize=15)
sns.barplot(x="payment_type", y="amount", data=payment_df, palette=set_palette(payment_df["amount"]), ax = ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Payment Method", fontsize=10)
ax[1].set_title("Average Transaction Value of Payment Methods", loc="center", fontsize=15)   
st.pyplot(fig)

st.subheader("Order Time")

fig = plt.figure(figsize=(35, 15))
sns.barplot(x="day", y="order_id", data=byday_df, palette=set_palette(byday_df['order_id']))
plt.ylabel(None)
plt.xlabel(None)
plt.title("Number of Orders by Day", loc="center", fontsize=40)
plt.tick_params(axis='y', labelsize=35)
plt.tick_params(axis='x', labelsize=30)
st.pyplot(fig)

fig = plt.figure(figsize=(35, 15))
sns.barplot(x="time", y="order_id", data=bytime_df, palette=set_palette(bytime_df['time']))
plt.ylabel(None)
plt.xlabel(None)
plt.title("Number of Orders by Time of Day", loc="center", fontsize=40)
plt.tick_params(axis='y', labelsize=35)
plt.tick_params(axis='x', labelsize=30)
st.pyplot(fig)


st.header("RFM Analysis", divider='blue')
st.subheader("Best Customer Based on RFM Parameters")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "BRL", locale='pt_BR') 
    st.metric("Average Monetary", value=avg_frequency)
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
 
sns.barplot(y="recency", x="index", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="frequency", x="index", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="monetary", x="index", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)
 
st.pyplot(fig)
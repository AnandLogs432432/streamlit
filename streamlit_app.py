import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import math

st.title("Data App Assignment (Anand Loganthan, DSBA 5122, 6/30/24)")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")

unique_category = ['Furniture', 'Office Supplies', 'Technology']

cat = st.selectbox("Please choose a category", unique_category)


st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")

if 'Furniture' in cat:
  sub_cat = st.multiselect("Please choose your sub-categories", ['Bookcases', 'Chairs', 'Tables', 'Furnishings'])

elif 'Office Supplies' in cat:
  sub_cat = st.multiselect("Please choose your sub-categories", ['Labels', 'Storage', 'Art', 'Binders', 'Appliances', 'Paper', 'Envelopes', 'Fasteners', 'Supplies'])

else:
  sub_cat = st.multiselect("Please choose your sub-categories", ['Phones', 'Accessories', 'Machines', 'Copiers'])  

if sub_cat:

  st.write("### (3) show a line chart of sales for the selected items in (2)")

  df1 = df.reset_index().set_index('Sub_Category')
  df1 = df1.loc[sub_cat]
  
  st.line_chart(data=df1, x='Order_Date', y='Sales', x_label = 'Order Date')
  
  st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
  
  total_sales = sum(df1['Sales'])
  total_sales_rounded = '$'+str(round(total_sales, 2))
  total_profit = sum(df1['Profit'])
  total_profit_rounded = '$'+str(round(total_profit, 2))
  total_profit_margin = (total_profit/total_sales)*100
  total_profit_margin_rounded = str(round(total_profit_margin, 2))+'%'
    
  st.metric('Total Sales', total_sales_rounded)
  st.metric('Total Profit', total_profit_rounded)
  st.metric('Total Profit Margin', total_profit_margin_rounded)
    
  st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
    
  overall_profit_margin = sum(df['Profit'])/sum(df['Sales'])*100
  overall_profit_margin_rounded = str(round(overall_profit_margin, 2))+'%'
    
  st.metric('Total Profit Margin', total_profit_margin_rounded, overall_profit_margin_rounded)

else:
  st.write('Choosing sub-categories will populate the rest of the form!')

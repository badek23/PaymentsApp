
#### Import Libraries ####
import streamlit as st
import pandas as pd
import os

#### Streamlit ####
st.set_page_config(page_title='Payments', page_icon='💳')

# Hide menu + footer options for users
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# Text on page
st.markdown("<h1 style='text-align: center; color: black;'>Payments App</h1>", unsafe_allow_html=True)
### st.markdown("<h1 style='font-size: 1em; text-align: center; color: black;'>XXX</h1>", unsafe_allow_html=True)

# Function to load data from CSV file
def load_data():
    if os.path.exists("data.csv"):
        return pd.read_csv("data.csv")
    else:
        return pd.DataFrame(columns=["Person Who Paid", "Person Who Owes", "Item", "Amount"])

# Function to save data to CSV file
def save_data(data):
    data.to_csv("data.csv", index=False) 

# Function to save input users in a list
@st.cache_data
def new_user():
    return []

if 'data' not in st.session_state:
    st.session_state.data = new_user()

# Load CSV of payments data
data = load_data()



user = st.text_input("Input New User")

if st.button("Input New User"):
    st.session_state.data.append(user)

user_paid = st.selectbox(
    'Person Who Paid',
    (set(st.session_state.data)))

user_topay = st.selectbox(
    'Person Who Owes',
    (set(st.session_state.data)))

item = st.text_input("Item")
amount = st.number_input('Amount')

# foo = st.slider("foo", 0, 100)
# bar = st.slider("bar", 0, 100)

if st.button("Add row"):
    data = data.append({"Person Who Paid": user_paid, "Person Who Owes": user_topay, "Item": item, "Amount": amount}, ignore_index=True)
    save_data(data)
    st.write("Owed money successfully added.")

if st.button("Delete payments"):
    data = pd.DataFrame(columns=["Person Who Paid", "Person Who Owes", "Item", "Amount"])
    save_data(data)
    st.write("Saved payments successfully deleted.")

if not data.empty:
    st.write(data)

# Iterate over each row in the DataFrame
if st.button("Calculate payments"):
    for i in range(len(data)-1):
        for j in range(len(data)):
            # Check if 'Person Who Paid' in row i is equal to 'Person Who Owes' in row i+j
            if data.loc[i, 'Person Who Paid'] == data.loc[i+j, 'Person Who Owes'] and data.loc[i+j, 'Person Who Paid'] == data.loc[i, 'Person Who Owes']:
                total = data.loc[i+j,'Amount'] - data.loc[i,'Amount']
                st.write(data['Person Who Owes'][i+j], "owes €", total, "to", data['Person Who Paid'][i+j])
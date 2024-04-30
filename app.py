
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
        return pd.DataFrame(columns=["Payer", "Ower", "Item", "Amount"])
    
# Load CSV of payments data
data = load_data()

# Function to save data to CSV file
def save_data(data):
    data.to_csv("data.csv", index=False) 

# Function to save input users in a list
@st.cache_data
def new_user():
    return []

if 'data' not in st.session_state:
    st.session_state.data = new_user()


delete_row = st.number_input("Delete entry by typing row num:", step=None, value=None)
if delete_row:
    # Convert delete_row to integer assuming it's an index
    delete_row_index = int(delete_row)
    # Remove the row at the specified index
    data = data.drop(delete_row_index)
    # Save the modified data
    save_data(data)
    st.write("Entry ", delete_row_index, " successfully deleted.")

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
    new_entry = pd.DataFrame({
        "Payer": [user_paid],
        "Ower": [user_topay],
        "Item": [item],
        "Amount": [amount]
    })
    new_entry = pd.DataFrame(new_entry)
    data = pd.concat([data, new_entry], axis=0)
    save_data(data)
    st.write("Owed money successfully added.")

if not data.empty:
    st.write(data)


if st.button("Calculate payments"):
    # Initialize a dictionary to store the balances for each pair
    balances = {}
    
    for index, row in data.iterrows():
        payer = row['Payer']
        receiver = row['Ower']
        amount = row['Amount']
        
        # Update the balances dictionary
        balances[(payer, receiver)] = balances.get((payer, receiver), 0) - amount
        balances[(receiver, payer)] = balances.get((receiver, payer), 0) + amount
    #total = {}
    # Figure out who owes whom
    for (payer, receiver), balance in balances.items():
        if balance < 0:
            st.write(receiver, "owes", payer, "€", round(-balance, 2))

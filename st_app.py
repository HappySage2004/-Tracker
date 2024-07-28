import streamlit as st

st.header("🩸 Ketchup tracker")
date = st.date_input("Pick the date")
action =  st.button("Enter")
if action:
    st.write("Sucessfully entered date -> ", date)


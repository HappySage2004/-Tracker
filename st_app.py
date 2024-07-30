import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

def convert_dateformat(date:str) -> str:
    # Convert the string to a datetime object
    date_obj = datetime.strptime(date, "%d/%m/%Y")
    formatted_date = date_obj.strftime("%d %B %Y")
    return  formatted_date

conn = st.connection("gsheets", type=GSheetsConnection)

st.title("Bubu's Health Tracker : ")
tab1, tab2, tab3 = st.tabs(["Period", "Blood Sugar", "Weight"])

with tab1:
    st.header("Periods 🩸")
    df_prd = conn.read( worksheet="database period", ttl="3s", usecols=[0])
    length1 = len(df_prd.index)
    date = st.date_input("Pick the date")
    col1, col2 = st.columns(2)
    with col1:
        action =  st.button("Enter")
    with col2:
        delete_action = st.button("Delete last entry")

    if action:
        df_prd.loc[len(df_prd.index)] = [date.strftime("%d/%m/%Y")]
        conn.update(worksheet="database period", data = df_prd)
        st.write("Sucessfully entered date : ", date, 'length --',len(df_prd))
    st.write("Current number of entries = ", length1)
    st.dataframe(df_prd)

with tab2:
    st.header("Blood Sugar 🍰")
    df_bldsgr = conn.read(worksheet = "database blood sugar", ttl = "3s", usecols=[0,1,2])
    length2 = len(df_bldsgr.index)
    date2 = st.date_input("Pick the date", key=2)

    col3, col4 = st.columns(2)
    with col3:
        fasting_lvl = st.number_input("Fasting")
    with col4: 
        pp_lvl = st.number_input("PP")
    
    col5, col6 = st.columns(2)
    with col5:
        action2 = st.button("Enter", key=3)
    with col6:
        delete_action2 = st.button("Delete last entry", key=4)
    
    if action2:
        df_bldsgr.loc[len(df_bldsgr.index)] = [date2.strftime("%d/%m/%Y"), fasting_lvl, pp_lvl]
        conn.update(worksheet="database blood sugar", data = df_bldsgr)
        st.write("Sucessfully entered reading on date : ", date2)
    st.write("Current number of entries = ", length2)
    st.dataframe(df_bldsgr)

with tab3:
    st.header("Weight 🧍‍♀️")
    df_weight = conn.read( worksheet="database weight", ttl="3s", usecols=[0,1])
    length3 = len(df_weight.index)

    col7, col8 = st.columns(2)
    with col7: 
        date3 = st.date_input("Pick the date", key=5)
    with col8: 
        weight = st.number_input("Weight in kgs")
    
    col9, col10 = st.columns(2)
    with col9:
        action3 =  st.button("Enter", key=6)
    with col10:
        delete_action3 = st.button("Delete last entry", key=7)

    if action3:
        df_weight.loc[len(df_weight.index)] = [date3.strftime("%d/%m/%Y"), weight]
        conn.update(worksheet="database weight", data = df_weight)
        st.write("Sucessfully entered date : ", date3, "   weight : ", weight, "kg")
    st.write("Current number of entries = ", length3)

    if(length3>=2):
        st.write("Last entry : ", convert_dateformat(df_weight['date'][length3-1]) , " -",df_weight['weight'][length3-1]," kg" )
        st.write("2nd Last entry : ", convert_dateformat(df_weight['date'][length3-2]) ," -" ,df_weight['weight'][length3-2], " kg" )
        st.write("Progress tracking chart :")
        st.line_chart(df_weight,x='date', y='weight', color="#FF4B4B")


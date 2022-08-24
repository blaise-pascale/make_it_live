import streamlit as st
import mysql.connector
g="Hello!"
st.set_page_config(page_title=g)
def check():
    b=st.error("Do you want to continue")
    if st.button("Yes"):
        st.write("Logged in !")
    if st.button("No"):
        return False
    
#st.title("Hello Everyone")

side=st.sidebar

side.title("Choose your Page:")
a=st.checkbox("Show/Hide")
if a:
    status=st.radio("Select Gender : ",('Male',"Female"))
    st.success(status)
if st.button("Log in"):
    check()
if "name" not in st.session_state:
    st.session_state["name"]=''
name=st.text_input("Enter Your Name Here :",st.session_state["name"])
submit=st.button("Submit")
if submit:
    st.session_state["name"]=name
    st.write("Hello ",st.session_state["name"])

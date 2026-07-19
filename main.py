import streamlit as st
st.title("hey Altaf")
name=st.text_input("Enter your name")
if st.button("submit"):
    if name:
        st.success(f"hello,{name}!welcome to my app,")
    else:
        st.warning("p-lease enter your nmae")

import streamlit as st
st.title("my first streamlit App")
name=st.text_input("Enter your name")
if st.button("submit"):
    if name:
        st.success(f"hello,{name}!welcome to streamlit,")
    else:
        st.warning("p-lease enter your nmae")
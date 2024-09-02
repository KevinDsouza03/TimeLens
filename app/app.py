import streamlit as st
import pandas as pd


def main():
    df = pd.read_csv('./results/focus.csv')
    st.title("What are my habits")
    st.bar_chart(df)

    




main() 
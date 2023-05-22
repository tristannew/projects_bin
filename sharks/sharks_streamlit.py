import streamlit as st
from sharks_analysis import df

st.bar_chart(data = df, x=df[df['Country'].count() > 20]['Country'])

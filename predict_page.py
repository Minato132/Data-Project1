#! C:\Users\chens\Documents\Data-Project1\env\Scripts\python.exe

import streamlit as st
import pickle 
import pandas as pd

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

data_reg = data['model']
data_country_label = data['countrylabel']
data_ed_label = data['educationlabel']

def show_predict_page():
    st.title("Software Developer Salary Prediction")
    st.write("""### We need some infomration to predict the salary""")

    countries = (
        "United States of America",
        "Germany",
        "United Kingdom of Great Britain and Northern Ireland",
        "Canada",
        "India",
        "France",
        "Netherlands",                                             
        "Australia",                                               
        "Spain",                                              
        "Brazil",                                                
        "Sweden",                                               
        "Italy",                                                  
        "Poland",                                               
        "Switzerland",                                              
        "Denmark",                                                
        "Norway",                                               
    ) 

    education = (
        'Less than Bachelor',
        'B.S',
        'M.S',
        'Post Grad'
    )

    country = st.selectbox("Country", countries)
    educationlv = st.selectbox("Education Level", education)
    experience = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = pd.DataFrame({'Country': [country], 
                          'EdLevel': [educationlv],
                          'YearsCodePro':[experience]}
                          )
        X['Country'] = data_country_label.transform(X["Country"])
        X['EdLevel'] = data_ed_label.transform(X['EdLevel'])
        X = X.astype(float)

        salary = data_reg.predict(X)
        
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
#! C:\Users\chens\Documents\Data-Project1\env\Scripts\python.exe

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def short_cat(category, cutoff):
    category_map = {}
    for i in range(len(category)):
        if category.values[i] >= cutoff:
            category_map[category.index[i]] = category.index[i]
        else:
            category_map[category.index[i]] = 'Other'
    
    return category_map


def clean_exp(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_degree(x):
    if 'Bachelor' in x:
        return 'B.S'
    if 'Master' in x:
        return 'M.S'
    if 'Professional' in x:
        return 'Post Grad'
    else:
        return 'Less than Bachelor'
    
@st.cache_data
def load_data():
    df = df = pd.read_csv('survey_results_public.csv')

    df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly']]
    df.rename(columns = {'ConvertedCompYearly': 'Salary'}, inplace = True)

    df = df[df['Salary'].notnull()]
    df.dropna(inplace = True)
    
    df = df[df['Employment'] ==  'Employed, full-time']
    df.drop(columns = 'Employment', inplace = True)
    country_map = short_cat(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_exp)

    df['EdLevel'] = df['EdLevel'].apply(clean_degree)
    return df


data = load_data()

def show_explore_page():
    st.title('Visual Representation of Software Engineer Salaries')
    st.header("Stack overflow Developer Survey 2020")

    dat = data['Country'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(dat, labels = dat.index, autopct = "%1.1f%%", shadow = True, startangle = 0)
    ax1.axis('Equal')

    st.subheader('The number of data from Different Countries')
    st.pyplot(fig1)
    

    st.subheader('Mean Salary Based on Country')
    dat = data.groupby(['Country'])['Salary'].mean().sort_values(ascending = True)
    st.bar_chart(dat)
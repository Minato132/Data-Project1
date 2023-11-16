# Code is used for the preliminarly cleaning and apply machine learning algorithms in to 
# predict data

#! C:\Users\chens\Documents\Data-Project1\env\Scripts\python.exe

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pickle


df = pd.read_csv('survey_results_public.csv')

df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly']]
df.rename(columns = {'ConvertedCompYearly': 'Salary'}, inplace = True)

#This line of code will drop all rows that have a null value in the specified column

df = df[df['Salary'].notnull()]
df.dropna(inplace = True)
# print(df.isnull().sum())
df = df[df['Employment'] ==  'Employed, full-time']
df.drop(columns = 'Employment', inplace = True)

# Here we will create logic in order to shorten our categories so that our machine learning program has
# a more accurate prediction

def short_cat(category, cutoff):
    category_map = {}
    for i in range(len(category)):
        if category.values[i] >= cutoff:
            category_map[category.index[i]] = category.index[i]
        else:
            category_map[category.index[i]] = 'Other'
    
    return category_map
            
country_map = short_cat(df.Country.value_counts(), 400)
df['Country'] = df['Country'].map(country_map)

# #Checking the boxplots
# #-------------------------------------------------------------
# df.boxplot('Salary', 'Country', vert = False)
# plt.xticks(rotation = 90)
# plt.show()
# #-------------------------------------------------------------

# From looking at boxplot we want to keep all values that are within 4k - 250k,
#   and we are getting rid of all other countries

df = df[(df['Salary'] <= 250000) & (df['Salary'] >= 4000) & (df['Country'] != 'Other')]

# #Checking the boxplots again
# #-------------------------------------------------------------
# df.boxplot('Salary', 'Country', vert = False)
# plt.xticks(rotation = 90)
# plt.show()
# #-------------------------------------------------------------

# Use the unique method to only print out unique values
# print(df['YearsCodePro'].unique())


# Now we can apply every value in here by a predefined function

def clean_exp(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

df['YearsCodePro'] = df['YearsCodePro'].apply(clean_exp)



# Using same idea as the experience column

def clean_degree(x):
    if 'Bachelor' in x:
        return 'B.S'
    if 'Master' in x:
        return 'M.S'
    if 'Professional' in x:
        return 'Post Grad'
    else:
        return 'Less than Bachelor'

df['EdLevel'] = df['EdLevel'].apply(clean_degree)



# We can relabel elements into number       
educationlabel = LabelEncoder()
df['EdLevel'] = educationlabel.fit_transform(df['EdLevel'])

# Doing the same thing for countries
countrylabel = LabelEncoder()
df['Country'] = countrylabel.fit_transform(df['Country'])

#--------------------------------------------------

# The data is set for modeling now

# Prepping out data without splitting any of it into training or testing


X = df.drop(columns = 'Salary')
y = df['Salary']
print(X)
# Now we machine learn
max_depth = [None, 2, 4, 6, 8, 10, 12]
parameters = {"max_depth" : max_depth}
regressor = DecisionTreeRegressor(random_state = 0)
gs  = GridSearchCV(regressor, parameters, scoring = 'neg_mean_squared_error')
gs.fit(X, y.values)
regressor = gs.best_estimator_
regressor.fit(X, y.values)


 
# Error testing
# y_pred = regressor.predict(X)
# error = np.sqrt(mean_squared_error(y, y_pred))
# print(error)


# Applying a Prediction

pred = pd.DataFrame({'Country': ['Germany'],
                     'EdLevel': ['M.S'],
                     'YearsCodePro':[10]})

pred['Country'] = countrylabel.transform(pred['Country'])
pred['EdLevel'] = educationlabel.transform(pred['EdLevel'])
pred = pred.astype(float)
print(pred)
# pred[:, 1] = educationlabel.transform(pred[:, 1])
# pred = pred.astype(float)

predict = regressor.predict(pred)
print(predict)

data = {'model': regressor, 'countrylabel': countrylabel, 'educationlabel': educationlabel}
with open('saved_steps.pkl', 'wb') as file:
    data = pickle.dump(data, file)

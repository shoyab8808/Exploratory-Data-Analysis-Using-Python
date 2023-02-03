#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install opendatasets --upgrade --quiet')


# In[5]:


import opendatasets as od


# In[6]:


od.download("stackoverflow-developer-survey-2020")


# In[7]:


import os


# In[8]:


os.listdir("stackoverflow-developer-survey-2020")


# In[9]:


import pandas as pd


# In[10]:


survey_raw_df=pd.read_csv("stackoverflow-developer-survey-2020/survey_results_public.csv")


# In[11]:


survey_raw_df


# In[12]:


survey_raw_df.columns


# In[16]:


pd.read_csv("stackoverflow-developer-survey-2020/survey_results_schema.csv")


# In[21]:


schema_fname="stackoverflow-developer-survey-2020/survey_results_schema.csv"
schema_raw=pd.read_csv(schema_fname, index_col="Column").QuestionText


# In[22]:


schema_raw


# In[25]:


schema_raw["YearsCodePro"]


# # data preperation and cleaning

# While the survey responses contain a wealth of information, we'll limit our analysis to the following areas:

#  Demographics of the survey respondents and the global programming community

# Distribution of programming skills, experience, and preferences
# Employment-related information, preferences, and opinions

# Let's select a subset of columns with the relevant data for our analysis.
# 
# 

# In[35]:


selected_columns = [
    #Demographics
    "Country",
    "Age",
    "Gender",
    "EdLevel",
    "UndergradMajor",
    #programing experiance
    'Hobbyist',
    'Age1stCode',
    "YearsCode",
    'YearsCodePro',
    'LanguageWorkedWith',
    'LanguageDesireNextYear',
    'NEWLearn',
    'NEWStuck',
    # Employment
    'Employment',
    'DevType',
    'WorkWeekHrs',
    'JobSat',
    'JobFactors',
    'NEWOvertime',
    'NEWEdImpt'
]


# In[36]:


len(selected_columns)


# Let's extract a copy of the data from these columns into a new data frame survey_df. We can continue to modify further without affecting the original data frame.
# 
# 

# In[37]:


survey_df = survey_raw_df[selected_columns].copy()


# In[38]:


schema=schema_raw[selected_columns]


# In[39]:


survey_df.shape


# In[40]:


survey_df.info()


# Most columns have the data type object, either because they contain values of different types or contain empty values (NaN). It appears that every column contains some empty values since the Non-Null count for every column is lower than the total number of rows (64461). We'll need to deal with empty values and manually adjust the data type for each column on a case-by-case basis.
# 
# Only two of the columns were detected as numeric columns (Age and WorkWeekHrs), even though a few other columns have mostly numeric values. To make our analysis easier, let's convert some other columns into numeric data types while ignoring any non-numeric value. The non-numeric are converted to NaN.

# In[41]:


survey_df.Age1stCode.unique()


# In[43]:


survey_df["Age1stCode"] = pd.to_numeric(survey_df.Age1stCode, errors = "coerce")
survey_df["YearsCode"] = pd.to_numeric(survey_df.YearsCode, errors = "coerce")
survey_df["YearsCodePro"] = pd.to_numeric(survey_df.YearsCodePro, errors = "coerce")          


# Let's now view some basic statistics about numeric columns.
# 
# 

# In[44]:


survey_df.info()


# In[45]:


survey_df.describe()


# There seems to be a problem with the age column, as the minimum value is 1 and the maximum is 279. This is a common issue with surveys: responses may contain invalid values due to accidental or intentional errors while responding. A simple fix would be to ignore the rows where the age is higher than 100 years or lower than 10 years as invalid survey responses. We can do this using the `.drop` method, [as explained here](https://www.geeksforgeeks.org/drop-rows-from-the-dataframe-based-on-certain-condition-applied-on-a-column/).

# In[47]:


survey_df.drop(survey_df[survey_df.Age< 10].index, inplace = True)
survey_df.drop(survey_df[survey_df.Age > 100].index, inplace = True)


# The same holds for WorkWeekHrs. Let's ignore entries where the value for the column is higher than 140 hours. (~20 hours per day).
# 
# 

# In[48]:


survey_df.drop(survey_df[survey_df.WorkWeekHrs > 140].index, inplace=True)


# The gender column also allows for picking multiple options. We'll remove values containing more than one option to simplify our analysis.

# In[49]:


survey_df["Gender"].value_counts()


# In[ ]:





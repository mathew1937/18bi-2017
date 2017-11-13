
# coding: utf-8

# # Martin Zemko: Mean daily temperature
# _1 November 2017_

# In[1]:


import pandas as pd


# In[2]:


dataframe = pd.read_excel('mean-daily-temperature-fisher-ri.xlsx',
                     header=0,
                     skiprows=14,
                     parse_cols=1,
                     names=['Date', 'Temperature'],
                     converters= {'Date': pd.to_datetime})


# ## Základná štatistiska datového súboru

# In[3]:


dataframe.info()


# In[4]:


dataframe.head()


# In[5]:


dataframe.describe()


# ## Prevzorkovanie časovej rady

# In[6]:


get_ipython().magic('matplotlib notebook')


# In[7]:


series = dataframe.set_index(['Date'])['Temperature']
series.resample('1M').mean().plot()


# ## Lineárna regresia

# In[8]:


import statsmodels.api as sm


# In[9]:


import numpy as np


# In[28]:


dataframe['Y'] = dataframe['Date'].apply(lambda x: x.year - 1988)
for m in range(1, 13):
    dataframe['M'+str(m)] = dataframe['Date'].apply(lambda x: 1 if x.month == m else 0)
X = dataframe.as_matrix()[:, 2:15]
X = X.astype(np.int32)
X


# In[29]:


y = dataframe['Temperature']


# In[30]:


model = sm.OLS(y, X)
results = model.fit()


# In[31]:


results.params.values


# In[32]:


dataframe['Fit'] = np.dot(X, results.params.values)


# In[33]:


series = dataframe.set_index(['Date'])[['Temperature', 'Fit']]
series.resample('1M').mean().plot()


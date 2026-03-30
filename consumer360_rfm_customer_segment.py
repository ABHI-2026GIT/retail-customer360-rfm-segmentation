#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[3]:


df = pd.read_csv(r"c:\Users\Lenovo\Downloads\cleaned_dataset_retail-project.csv")


# In[4]:


df.head()


# In[5]:


df.info()


# In[6]:


df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])


# In[7]:


df.info()


# In[16]:


# RFM Analysis


# In[8]:


reference_date = df["InvoiceDate"].max()


# In[39]:


print(reference_date)


# In[9]:


recency = df.groupby("CustomerID")["InvoiceDate"].max()
recency = (reference_date-recency).dt.days


# In[44]:


print(recency)


# In[10]:


frequency = df.groupby("CustomerID")["InvoiceNo"].count()


# In[48]:


print(frequency)


# In[ ]:





# In[11]:


monetary = df.groupby("CustomerID")["TotalPrice"].sum()


# In[51]:


print(monetary)


# In[ ]:





# In[12]:


rfm = pd.concat ([recency, frequency,monetary],axis=1)


# In[13]:


rfm.columns= ["recency","frequency","monetary"]
rfm.columns

rfm =  rfm.reset_index()
# In[14]:


print(rfm)


# In[ ]:





# In[19]:


rfm.head()


# In[72]:


# RFM Scoring


# In[15]:


rfm["R_score"] = pd.qcut(rfm["recency"],5,
                         labels =[5,4,3,2,1])


# In[16]:


rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method= "first"),5,
                         labels = [1,2,3,4,5])


# In[17]:


rfm["M_score"] = pd.qcut(rfm["monetary"],5,
                         labels = [1,2,3,4,5])


# In[18]:


rfm["RFM score"] = (rfm["R_score"].astype(str)+
                    rfm["F_score"].astype(str)+
                    rfm["M_score"].astype(str))


# In[19]:


rfm.head()


# In[20]:


rfm["RFM score"].value_counts()


# In[ ]:


# customer segmentation


# In[21]:


def segment_customer(row):
    r = row['R_score']
    f = row['F_score']
    m = row['M_score']

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    elif r >= 3 and f >= 4:
        return "Loyal Customers"

    elif r >= 4 and f >= 2 and m >= 2:
        return "Potential Loyalist"

    elif r >= 4 and f <= 2:
        return "Recent Users"

    elif r == 3 and f <= 2:
        return "Promising"

    elif r == 3 and f >= 3:
        return "Needs Attention"

    elif r == 2 and f <= 3:
        return "About To Sleep"

    elif r == 1 and f <= 2:
        return "Lost"

    elif r <= 2 and f >= 3:
        return "Hibernating"

    else:
        return "Price Sensitive"


# In[22]:


rfm["Segment"] = rfm.apply(segment_customer, axis=1)


# In[23]:


rfm["Segment"].value_counts()


# In[30]:


rfm.head()


# In[24]:


final_data = df.merge(rfm, on="CustomerID", how="left")


# In[25]:


final_data.head()


# In[26]:


final_data.to_csv(r"c:\Users\Lenovo\Downloads\consumer360_rfm_customer_segment.csv",index = False)


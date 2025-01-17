# -*- coding: utf-8 -*-
"""FacilityLocation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Iml-uQz1rMxM0_SsvAJPq76rcnJ7KzEC
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#from google.colab import drive
#drive.mount('/content/drive')



# Read the PIN Code Master file in a dataframe
print("Importing PIN Code Master ...")
dtypes={'Pincode':str}
df_pin = pd.read_csv(r'E:\FacilityLocation\DATA\pincode.csv',dtype=dtypes)
df_pin.info()

df_pin.drop(['OfficeName','OfficeType', 'Delivery'], axis=1, inplace=True)
# Remove duplicates and modify the original DataFrame
df_pin.drop_duplicates(subset=['Pincode'], keep='first', inplace=True)
df_pin.info()

# Read the HSN MASTER Excel file into a DataFrame
print("Importing HSN Code Master ...")
df_hsn = pd.read_excel('E:\FacilityLocation\DATA\HSN_MASTER.xlsx', sheet_name='Export Worksheet')
df_hsn.info()

df_hsn = df_hsn.astype({'HSN_CODE': 'str'})
df_hsn['hsncode']="@" + df_hsn['HSN_CODE']
df_hsn.rename(columns={'HSN_DESC': 'hsndesc'},inplace=True)
df_hsn.drop(['HSN_CODE'], axis=1, inplace=True)
df_hsn.head()

print("Importing E-Way Bill data for March 2024 ...")
dtypes = {'bharat_sir_eway_data_mar24_050424.start_pin': int, 'bharat_sir_eway_data_mar24_050424.destination_pin': int,'bharat_sir_eway_data_mar24_050424.origin_from_state': int,'bharat_sir_eway_data_mar24_050424.destination_from_state': int,'bharat_sir_eway_data_mar24_050424.rtn_period':str,'bharat_sir_eway_data_mar24_050424.travel_distance':int,'bharat_sir_eway_data_mar24_050424.transport_mode':str,'bharat_sir_eway_data_mar24_050424.hsn_code_4d':str,'bharat_sir_eway_data_mar24_050424.quantity':float,'bharat_sir_eway_data_mar24_050424.unit_quantity_code':str,'bharat_sir_eway_data_mar24_050424.amount':float,'bharat_sir_eway_data_mar24_050424.total_tax':float,'bharat_sir_eway_data_mar24_050424.ewbs_count':int,'bharat_sir_eway_data_mar24_050424.supplier_gstin_cnt':int}

df = pd.read_csv(r'E:\FacilityLocation\DATA\eway_data_mar24.csv',dtype=dtypes)
#df = pd.read_csv(r'E:\FacilityLocation\DATA\eway_data_mar24.csv',dtype=dtypes, nrows=10000)

df.rename(columns={'bharat_sir_eway_data_mar24_050424.start_pin': 'start_pin','bharat_sir_eway_data_mar24_050424.destination_pin':'dest_pin','bharat_sir_eway_data_mar24_050424.origin_from_state': 'start_statecode','bharat_sir_eway_data_mar24_050424.destination_from_state':'dest_statecode','bharat_sir_eway_data_mar24_050424.rtn_period':'mth','bharat_sir_eway_data_mar24_050424.travel_distance':'distance','bharat_sir_eway_data_mar24_050424.transport_mode':'mode','bharat_sir_eway_data_mar24_050424.hsn_code_4d':'hsn','bharat_sir_eway_data_mar24_050424.quantity':'qty','bharat_sir_eway_data_mar24_050424.unit_quantity_code':'uqc','bharat_sir_eway_data_mar24_050424.amount':'amount','bharat_sir_eway_data_mar24_050424.total_tax':'tax','bharat_sir_eway_data_mar24_050424.ewbs_count':'ewbs_cnt','bharat_sir_eway_data_mar24_050424.supplier_gstin_cnt':'supp_cnt'}, inplace=True)

# Define a dictionary mapping encoded values to their corresponding decoded values
decode_map = {'1': 'Road', '2': 'Rail', '3': 'Air', '4': 'Ship', '5': 'Multi Modal'}

# Replace the encoded categorical values with their decoded values
df['mode'] = df['mode'].replace(decode_map)

df = df.astype({'start_pin': 'str', 'dest_pin': 'str','start_statecode': 'str', 'dest_statecode': 'str'})

print(df.head())

print(df.shape)

print("Joining Datasets")
df1=pd.merge(df, df_pin, left_on='start_pin', right_on='Pincode', how='left')
df1.drop(['Pincode'], axis=1, inplace=True)
df1.rename(columns={'CircleName': 'start_circle','RegionName':'start_region','DivisionName':'start_division','District':'start_district','StateName':'start_state','Latitude':'start_lat','Longitude':'start_long'}, inplace=True)
df2=pd.merge(df1, df_pin, left_on='dest_pin', right_on='Pincode', how='left')
df2.drop(['Pincode'], axis=1, inplace=True)
df2.rename(columns={'CircleName': 'dest_circle','RegionName':'dest_region','DivisionName':'dest_division','District':'dest_district','StateName':'dest_state','Latitude':'dest_lat','Longitude':'dest_long'}, inplace=True)
df=pd.merge(df2, df_hsn, left_on='hsn', right_on='hsncode', how='left')
df.drop(['hsncode'], axis=1, inplace=True)
print(df.head())


#df.to_csv('SampleData.csv')

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

print("\nUnique values in categorical columns:")
for column in df.select_dtypes(include=['object']).columns:
    print(f"{column}: {df[column].nunique()} unique values")

print("\nSummary statistics:")
df.describe()

# Distribution of numerical columns

# Histograms for numerical columns
print("Histograms for numerical columns")
df["amount_cr"]=df["amount"]/1e8
numerical_columns=['distance','qty','amount_cr','tax','ewbs_cnt','supp_cnt']
for column in numerical_columns:
    plt.figure(figsize=(8, 6))
    df[column].hist(color='skyblue')
    plt.title("Frequency Distribution: " + column)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.grid(False)
    plt.show()



# Distribution of categorical columns
print("Distribution of categorical columns: Month & Mode")
categorical_columns=['mth','mode']
for column in categorical_columns:
    grouped = df.groupby(column)['amount'].count().reset_index()
    plt.bar(grouped[column], grouped['amount'])
    plt.title("Frequency Distribution : " + column)
    plt.xlabel('Category')
    plt.ylabel('Frequency')
    plt.grid(False)
    plt.show()

# Distribution of categorical columns: Horizontal Bar
print("Distribution of categorical columns: Horizontal Bar: Start & Destination State")
categorical_columns=['start_state','dest_state']
for column in categorical_columns:
    grouped = df.groupby(column)['amount'].count().reset_index()
    plt.barh(grouped[column], grouped['amount'])
    plt.title("Frequency Distribution : "+ column)
    plt.xlabel('Frequency')
    plt.ylabel('States')
    plt.grid(False)
    plt.show()

# Statistics on values against categorical columns
print("Statistics on values against categorical columns: Month & Mode")
categorical_columns={'mth','mode'}
for column in categorical_columns:
    grouped = df.groupby(column)['amount'].sum().reset_index()
    grouped['amount_cr']=grouped['amount']/1e8
    plt.bar(grouped[column], grouped['amount_cr'])
    plt.title("Value of Items under Movement : " + column)
    plt.xlabel('Category:'+ column)
    plt.ylabel('Amount (Cr. of Rs.)')
    plt.grid(False)
    plt.show()

# Statistics on values against categorical columns: Horizontal Bar
print("Statistics on values against categorical columns: Horizontal Bar: Start_district,Start_state,Dest_state")
categorical_columns={'start_state','dest_state'}
for column in categorical_columns:
    grouped = df.groupby(column)['amount'].sum().reset_index()
    grouped['amount_cr']=grouped['amount']/1e8
    plt.barh(grouped[column], grouped['amount_cr'])
    #df.groupby(column).sum('amount').plot(kind='bar')
    plt.title("Value of Items under Movement : " + column)
    plt.xlabel('Category')
    plt.ylabel('Amount (Cr. of Rs.) ')
    plt.grid(False)
    plt.show()

# Statistics on values against categorical columns
print("Pie Chart on Share of each Mode")
categorical_columns={'mode'}
df1=df.groupby(['mode']).sum('amount')
print(df1)
df1.plot(kind='pie',y='amount', autopct='%1.0f%%')
plt.title("Share of multiple Transport Modes")
plt.show()


#Top 5 states with highest value of Loading
print("Top 10 states with high value of Loading")
n = 10
grouped_start_state = df.groupby('start_state')['amount'].sum().reset_index()
grouped_start_state['amount_cr']=grouped_start_state['amount']/1e8
# Get the top n records
top_start_state = grouped_start_state.nlargest(n, 'amount_cr')
top_start_state.sort_values('amount_cr',inplace=True)
#print(f"\nTop {n} Loading")
#print(top_start_state['amount_cr'])
plt.barh(top_start_state['start_state'], top_start_state['amount_cr'])
plt.title('Top  10 Originating State')
plt.ylabel('State')
plt.xlabel('Amount (Cr. of Rs.)')
plt.grid(False)
plt.show()

#Top 20 Districts with highest value of Loading
print("Top 20 Districts with highest value of Loading")
n = 20
grouped_start_district = df.groupby('start_district')['amount'].sum().reset_index()
grouped_start_district['amount_cr']=grouped_start_district['amount']/1e8
# Get the top n records
top_start_district = grouped_start_district.nlargest(n, 'amount_cr')
top_start_district.sort_values('amount_cr',inplace=True)

#print(f"\nTop {n} Loading")
#print(top_start_district['amount_cr'])
plt.barh(top_start_district['start_district'], top_start_district['amount_cr'])
plt.title('Top 20 Originating District')
plt.ylabel('District')
plt.xlabel('Amount (Cr. of Rs.)')
plt.grid(False)
plt.show()

print(top_start_district)



#Top 50 HSN with highest value of Loading
print("Top 50 HSN with highest value of Loading")
n = 50
grouped_hsn = df.groupby('hsn')['amount'].sum().reset_index()
grouped_hsn['amount_cr']=grouped_hsn['amount']/1e8
# Get the top n records
top_hsn = grouped_hsn.nlargest(n, 'amount_cr')
top_hsn.sort_values('amount_cr',inplace=True)
#print(f"\nTop {n} Loading")
#print(top_hsn['amount_cr']
plt.figure(figsize=(8, 12))  # Width: 8 inches, Height: 10 inches
plt.barh(top_hsn['hsn'], top_hsn['amount_cr'])
plt.title('Top 50 HSN with High value of Loading')
plt.xlabel('Amount (Cr. of Rs.)')
plt.ylabel('HSN')
plt.grid(False)
plt.show()

# Correlation Matrix
print("Plotting Correlation Matrix")
# Select only numeric columns
numeric_df = df.select_dtypes(include=[np.number])
numeric_df.drop(['amount_cr'],axis=1, inplace=True)
numeric_df.head()

# Compute the correlation matrix
corr_matrix = numeric_df.corr()

# Display the correlation matrix
print("\nCorrelation Matrix:")
print(corr_matrix)

# Set up the matplotlib figure
plt.figure(figsize=(10, 8))

# Draw the heatmap
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)

# Add title and labels
plt.title('Correlation Matrix')
plt.show()
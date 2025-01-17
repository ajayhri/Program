# -*- coding: utf-8 -*-
"""FacilityLocation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Iml-uQz1rMxM0_SsvAJPq76rcnJ7KzEC

## **Importing Libraries**
"""
print('Importing Libraries ...')
import pandas as pd
import os
import matplotlib.pyplot as plt

"""##**Reading csv File**"""

#from google.colab import drive
#drive.mount('/content/sample_data')
#os.chdir('/content/drive/MyDrive/FacilityLocation/Data')

print('Reading csv file ...')
dtypes = {'START_PIN': str, 'DEST_PIN':str, 'START_STATECODE': str,'DEST_STATECODE': str,'MTH':str,'DISTANCE':int,'MODE':str,'HSN':str,'QTY':float,'UQC':str,'AMOUNT':float,'TAX':float,'EWBS_CNT':int,'SUPP_CNT':int, 'DISTANCERANGE':str}

df = pd.read_csv(r'E:\FacilityLocation\DATA\eway_final.csv',dtype=dtypes, encoding='latin-1')

# Define the desired order of modes
mode_order = ['Multi Modal','Air', 'Ship','Rail','Road']

# Define the distance slab order
#dist_slab_order = ['Upto 200 Km.','Between 200 and 500 Km.', 'Between 500 and 1000 Km.','Between 1000 and 2000 Km.','More than 2000 Km.']

# Define a dictionary of colors for each mode
mode_colors = {
    'Road': 'red',
    'Rail': 'green',
    'Air': 'orange',
    'Ship': 'blue',
    'Multi Modal': 'purple'
}

# Define the function to categorize ages
def categorize_distance(dist_range):
    if dist_range == 'Upto 200 Km.':
        return 'SLAB 0: Upto 200 Km.)'
    elif dist_range == 'Between 200 and 500 Km.':
        return 'SLAB 1: Between 200 and 500 Km.'
    elif dist_range == 'Between 500 and 1000 Km.':
        return 'SLAB 2: Between 500 and 1000 Km.'
    elif dist_range == 'Between 1000 and 2000 Km.':
        return 'SLAB 3: Between 1000 and 2000 Km.'
    elif dist_range == 'More than 2000 Km.':
        return 'SLAB 4: More than 2000 Km.'
    else:
        return 'SLAB -1: Invalid data'



"""##**Data Exploration**"""

# Shape of Data
print('Shape of Data')
print(df.shape)

# Data Structure
print('Structure of Data')
print(df.info())

#  Data
print('Sample Data')
print(df.head(5))

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

print("\nUnique values in categorical columns:")
for column in df.select_dtypes(include=['object']).columns:
    print(f"{column}: {df[column].nunique()} unique values")

#Summary statistics
print('Data Statistics')
print(df.describe())



"""##**Distribution of Columns**



"""

# Distribution of numerical columns

# Histograms for numerical columns
numerical_columns=['DISTANCE','QTY','AMOUNT','TAX','EWBS_CNT','SUPP_CNT']
for column in numerical_columns:
    plt.figure(figsize=(8, 6))
    df[column].hist(color='skyblue')
    plt.title(column)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.grid(False)
    plt.show()

# Distribution of categorical columns
categorical_columns=['MTH','MODE', 'START_STATE','DEST_STATE']
for column in categorical_columns:
    grouped = df.groupby(column)['AMOUNT'].count().reset_index()
    grouped.sort_values('AMOUNT',ascending=False,inplace=True)
    plt.bar(grouped[column], grouped['AMOUNT'])
    plt.title(column)
    plt.xlabel('Category')
    plt.ylabel('Frequency')
    plt.xticks(rotation=90)
    plt.grid(False)
    plt.show()

"""### **Statistics on Values against Categorical Columns**"""

grouped = df.groupby(['MTH','MODE'])['AMOUNT'].sum().reset_index()
grouped.sort_values('AMOUNT',ascending=False,inplace=True)
grouped['AMOUNT_CR']=grouped['AMOUNT']/1e8
# Create a pivot table
pivot_table = grouped.pivot(index='MTH', columns='MODE', values='AMOUNT')
# Reorder the pivot table based on the desired order
pivot_table = pivot_table.reindex(columns=mode_order)
# Create the stacked bar chart
pivot_table.plot(kind='bar', stacked=True, color=mode_colors)
# Add label and Title
plt.title('Stacked Bar Chart of Amount by Mode and Month')
plt.xlabel('MONTH')
plt.ylabel('Amount (in Cr. of Rs.)')
#plt.xticks(rotation=90)
plt.grid(False)
plt.show()

# Statistics on values against States
categorical_columns={'START_STATE','DEST_STATE'}
for column in categorical_columns:
    grouped = df.groupby([column,'MODE'])['AMOUNT'].sum().reset_index()
    grouped[column]=grouped[column].replace(['THE DADRA AND NAGAR HAVELI AND DAMAN AND DIU','ANDAMAN AND NICOBAR ISLANDS'],['DADRA,N H& DIU','A&N ISLANDS'])
    grouped['AMOUNT_CR']=grouped['AMOUNT']/1e8
    # Create a pivot table
    pivot_table = grouped.pivot(index=column, columns='MODE', values='AMOUNT')
    # Reorder the pivot table based on the desired order
    pivot_table = pivot_table.reindex(columns=mode_order)
    # Sort pivot table by total Amount in Ascending order
    pivot_table['Total'] = pivot_table.sum(axis=1)
    pivot_table = pivot_table.sort_values(by='Total', ascending=True)
    # Drop the 'Total' column after sorting
    pivot_table = pivot_table.drop(columns='Total')
    # Create the stacked bar chart
    pivot_table.plot(kind='barh', stacked=True, color=mode_colors)
    # Add label and Title
    plt.title('Stacked Bar Chart of Amount by Mode and '+ column)
    #plt.barh(grouped[column], grouped['AMOUNT_CR'])
    plt.title(column)
    plt.xlabel('State')
    plt.xlabel('Amount (in Cr. of Rs.)')
    #plt.xticks(rotation=90)
    plt.grid(False)
    plt.show()

# Statistics on values against State Pairs
n=25


grouped_state_pair = df.groupby(['START_STATE','DEST_STATE','MODE'])['AMOUNT'].sum().reset_index()
grouped_state_pair['START_STATE']=grouped_state_pair['START_STATE'].replace(['THE DADRA AND NAGAR HAVELI AND DAMAN AND DIU','ANDAMAN AND NICOBAR ISLANDS'],['DADRA,N H& DIU','A&N ISLANDS'])
grouped_state_pair['DEST_STATE']=grouped_state_pair['DEST_STATE'].replace(['THE DADRA AND NAGAR HAVELI AND DAMAN AND DIU','ANDAMAN AND NICOBAR ISLANDS'],['DADRA,N H& DIU','A&N ISLANDS'])
grouped_state_pair['STATEPAIR']=grouped_state_pair['START_STATE']+'-'+ grouped_state_pair['DEST_STATE']
grouped_state_pair['AMOUNT_CR']=grouped_state_pair['AMOUNT']/1e8
grouped_state_pair = grouped_state_pair.drop(columns='START_STATE')
grouped_state_pair = grouped_state_pair.drop(columns='DEST_STATE')
# Get the top n records
top_state_pair = grouped_state_pair.nlargest(n, 'AMOUNT_CR')
top_state_pair.sort_values('AMOUNT_CR',inplace=True)

top_state_pair.sort_values('AMOUNT_CR',inplace=True)

#print(f"\nTop {n} State Pair")
#print(top_state_pair)
# Create a pivot table
pivot_table = top_state_pair.pivot(index='STATEPAIR', columns='MODE', values='AMOUNT_CR')
# Reorder the pivot table based on the desired order
pivot_table = pivot_table.reindex(columns=mode_order)
# Sort pivot table by total Amount in Ascending order
pivot_table['Total'] = pivot_table.sum(axis=1)
pivot_table = pivot_table.sort_values(by='Total', ascending=True)
# Drop the 'Total' column after sorting
pivot_table = pivot_table.drop(columns='Total')
# Create the stacked bar chart
pivot_table.plot(kind='barh', stacked=True, color=mode_colors)

# Add label and Title
plt.title('OD State Pair wise Value of Movement')
plt.xlabel('State Pair')
plt.xlabel('Amount (in Cr. of Rs.)')
plt.grid(False)
plt.show()

# Statistics on values against categorical columns
categorical_columns={'MODE'}
df1=df.groupby(['MODE']).sum('AMOUNT')
df1.plot(kind='pie',y='AMOUNT', autopct='%1.0f%%')

#Distance Slab wise Value of Loading

grouped_dist_slab= df.groupby(['DISTANCERANGE','MODE'])['AMOUNT'].sum().reset_index()
grouped_dist_slab['AMOUNT_CR']=grouped_dist_slab['AMOUNT']/1e8
grouped_dist_slab['SLAB'] = grouped_dist_slab['DISTANCERANGE'].apply(categorize_distance)
grouped_dist_slab.sort_values(by='SLAB', ascending=False, inplace=True)

# Create a pivot table
pivot_table = grouped_dist_slab.pivot(index='SLAB', columns='MODE', values='AMOUNT_CR')
pivot_table = pivot_table.sort_values(by='SLAB', ascending=False)

# Create the stacked bar chart
#plt.figure(figsize=(20, 12))  # Width: 8 inches, Height: 10 inches
pivot_table.plot(kind='barh', stacked=True, color=mode_colors)
plt.title('Distance Slab wise Value of Movement')
plt.xlabel('Amount (Cr. of Rs.)')
plt.ylabel('Distance Slab')
plt.grid(False)
plt.show()



#Top 50 HSN with highest value of Loading
n = 50
grouped_hsn = df.groupby(['HSN','MODE'])['AMOUNT'].sum().reset_index()
grouped_hsn['AMOUNT_CR']=grouped_hsn['AMOUNT']/1e8
# Get the top n records
top_hsn = grouped_hsn.nlargest(n, 'AMOUNT_CR')
top_hsn.sort_values('AMOUNT_CR',inplace=True)
#print(f"\nTop {n} Loading")
#print(top_hsn)

# Create a pivot table
pivot_table = top_hsn.pivot(index='HSN', columns='MODE', values='AMOUNT_CR')
# Reorder the pivot table based on the desired order
pivot_table = pivot_table.reindex(columns=mode_order)
# Sort pivot table by total Amount in Ascending order
pivot_table['Total'] = pivot_table.sum(axis=1)
pivot_table = pivot_table.sort_values(by='Total', ascending=True)
# Drop the 'Total' column after sorting
pivot_table = pivot_table.drop(columns='Total')
plt.figure(figsize=(20, 12))  # Width: 8 inches, Height: 10 inches
# Create the stacked bar chart
pivot_table.plot(kind='barh', stacked=True, color=mode_colors)


#plt.figure(figsize=(8, 12))  # Width: 8 inches, Height: 10 inches
plt.title('Top 50 HSN')
plt.xlabel('Amount (Cr. of Rs.)')
plt.ylabel('HSN')
plt.grid(False)
plt.show()

#Top 20 Originating PIN with highest value of Loading
n = 20
grouped_start_pin = df.groupby(['START_PIN','MODE'])['AMOUNT'].sum().reset_index()
grouped_start_pin['AMOUNT_CR']=grouped_start_pin['AMOUNT']/1e8
# Get the top n records
top_start_pin = grouped_start_pin.nlargest(n, 'AMOUNT_CR')
top_start_pin.sort_values('AMOUNT_CR',inplace=True)

# Create a pivot table
pivot_table = top_start_pin.pivot(index='START_PIN', columns='MODE', values='AMOUNT_CR')
# Reorder the pivot table based on the desired order
pivot_table = pivot_table.reindex(columns=mode_order)
# Sort pivot table by total Amount in Ascending order
pivot_table['Total'] = pivot_table.sum(axis=1)
pivot_table = pivot_table.sort_values(by='Total', ascending=True)
# Drop the 'Total' column after sorting
pivot_table = pivot_table.drop(columns='Total')
plt.figure(figsize=(20, 12))  # Width: 8 inches, Height: 10 inches
# Create the stacked bar chart
pivot_table.plot(kind='barh', stacked=True, color=mode_colors)


plt.title('Top 20 Originating PIN')
plt.xlabel('Amount (Cr. of Rs.)')
plt.ylabel('PIN')
plt.grid(False)
plt.show()

#Top 20 Districts with highest value of Loading
n = 20
grouped_start_district = df.groupby(['START_DISTRICT','MODE'])['AMOUNT'].sum().reset_index()
grouped_start_district['AMOUNT_CR']=grouped_start_district['AMOUNT']/1e8
# Get the top n records
top_start_district = grouped_start_district.nlargest(n, 'AMOUNT_CR')
top_start_district.sort_values('AMOUNT_CR',inplace=True)

# Create a pivot table
pivot_table = top_start_district.pivot(index='START_DISTRICT', columns='MODE', values='AMOUNT_CR')
# Reorder the pivot table based on the desired order
pivot_table = pivot_table.reindex(columns=mode_order)
# Sort pivot table by total Amount in Ascending order
pivot_table['Total'] = pivot_table.sum(axis=1)
pivot_table = pivot_table.sort_values(by='Total', ascending=True)
# Drop the 'Total' column after sorting
pivot_table = pivot_table.drop(columns='Total')
plt.figure(figsize=(20, 12))  # Width: 8 inches, Height: 10 inches
# Create the stacked bar chart
pivot_table.plot(kind='barh', stacked=True, color=mode_colors)

plt.title('Top 20 Originating District')
plt.xlabel('Amount (Cr. of Rs.)')
plt.ylabel('District')
plt.grid(False)
plt.show()

#Top 20 Destination Pin with highest value of Loading
n = 20
grouped_dest_pin = df.groupby(['DEST_PIN','MODE'])['AMOUNT'].sum().reset_index()
grouped_dest_pin['AMOUNT_CR']=grouped_dest_pin['AMOUNT']/1e8
# Get the top n records
top_dest_pin = grouped_dest_pin.nlargest(n, 'AMOUNT_CR')
top_dest_pin.sort_values('AMOUNT_CR',inplace=True)

# Create a pivot table
pivot_table = top_dest_pin.pivot(index='DEST_PIN', columns='MODE', values='AMOUNT_CR')
# Reorder the pivot table based on the desired order
pivot_table = pivot_table.reindex(columns=mode_order)
# Sort pivot table by total Amount in Ascending order
pivot_table['Total'] = pivot_table.sum(axis=1)
pivot_table = pivot_table.sort_values(by='Total', ascending=True)
# Drop the 'Total' column after sorting
pivot_table = pivot_table.drop(columns='Total')
plt.figure(figsize=(20, 12))  # Width: 8 inches, Height: 10 inches
# Create the stacked bar chart
pivot_table.plot(kind='barh', stacked=True, color=mode_colors)

plt.title('Top 20 Destination PIN')
plt.xlabel('Amount (Cr. of Rs.)')
plt.ylabel('PIN')
plt.grid(False)
plt.show()

#Top 20 Districts with highest value of UnLoading
n = 20
grouped_dest_district = df.groupby(['DEST_DISTRICT','MODE'])['AMOUNT'].sum().reset_index()
grouped_dest_district['AMOUNT_CR']=grouped_dest_district['AMOUNT']/1e8
# Get the top n records
top_dest_district = grouped_dest_district.nlargest(n, 'AMOUNT_CR')
top_dest_district.sort_values('AMOUNT_CR',inplace=True)

# Create a pivot table
pivot_table = top_dest_district.pivot(index='DEST_DISTRICT', columns='MODE', values='AMOUNT_CR')
# Reorder the pivot table based on the desired order
pivot_table = pivot_table.reindex(columns=mode_order)
# Sort pivot table by total Amount in Ascending order
pivot_table['Total'] = pivot_table.sum(axis=1)
pivot_table = pivot_table.sort_values(by='Total', ascending=True)
# Drop the 'Total' column after sorting
pivot_table = pivot_table.drop(columns='Total')
plt.figure(figsize=(20, 12))  # Width: 8 inches, Height: 10 inches
# Create the stacked bar chart
pivot_table.plot(kind='barh', stacked=True, color=mode_colors)

plt.title('Top 20 Destination District')
plt.xlabel('Amount (Cr. of Rs.)')
plt.ylabel('District')
plt.grid(False)
plt.show()

#Top 5 OD-Pair with highest value of Loading
n = 5

grouped_od_pair = df.groupby(['START_DISTRICT','DEST_DISTRICT','MODE'])['AMOUNT'].sum().reset_index()
grouped_od_pair['AMOUNT_CR']=grouped_od_pair['AMOUNT']/1e8
# Get the top n records
top_od_pair = grouped_od_pair.nlargest(n, 'AMOUNT_CR')
top_od_pair.sort_values('AMOUNT_CR',inplace=True)
top_od_pair['ODPAIR']=top_od_pair['START_DISTRICT']+'-'+ top_od_pair['DEST_DISTRICT']

# Create a pivot table
pivot_table = top_od_pair.pivot(index='ODPAIR', columns='MODE', values='AMOUNT_CR')
# Reorder the pivot table based on the desired order
pivot_table = pivot_table.reindex(columns=mode_order)
# Sort pivot table by total Amount in Ascending order
pivot_table['Total'] = pivot_table.sum(axis=1)
pivot_table = pivot_table.sort_values(by='Total', ascending=True)
# Drop the 'Total' column after sorting
pivot_table = pivot_table.drop(columns='Total')
plt.figure(figsize=(20, 12))  # Width: 8 inches, Height: 10 inches
# Create the stacked bar chart
pivot_table.plot(kind='barh', stacked=True, color=mode_colors)

plt.title('Top 20 Origin-Destination District Pair by Total Amount')
plt.xlabel('Amount (Cr. of Rs.)')
plt.ylabel('District')
plt.grid(False)
plt.show()

maxhsn=3
for ind in top_od_pair.index:
    #print(top_od_pair['START_DISTRICT'][ind], top_od_pair['DEST_DISTRICT'][ind])
    df_filtered=df[(df['START_DISTRICT']==top_od_pair['START_DISTRICT'][ind]) & (df['DEST_DISTRICT']==top_od_pair['DEST_DISTRICT'][ind])]

    grouped_hsn = df_filtered.groupby(['HSN','MODE'])['AMOUNT'].sum().reset_index()
    grouped_hsn['AMOUNT_CR']=grouped_hsn['AMOUNT']/1e8


    # Get the top n records
    n = min(maxhsn,len(grouped_hsn)) # Ensure n is not greater than the number of unique HSN
    top_hsn = grouped_hsn.nlargest(n, 'AMOUNT_CR')
    top_hsn.sort_values('AMOUNT_CR',inplace=True)

    # Create a pivot table
    pivot_table = top_hsn.pivot(index='HSN', columns='MODE', values='AMOUNT_CR')
    # Reorder the pivot table based on the desired order
    pivot_table = pivot_table.reindex(columns=mode_order)
    # Sort pivot table by total Amount in Ascending order
    pivot_table['Total'] = pivot_table.sum(axis=1)
    pivot_table = pivot_table.sort_values(by='Total', ascending=True)
    # Drop the 'Total' column after sorting
    pivot_table = pivot_table.drop(columns='Total')
    # Create the stacked bar chart
    pivot_table.plot(kind='barh', stacked=True, color=mode_colors)

    plt.title('Top 3 HSN loaded for OD-Pair   ' + top_od_pair['ODPAIR'][ind] )
    plt.xlabel('Amount (Cr. of Rs.)')
    # Wrap the y-axis labels
    #plt.yticks([textwrap.fill(label, width=20) for label in top_hsn['HSNDTL']])
    plt.ylabel('HSN')
    plt.grid(False)
    plt.show()
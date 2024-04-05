#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 14:46:29 2024

@author: danielhill
"""

import pandas as pd

#File path
file_path = '/Users/danielhill/Documents/MSc Data Science/Interdisciplinary group project/Data/Air_quality_continuous_(pre-2023).csv'

# Read CSV into a dataframe
df = pd.read_csv(file_path)

# Convert the 'Date_Time' column to datetime object, replacing out-of-bounds values with NA
df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], errors='coerce')

#Filter to remove unneeded columns
columns_to_remove = ['LOCATION', 'INSTRUMENT_TYPE', 'CUR', 'OBJECTID', 'NOX']
filtered_df = df.drop(columns=columns_to_remove)

# Filter df to include only non-NA date values
filtered_df = filtered_df[filtered_df['DATE_TIME'].notna()]

# Filter df to include only data from 1st January 2017 to 31st December 2022 (inclusive)
filtered_df2 = filtered_df[(filtered_df['DATE_TIME'] >= '2017-01-01') & (filtered_df['DATE_TIME'] <= '2022-12-22')]

# Filter df to remove rows with missing values in 'Site_ID' column
filtered_df3 = filtered_df2.dropna(subset=['SITE_ID'])

# Filter df to remove rows where datetime and siteID are duplicated, keeping the second occurrence
df_no_duplicates = filtered_df3.drop_duplicates(subset=['DATE_TIME', 'SITE_ID'], keep='last')

#Drop datetime and temperature columns to test for negative values
df_neg_test = df_no_duplicates.drop(['DATE_TIME'], axis=1)

# Check for negative values in each column
negative_values_mask = df_neg_test < 0

# Check if any negative values are present in each column
columns_with_negatives = negative_values_mask.any()

# Display columns with negative values
print("\nColumns with negative values:")
print(columns_with_negatives)

#Remove rows that contain a negative value, column by column
filtered_df4 = df_no_duplicates.loc[~(df_no_duplicates['NO2'] < 0)]  
filtered_df4 = filtered_df4.loc[~(filtered_df4['NO'] < 0)]
filtered_df4 = filtered_df4.loc[~(filtered_df4['PM10'] < 0)]
filtered_df4 = filtered_df4.loc[~(filtered_df4['PM2_5'] < 0)]

#Re-testing to ensure that all negative values have been removed
df_neg_test2 = filtered_df4.drop(['DATE_TIME'], axis=1)
negative_values_mask2 = df_neg_test2 < 0
columns_with_negatives2 = negative_values_mask2.any()

print("\nColumns with negative values:")
print(columns_with_negatives2)

# Group by month and calculate the mean for NO2, NO, PM10 and PM2_5 columns
monthly_data = filtered_df4.groupby(filtered_df4['DATE_TIME'].dt.to_period('M'))[['NO2', 'NO', 'PM10', 'PM2_5']].mean()

# Save the DataFrame to a CSV file
monthly_data.to_csv('/Users/danielhill/Documents/MSc Data Science/Interdisciplinary group project/Data/Air_quality_monthly.csv')



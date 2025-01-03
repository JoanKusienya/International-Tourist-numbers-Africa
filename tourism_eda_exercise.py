# -*- coding: utf-8 -*-
"""Tourism EDA Exercise.ipynb

"""

import pandas as pd


url = "https://raw.githubusercontent.com/JoanKusienya/International-Tourist-numbers-Africa/main/Tourism%20Data.csv"
url1 = "https://raw.githubusercontent.com/JoanKusienya/International-Tourist-numbers-Africa/main/Metadata_Country.csv"

df = pd.read_csv(url)
df1 = pd.read_csv(url1)

print(df.info())
print(df.describe())

print(df1.info())
print(df1.describe())

print(df.isnull().sum())

"""# Missing Values"""

columns_to_keep = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'] + [str(year) for year in range(2010, 2020)]
df_recent = df[columns_to_keep]
df_recent.head()

"""#  Merge datasets
Columns to keep and Df containing Income groups, regions
"""

df_all= pd.merge(df_recent,df1, on= "Country Code")
df_all.head()

"""# Data Preprocessing

Remove noise(punctuation, lowercase, unnamed columns)

"""

import re
def remove_punctuation(text):
    if isinstance(text, str):
        return re.sub(r'[^\w\s]', '', text)
    return text

#lowercase all info
df_punct=df_all.apply(lambda x: x.str.lower() if x.dtype == "object" else x)

#Remove Punctuation
df_clean= df_punct.apply(lambda x: x.apply(remove_punctuation) if x.dtype == "object" else x)
df_clean

# Drop Unnamed column
dff=df_clean.loc[:, ~df_clean.columns.str.contains('^Unnamed')]
dff.head()

"""# Format your dataset: African Countries"""

!pip install country_list

"""Extract data for african countries only"""

df_africa = dff[dff['Region'].str.contains('africa', na=False)]

# Display the DataFrame
df_africa.head()

#Compare countries in dataset, df_africa with those in the african country list


#Create country list for african countries
africa1 = {'Country': [
    'algeria', 'angola', 'benin', 'botswana', 'burkina faso', 'burundi',
    'cabo verde', 'cameroon', 'central african republic', 'chad', 'comoros',
    'congo dem rep', 'congo rep', 'djibouti',
    'egypt arab rep', 'equatorial guinea', 'eritrea', 'eswatini', 'ethiopia', 'gabon',
    'gambia the', 'ghana', 'guinea', 'guineabissau', 'cote divoire', 'kenya',
    'lesotho', 'liberia', 'libya', 'madagascar', 'malawi', 'mali', 'mauritania',
    'mauritius', 'morocco', 'mozambique', 'namibia', 'niger', 'nigeria', 'rwanda',
    'sao tome and principe', 'senegal', 'seychelles', 'sierra leone', 'somalia',
    'south africa', 'south sudan', 'sudan', 'tanzania', 'togo', 'tunisia', 'uganda',
    'zambia', 'zimbabwe'
]}

african_countries = pd.DataFrame(africa1)

#Remove countries in df_africa that are in the Middle East
me_countries= df_africa[~df_africa['Country Name'].isin(african_countries['Country'])]
df_me=pd.DataFrame(me_countries)
df_me

# Update the Region column to "Middle East" for df_me
df_me['Region'] = 'middle east'
df_me

# Remove Middle Eastern countries from dataframe
df_africa1= df_africa = df_africa[~df_africa['Country Name'].isin(df_me['Country Name'])]

#Update region name for north african countries
df_africa1.loc[df_africa1['Region'].str.contains('middle east', case=False, na=False), 'Region'] = 'north africa'
df_africa1.head()

"""# **African Regions & Countries**"""

# Split the regions into East, West, Central, North, and Southern African countries
north_africa = ['egypt arab rep', 'libya', 'tunisia', 'algeria', 'morocco', 'sudan']
west_africa = ['nigeria', 'ghana', 'senegal', 'mali', 'benin', 'burkina faso', 'cabo verde', 'cote divoire', 'gambia the', 'guinea', 'guineabissau', 'liberia', 'niger', 'mauritania', 'sierra leone', 'togo']
central_africa = ['congo dem rep', 'congo rep', 'cameroon', 'gabon', 'equatorial guinea', 'sao tome and principe', 'chad', 'angola', 'central african republic']
east_africa = ['kenya', 'tanzania', 'uganda', 'ethiopia', 'south sudan', 'somalia', 'seychelles', 'rwanda', 'eritrea','mauritius', 'comoros', 'burundi', 'djibouti', 'madagascar']
southern_africa = ['south africa', 'namibia', 'botswana', 'zimbabwe', 'malawi', 'mozambique', 'zambia', 'lesotho', 'eswatini']

def updated_africa_region(df_africa1):
    # Dictionary of regions
    africa_region = {
        'north africa': north_africa,
        'west africa': west_africa,
        'central africa': central_africa,
        'east africa': east_africa,
        'southern africa': southern_africa
    }

    print(type(africa_region))

    # Map each country to its region
    country_to_region = {country: region for region, countries in africa_region.items() for country in countries}

    # Update the DataFrame with region info
    df_africa1['Region'] = df_africa1['Country Name'].map(country_to_region)

    # Fill missing values in 'Region' column if any
    df_africa1['Region'] = df_africa1['Region'].fillna(df_africa1['Region'])

    # Return the updated DataFrame
    return df_africa1

updated_africa_region(df_africa1).head()

#Regions in my data
df_updated= updated_africa_region(df_africa1)
df_updated['Region'].unique()

"""# **EDA:**

**1.Average Tourism Numbers for African Countries**
"""

df_updated.head()

# Add a column with the average tourist numbers for each country btn 2010-2019
years = [str(year) for year in range(2010, 2020)]

df_updated[years] = df_updated[years].apply(pd.to_numeric, errors='coerce')

# average tourist numbers
df_updated['Avg Tourist Numbers'] = df_updated[years].mean(axis=1)

# Group by country and calculate the average
df_updated.groupby(['Country Name', 'IncomeGroup', 'Region','Avg Tourist Numbers'])[['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']].mean().reset_index()

"""**Fill year columns (Nan) with average tourist numbers**

Drop countries without any data for all the years
"""

for year in years:
    if year in df_updated.columns:
       df_updated.dropna(how='all', inplace=True)
df_updated.head()

df_avg=df_updated.groupby(['Country Name', 'IncomeGroup', 'Region','Avg Tourist Numbers'])[['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']].mean().reset_index()
df_avg.head()

"""**Visualize the data**"""

#Create a Chloropleth Map
import plotly.express as px


fig = px.choropleth(
    df_avg,
    locations='Country Name',
    locationmode='country names',
    color='Avg Tourist Numbers',
    hover_name='Country Name',
    title='Average Tourist Numbers for African Countries',
    color_continuous_scale=px.colors.sequential.Plasma,
    scope='africa'
)
# Show the figure
fig.show()

"""# **Tourism Performance for African countries between 2010-2019**"""

# Convert years to numeric
df_avg.iloc[:, 4:] = df_avg.iloc[:, 4:].apply(pd.to_numeric, errors='coerce')

# Create Parallel Coordinates Plot
fig = px.parallel_coordinates(df_avg,
                               color='Avg Tourist Numbers',
                               labels={"Avg Tourist Numbers": "Average Tourist Numbers"},
                               dimensions=['2010', '2011', '2012', '2013', '2014',
                                           '2015', '2016', '2017', '2018', '2019'],
                               title='Parallel Coordinates Plot of Tourist Numbers by Year')

fig.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Calculate the average tourist numbers across the years
df_avg['Average Tourist Numbers'] = df_avg[years].mean(axis=1)

# Sort the DataFrame by Average Tourist Numbers in descending order
df_sorted = df_avg.sort_values(by='Average Tourist Numbers', ascending=False)

# Create a color palette
palette = sns.color_palette("husl", len(df_sorted))

# Create the bar chart
plt.figure(figsize=(12, 8))
sns.barplot(x='Average Tourist Numbers', y='Country Name', data=df_sorted, palette=palette)

# Set titles and labels
plt.title('Average Tourist Numbers by Country (2010-2019)', fontsize=16)
plt.xlabel('Average Tourist Numbers', fontsize=14)
plt.ylabel('Country Name', fontsize=14)

# Show the plot
plt.grid(axis='x')
plt.tight_layout()
plt.show()

"""## **Tourist Numbers by region(2010-2019)**

**Average Tourist Numbers by Region(2010-2019)**
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Bar Chart for North Africa in Descending order
plt.figure(figsize=(12, 6))
north_africa = df_avg[df_avg['Region'] == 'north africa'].sort_values(by='Avg Tourist Numbers', ascending=False)
sns.barplot(x='Avg Tourist Numbers', y='Country Name', data=north_africa, palette='viridis')
plt.title('Average Tourist Numbers in North Africa ')
plt.xlabel('Avg Tourist Numbers')
plt.ylabel('Country Name')
plt.grid(True)
plt.show()

#2. Bar Chart for West Africa
plt.figure(figsize=(12, 6))
west_africa = df_avg[df_avg['Region'] == 'west africa']
west_africa_sorted = west_africa.sort_values(by='Avg Tourist Numbers', ascending=False)

sns.barplot(x='Avg Tourist Numbers', y='Country Name', data=west_africa_sorted, palette='viridis')
plt.title('Average Tourist Numbers in West Africa')
plt.xlabel('Avg Tourist Numbers')
plt.ylabel('Country Name')
plt.grid(True)
plt.show()

# 3. Pie Chart for Central Africa
plt.figure(figsize=(10, 7))
central_africa = df_avg[df_avg['Region'] == 'central africa'].groupby('Country Name')['Avg Tourist Numbers'].sum()
plt.pie(central_africa, labels=central_africa.index, autopct='%1.1f%%', startangle=140)
plt.title('Tourist Numbers Distribution in Central Africa')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
# 4. Bar Plot for East Africa in Descending Order
plt.figure(figsize=(12, 6))
southern_africa = df_avg[df_avg['Region'] == 'east africa']
southern_africa_sorted = southern_africa.sort_values(by='Avg Tourist Numbers', ascending=False)

sns.barplot(x='Avg Tourist Numbers', y='Country Name', data=southern_africa_sorted, palette='viridis')
plt.title('Average Tourist Numbers in East Africa')
plt.xlabel('Avg Tourist Numbers')
plt.ylabel('Country Name')
plt.grid(True)
plt.show()

#5. Heatmap for Southern Africa
plt.figure(figsize=(12, 6))
southern_africa = df_avg[df_avg['Region'] == 'southern africa'].sort_values(by='Avg Tourist Numbers', ascending=False)
sns.heatmap(southern_africa[['Country Name', 'Avg Tourist Numbers']].set_index('Country Name'), annot=True, cmap='YlGnBu')
plt.title('Heatmap of Average Tourist Numbers in Southern Africa (Descending Order)')
plt.xlabel('Average Tourist Numbers')
plt.ylabel('Country Name')
plt.show()

"""**Countries with the highest tourist numbers in each region(2010-2019)**"""

import pandas as pd
import matplotlib.pyplot as plt

# Ensure that the columns for years are numeric
df_avg.iloc[:, 4:] = df_avg.iloc[:, 4:].apply(pd.to_numeric, errors='coerce')

# Calculate the sum of tourist numbers for each country from 2010 to 2019
df_avg['Total Tourist Numbers'] = df_avg[years].sum(axis=1)

# Define the regions
regions = df_avg['Region'].unique()

# Create a plot for each region
plt.figure(figsize=(16, 12))

for region in regions:
    plt.subplot(3, 2, list(regions).index(region) + 1)  # Create subplots for each region
    top_countries = df_avg[df_avg['Region'] == region].nlargest(5, 'Total Tourist Numbers')

    for index, row in top_countries.iterrows():
        plt.plot(years, row[years], marker='o', label=row['Country Name'])

    plt.title(f'Top 5 Countries in {region} (2010-2019)')
    plt.xlabel('Year')
    plt.ylabel('Tourist Numbers')
    plt.xticks(rotation=45)
    plt.legend(title='Countries', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)

plt.tight_layout()
plt.show()

"""# **Countries with Highest Tourist Numbers per Income Group(2010-2019)**

**Performance of various countries per income group**
"""

df_avg['IncomeGroup'].unique()

# Tourist Numbers depending on Income group


df_avg.iloc[:, 4:] = df_avg.iloc[:, 4:].apply(pd.to_numeric, errors='coerce')

df_avg[years].mean(axis=1)

# Define the income groups
income_groups = ['high income','upper middle income', 'lower middle income', 'low income', ]

# Create a plot for each income group
plt.figure(figsize=(16, 12))

for income_group in income_groups:
    plt.subplot(2, 2, income_groups.index(income_group) + 1)  # Create subplots for each income group
    top_countries = df_avg[df_avg['IncomeGroup'] == income_group].nlargest(7, 'Avg Tourist Numbers')

    for index, row in top_countries.iterrows():
        plt.plot(years, row[years], marker='o', label=row['Country Name'])

    plt.title(f'Top 5 Countries in {income_group} (2010-2019)')
    plt.xlabel('Year')
    plt.ylabel('Tourist Numbers')
    plt.xticks(rotation=45)
    plt.legend(title='Countries', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)

plt.tight_layout()
plt.show()

"""Top countries in the different regions

High Income Country: Seychelles

Upper Middle Income Countries: South Africa

Lower Middle Icome Countries: Morocco

Low Income: Mozambique
"""

df_avg.iloc[:, 4:] = df_avg.iloc[:, 4:].apply(pd.to_numeric, errors='coerce')

# Define income groups
income_groups = df_avg['IncomeGroup'].unique()

# Prepare a figure
plt.figure(figsize=(15, 10))

for income_group in income_groups:
    # Filter top country for each income group based on Avg Tourist Numbers
    top_country = df_avg[df_avg['IncomeGroup'] == income_group].nlargest(1, 'Avg Tourist Numbers')

    # Get years and values for line plot
    years = list(map(str, range(2010, 2020)))
    tourist_numbers = top_country[years].values.flatten()

    # Create a subplot for each income group
    plt.subplot(len(income_groups), 1, list(income_groups).index(income_group) + 1)

    # Bar plot for average tourist numbers
    sns.barplot(x=years, y=tourist_numbers, color='b', alpha=0.6, label='Average Tourist Numbers')

    # Line plot for the same data
    plt.plot(years, tourist_numbers, marker='o', linestyle='-', color='r', label='Tourist Trend')

    # Customize the plot
    plt.title(f'Top Country in {income_group} Income Group', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Tourist Numbers', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()

"""Visualize the best performing country for each income group by its tourist numbers across the years

# **Anova : Statistical Analysis**

**Statistical analysis for the regions**
"""

from scipy import stats

north_africa = df_avg[df_avg['Region']== 'north africa']['Avg Tourist Numbers']
west_africa = df_avg[df_avg['Region'] == 'west africa']['Avg Tourist Numbers']
east_africa = df_avg[df_avg['Region'] == 'east africa']['Avg Tourist Numbers']
central_africa= df_avg[df_avg['Region']=='central africa']['Avg Tourist Numbers']
southern_africa=df_avg[df_avg['Region']=='southern africa']['Avg Tourist Numbers']

# Perform the ANOVA
f_stat, p_value = stats.f_oneway(north_africa, west_africa, east_africa, central_africa, southern_africa)

print(f"F-statistic: {f_stat}, P-value: {p_value}")

"""**Statistical analysis of the income groups**"""

low_income = df_avg[df_avg['IncomeGroup'] == 'low income']['Avg Tourist Numbers']
lower_middle_income = df_avg[df_avg['IncomeGroup'] == 'lower middle income']['Avg Tourist Numbers']
upper_middle_income = df_avg[df_avg['IncomeGroup'] == 'upper middle income']['Avg Tourist Numbers']
high_income = df_avg[df_avg['IncomeGroup'] == 'high income']['Avg Tourist Numbers']

# Perform the ANOVA
f_stat, p_value = stats.f_oneway(low_income, lower_middle_income, upper_middle_income, high_income)

print(f"F-statistic: {f_stat}, P-value: {p_value}")

"""# **Tourism Performance for Kenya (2010-2019)**

**Extract data for Kenya**
"""

df_kenya = df_avg[df_avg['Country Name'] == 'kenya']

df_kenya

"""**Combined bar chart and line graph to show the tourism trend (2010-2019)**"""

import numpy as np
values = df_kenya.iloc[0, 4:14].values

# Define the years
years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

# Create a colormap
colors = plt.cm.viridis(np.linspace(0, 1, len(years)))

plt.figure(figsize=(10, 6))

# Plot the bar chart
bars = plt.bar(years, values, color=colors, alpha=0.7, label='Tourist Numbers')

# Plot the line chart
plt.plot(years, values, marker='o', linestyle='-', color='r', alpha=0.7, label='Trend Line')

# Customize the plot
plt.title('Tourist Numbers in Kenya (2010-2019)', fontsize=16)
plt.xlabel('Year')
plt.ylabel('Number of Tourists')
plt.legend()
plt.grid(True)

plt.show()

"""# EDA Using Sweetviz"""

pip install sweetviz

import pandas as pd
import sweetviz as sv
report = sv.analyze(df_avg)

# Generate report

#report.show_html('sweetviz_report.html')


International Tourism Statistics- Africa

**A. Project Overview 📝**
Goal of the project:
To assess the tourism performance of various African countries (2010-2019)

**B.Data Cleaning and Preparation** 🔧
Missing Value Treatment:

Dropped all columns with missing values (all), Unnamed columns
Data preprocessing:
- Removed noise, lowercase str
- Merged the 2 datasets on Country code(common column)
- Dropped all extra columns not in use
  
**C. Exploratory Data Analysis**
Bivariate Analysis:
- African Countries against average tourism numbers(2010-2019).
- Plot a map of Africa) with (avg tourist numbers) for easier visualization.
- Tourism performance for Kenya(2010-2019)
Multivariate Analysis:
- Top 5 countries with the highest, average tourist numbers per region(2010-2019)
- Top 7 countries with the highest tourist numbers cumulatively(2010-2019) per income group
- Compare the top countries for each income group against each other, view the tourism trend
- Statistical analysis of the income groups and regions

**D. Insights**
1. Most African countries have an average of 300,000 tourists per year
2. South Africa and North African countries average have the most international tourists
3. Per Region:
   
a. Morocco has had a consistently positive linear relationship

b. Central African countries experienced a dip (2018) and then a slight spike (2019)

c. West African countries(missing data- filled with mean), positive linear with a spike in 2015

d. Southern African countries, South Africa has the highest number consistently by a huge margin

e. East Africa, apart from Kenya(leading) and Tanzania, these countries experienced a slight decline in 2018

4, Per Income Group

a. High Income: Seychelles is the only country

b. Upper Middle Income: South Africa leads Algeria by a considerable margin

c. Lower Middle Income: Morocco and Egypt seem to tie in 2019, Egypt has come from behind. Kenya(6th)

d. Low Income: East African countries seem to fall in this group, Mozambique leads but takes a sharp dip in 2019.

5. Top countries per income group trend analysis:
-South Africa(Upper Middle Income), the most international tourists overall, positive trend

- Morocco(Lower Middle Income), positive trend
  
- Mozambique(Low Middle Income), fluctuated 2016-2019
  
- Seychelles(High Income), Positive trend

6. Kenya
  
- Decline in tourist numbers between 2011-2015
  
- Positive trend in tourism numbers from 2016
  
- Kenya seems to be the leading tourist destination in East Africa based on income and regional analysis.


**E. Hypothesis Testing and Insights 🎯**
Statistical Tests Used: Anova
Findings and Insights:
a. Regions
- F-statistic of 6.43 suggests that there is a noticeable difference between the means of the regions.
  
-A p-value of 0.000393 is much smaller than the common significance level of 0.05. (reject the null hypothesis)
This indicates that there are statistically significant differences in the average tourist numbers among the regions.

b. Income Groups
- F-statistic of 2.66 suggests that there are some differences between the means of the income groups, but they may not
be very pronounced.

- Since the p-value is slightly above 0.05, you cannot reject the null hypothesis at the 5% significance level. This suggests that there is no statistically significant difference in the average tourist numbers
among the different income groups at the 5% level. However, the p-value is quite close to 0.05, indicating that there might be a trend worth exploring
further.

**F. Final Report and Presentation 📑**
Key Findings:
- There are regional disparities with South Africa(Country) and North African countries
attracting more tourists.

-There is a margin of tourist numbers between Central and East African countries
vs North and Southern African countries.

-There is a great decline in tourist numbers in Kenya between 2011-2015, which may be as a result of new policies under the newly promulgated 2010 constitution.
Limitations of the Analysis:
Missing values for most countries and years

**Recommendations and Next Steps:**

-Improve data collection to reduce missing data

- Conduct a more in-depth analysis of the factors contributing to the success of top-performing countries in each income group to identify replicable strategies.



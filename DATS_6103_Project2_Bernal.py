#!/usr/bin/env python
# coding: utf-8

# #                        DATS 6103 - Fall 2020 - Daniel Bernal

# # Individual Project #2 - Analysis of Telecommunications Infrastructure
# 

# # Introduction

# For this project I have selected to analyze aspects of telecommunications infrastructure. This is a sector that has been seen as a key driver that brings opportunity for growth in many sectors of an economy. There is a significant number of researches that have focused on different aspects at a country and industry level. For this analysis we will be focusing on 62 countries for the 2000-2018 period.
# 
# 
# Data
# 
# I opted to obtain the data from the [The World Bank's World Development Indicators](https://databank.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG/1ff4a498/Popular-Indicators#advancedDownloadOptions) because it is a reliable source and because it possesses a great variety of data related to the selected topic.
# 
# Series names include: 
# 
# - Access to electricity (% of population)
# - Computer, communications and other services (% of commercial service exports)
# - Computer, communications and other services (% of commercial service imports)
# - ICT goods exports (% of total goods exports)
# - ICT goods imports (% total goods imports)
# - ICT service exports (% of service exports, BoP)
# - ICT service exports (BoP, current USD)
# - Secure Internet servers (per 1 million people)
# - Individuals using the Internet (% of population)
# - Fixed telephone subscriptions (per 100 people)
# - GDP per capita (current USD)
# - Access to electricity, rural (% of rural population)
# - Mobile cellular subscriptions (per 100 people)
# 

# # Import Python Packages

# In[1]:


import pandas as pd
import plotly #Main tool used for graphing the data
import chart_studio.plotly as py
import plotly.express as px


# # 1. Read the CSV File

# In[2]:


df = pd.read_csv('tecommunications.csv')


# # 2. Data Manipulation

# # 2.1 Modifying Variable Names

# The data is obtained with the original series names. For better handling, the original names are replaced with short variables names. To do so, we pass a dictionary with the original names and replace all of them.

# In[3]:


df['series'].replace({'Access to electricity (% of population)': 'elect_total',
'Computer, communications and other services (% of commercial service exports)': 'com_serv_exp',
'Computer, communications and other services (% of commercial service imports)': 'com_serv_imp',
'ICT goods exports (% of total goods exports)': 'ictgoodsexp',
'ICT goods imports (% total goods imports)': 'ictgoodsimp',
'ICT service exports (% of service exports, BoP)': 'ictserv_exp',
'ICT service exports (BoP, current US$)': 'ictserv_exp_usd',
'Secure Internet servers (per 1 million people)': 'sec_internet',
'Individuals using the Internet (% of population)': 'internet_usage',
'Fixed telephone subscriptions (per 100 people)': 'phone_usage',
'Mobile cellular subscriptions (per 100 people)': 'mobile_usage',
'GDP per capita (current US$)': 'gdppc',
'Access to electricity, rural (% of rural population)': 'elect_rural'}, inplace=True)


# # 2.2 Assigning Regions to Each Country

# Each country is assigned a region which is the continent where they are located. The purpose of it is to have a categorical variable that allows us to make associations by region.
# 
# For this study, countries such as Russia, Azerbaijan, and Turkey are classified in the European region, while Egypt is classified in the African region.
# 
# To perform execute this, we pass a dictionary that includes each country with its respective region.

# In[4]:


country_classif = {'Albania': 'Europe', 'Algeria': 'Africa', 'Argentina': 'Latin America', 'Armenia': 'Asia',
 'Australia': 'Oceania', 'Austria': 'Europe', 'Azerbaijan': 'Europe', 'Barbados': 'North America', 'Belgium': 'Europe',
 'Brazil': 'Latin America', 'Bulgaria': 'Europe', 'Cameroon': 'Africa', 'Canada': 'North America', 'Chile': 'Latin America',
 'China': 'Asia', 'Colombia': 'Latin America', 'Croatia': 'Europe', 'Czech Republic': 'Europe', 'Cyprus': 'Europe',
 'Denmark': 'Europe', 'Ecuador': 'Latin America', 'Egypt, Arab Rep.': 'Africa', 'France': 'Europe', 'Germany': 'Europe',
 'Greece': 'Europe', 'Hungary': 'Europe', 'India': 'Asia', 'Iceland': 'Europe', 'Ireland': 'Europe', 'Israel': 'Asia',
 'Italy': 'Europe', 'Japan': 'Asia', 'Korea, Rep.': 'Asia', 'Moldova': 'Europe', 'Morocco': 'Africa', 'Monaco': 'Europe',
 'Netherlands': 'Europe', 'Nepal': 'Asia', 'Nigeria': 'Africa', 'Norway': 'Europe', 'Pakistan': 'Asia', 'Paraguay': 'Latin America',
 'Panama': 'Latin America', 'Peru': 'Latin America', 'Poland': 'Europe', 'Portugal': 'Europe', 'Philippines': 'Asia', 'Qatar': 'Asia',
 'Russian Federation': 'Europe', 'Saudi Arabia': 'Asia', 'Singapore': 'Asia', 'Slovenia': 'Europe', 'South Africa': 'Africa',
 'Spain': 'Europe', 'Sweden': 'Europe', 'Switzerland': 'Europe', 'Turkey': 'Europe', 'United States': 'North America',
 'United Kingdom': 'Europe', 'United Arab Emirates': 'Asia', 'Uruguay': 'Latin America', 'Vietnam': 'Asia'}


# We add the column 'region' to the dataframe by maping (map()) each country with a region.
# 
# Following that, we re-assign the order of the columns for the data frame.

# In[5]:


df['region'] = df['country'].map(country_classif)
df = df[['country','code','region','series','2000','2001','2002','2003','2004','2005','2006',
         '2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']]


# # 3. Analysis

# The methodology used is based on creating dataframes from the original dataframe. Once each dataframe is created, we query the needed information.
# 
# As an example we create a GDP per Capita dataframe that later will be used for the analysis.

# In[6]:


gdppc = df.loc[(df['series'] == 'gdppc')]
gdppc = gdppc.drop(['series'], axis=1)
gdppc = pd.melt(gdppc, id_vars=['country','code','region'], var_name="year", value_name="gdppc")
gdppc.head(5)


# # 3.1 Access to Electricity

# The electricity is certainly a main determinant for the production of goods and services, it represents an impact not only in telecommunications but also in areas like health, education, food, and poverty reduction. As electricity has a vital meaning in an economy we have seen that some countries are still not able to provide access to its entire population over the years.
# 
# Some factors could be: 
# 
# - Household income(not able to afford it)
# - Geographical location - represent technical challenges to deliver the service

# # Access for Rural Population
# 
# Findings: 
# 
# - A significant increase is evidenced over the years.
# - As of 2018, countries such as Peru, Nigeria, South Africa and Pakistan have levels under 90%.

# In[7]:


#Create a dataframe for the series needed
elect_rural = df.loc[(df['series'] == 'elect_rural')] 
elect_rural = elect_rural.drop(['series','region'], axis=1) #Dropping columns that are not needed
#Use melt() to modify the structure of the dataframe
elect_rural = pd.melt(elect_rural, id_vars=['country','code'], var_name='year', value_name='elect_rural')

#Creating a choropleth map with plotly with a year animation to illustrate the the change in levels over the years
elect1 = px.choropleth(elect_rural, #We use the dataframe defined above with the series needed
                   locations='code', #The country code will help plotly to identify the location for each country
                    #The country codes are included in the datasets when they are obtained from the world bank
                   color = 'elect_rural', #Indicating that the color will change according to the variable values
                   animation_frame= 'year', #Animation will be based from year to year
                    hover_name='country', #Will help to display information for each country when the cursor is placed over it
                   color_continuous_scale='Magma', #Color selection
                    projection='natural earth', #This is one type of projection of the globe
                   labels=dict(elect_rural='Access to Electricity - Rural'))
#Assign the transition time for each year
elect1.update_layout(transition = {'duration': 50000}, title_text = 'Access to Electricity in the Rural Areas')
elect1.show()


# # Access for Total Population
# 
# 
# Findings:
# 
# - Countries have been able to increase the access level over years
# - There are still countries in Latin America, Africa, and Asia that still haven't been able to achieve 99% levels

# In[8]:


#The approach selected is identical to the one performed to display the access for rural population

#Defining the dataframe with the data needed
elect_total = df.loc[(df['series'] == 'elect_total')]
elect_total = elect_total.drop(['series','region'], axis=1)
elect_total = pd.melt(elect_total, id_vars=['country','code'], var_name='year', value_name='elect_total')

#Creating a choropleth map with a year animation
elect2 = px.choropleth(elect_total,
                   locations='code',
                   color = 'elect_total',
                   animation_frame= 'year',
                    hover_name="country",
                   color_continuous_scale='Magma',
                    projection='natural earth',
                   labels=dict(elect_total='Access to Electricity'))
elect2.update_layout(transition = {'duration': 50000}, title_text = 'Access to Electricity as a Percent of Total Population')
elect2.show()


# # 3.2 Imports and Exports of ICT Goods (% of Total Goods)
# 
# ICT stands for Information and Communication Technology. Evidently ICT goods represents a booster in productivity, and countries have different policies regarding sponsorships to promote the developments of such. Accross the globe we see that some countries are exporters while other are big importers.
# 
# Findings:
# - Latin America, Africa, and Oceania seem to have the countries with less movement in both, imports and exports.
# - As expected, Asian countries such as Singapore, Philipines, China, South Korea, and Vietnam have been big importers and exporters compared to the other countries included in this analysis. This may indicate strong investment initiatives.

# In[11]:


#We create, re-organize, and merge the dataframes that contains the data for imports, exports, and GDP per capita
#Dataframe for imports
ictgoodsimp = df.loc[(df['series'] == 'ictgoodsimp')]
ictgoodsimp = ictgoodsimp.drop(['series'], axis=1)
ictgoodsimp = pd.melt(ictgoodsimp, id_vars=['country','code','region'], var_name="year", value_name='ictgoodsimp')

#Dataframe for exports
ictgoodsexp = df.loc[(df['series'] == 'ictgoodsexp')]
ictgoodsexp = ictgoodsexp.drop(['series'], axis=1)
ictgoodsexp = pd.melt(ictgoodsexp, id_vars=['country','code','region'], var_name='year', value_name='ictgoodsexp')

#Merge all the data
#We use the previously created dataframe for GDP per capita 
gdp_ict = pd.merge(gdppc, ictgoodsimp, how='left', on=['country', 'code', 'region','year'])
gdp_ict = pd.merge(gdp_ict, ictgoodsexp, how='left', on=['country', 'code', 'region','year']).dropna()

#Create a scatter plot with plotly to compare imports and exports
#We use the years as the animation
#GDP per capita is included in the size for each dot
#Each dot represents a country
#Colors of the plots represent the region where they belong to
gdpict = px.scatter(gdp_ict, x='ictgoodsexp', y='ictgoodsimp', animation_frame='year', animation_group='country',size='gdppc',
                hover_name='country',color='region', size_max=40, range_x=[-3,60], range_y=[-3,60], 
                 labels=dict(ictgoodsexp='ICT Goods Exports - Percentage of Exports', ictgoodsimp='ICT Goods Imports - Percentage of Imports',
                gdppc='GDP Per Capita',region='Region'))
gdpict.update_layout(transition = {'duration': 50000}, title_text = 'Comparison of ICT Percent of Goods Imports vs Percent of Goods Exports')
gdpict.show()


# # 3.3 Imports and Exports of Computer, Communications and other Services
# 
# It represents a measurement of international commercial services related to this sector. 
# 
# Findings:
#  - European countries have been big importers over time.
#  - Asian countries represent the biggest exporters of such services.
#  - Africa shows more tendencies of importing compared to exporting services.

# In[18]:


#We create, re-organize, and merge the dataframes that contains the data for imports and exports
#Dataframe for exports
com_serv_exp = df.loc[(df['series'] == 'com_serv_exp')]
com_serv_exp = com_serv_exp.drop(['series'], axis=1)
com_serv_exp = pd.melt(com_serv_exp, id_vars=['country','code','region'], var_name="year", value_name='com_serv_exp')

#Dataframe for imports
com_serv_imp = df.loc[(df['series'] == 'com_serv_imp')]
com_serv_imp = com_serv_imp.drop(['series'], axis=1)
com_serv_imp = pd.melt(com_serv_imp, id_vars=['country','code','region'], var_name="year", value_name='com_serv_imp')

#Merging the dataframes
comm_comp = pd.merge(com_serv_imp, com_serv_exp, how='left', on=['country', 'code', 'region','year']).dropna()

#Similarly to 3.2, we use a scatter plot but in this opportunity we are not putting GDP per capita in context
#We separate the countries by region
comserv = px.scatter(comm_comp, x='com_serv_exp', y='com_serv_imp', animation_frame='year',facet_col='region', animation_group='country',
                hover_name='country',color='region', size_max=60, range_x=[-3,100], range_y=[-3,100], 
                 labels=dict(com_serv_exp='Exports', com_serv_imp='Imports',region='Region'))
comserv.update_layout(transition = {'duration': 50000}, title_text = 'Comparison of Imports and Exports of Computers, Communications and other Services')
comserv.show()


# # 3.4 Biggest ICT Service Exporters
# 
# We continue by analyzing ICT services. In this section will take a look at the historical top exporters in USD. Based on the top exporters we will look at their historical values in terms of percentages of all services that they export.
# 
# Findings: 
# - India has been the top ICT service exporter among all countries followed by Ireland and the US.
# - 6 European countries included in the top ten. Making Europe the region with the most spending. 
# - From the western world, the US is the biggest exporter of ICT services.
# 

# In[24]:


#Create a dataframe for ICT service exports in USD
ictserv_exp_usd = df.loc[(df['series'] == 'ictserv_exp_usd')]
ictserv_exp_usd = ictserv_exp_usd.drop(['series'], axis=1)
ictserv_exp_usd = pd.melt(ictserv_exp_usd, id_vars=['country','code','region'], var_name="year", value_name="ictserv_exp_usd").dropna()

#Create a datafame to identify the total exports for all the countries for all the years and selecting the top ten countries
ictserv_exp_usdtop = ictserv_exp_usd.groupby(['country','region']).sum()
ictserv_exp_usdtop= ictserv_exp_usdtop.sort_values(by='ictserv_exp_usd', ascending = False).reset_index()
ictserv_exp_usdtop = ictserv_exp_usdtop[:10] #After sorting, we select the top ten

#Create a list of the top countries and use it to query their year by year values(please note that this is not adding values)
top_countries = list(ictserv_exp_usdtop['country'])
ict_top = ictserv_exp_usd[ictserv_exp_usd['country'].isin(top_countries)]

#Create a stacked bar plot for the top ten countries, we display the total over years and the total for each year
#Totals for each year can be observed when the cursor is pointed over a specific box
exp1 = px.bar(ict_top, x='country', y='ictserv_exp_usd', title="Top Ten Countries in ICT Service Exports - USD from 2000 to 2017",
            labels=dict(ictserv_exp_usd='ICT Service Exports - USD', country='Country'), hover_name="year")
#Updating bar and line colors and style
exp1.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)

#We create a pie chart to display the total over years for each country
#In addition, countries are grouped by region and the total values for each one of them.
exp2 = px.sunburst(ictserv_exp_usdtop, path=['region', 'country'], values='ictserv_exp_usd',
                  title='Top Ten Countries in ICT Service Exports - USD Grouped by Region')


exp1.show()
exp2.show()


# We create a line plot and illustrate the top countries and their respective ICT service exports values as a percent of service exports.
# 
# Findings:
# - ICT service exports represent a big share of service exports for India, Ireland and Israel.

# In[23]:


#Create the dataframe for the data needed
ictserv_exp = df.loc[(df['series'] == 'ictserv_exp')]
ictserv_exp = ictserv_exp.drop(['series'], axis=1)
ictserv_exp = pd.melt(ictserv_exp, id_vars=['country','code','region'], var_name="year", value_name="ictserv_exp")

#Some 2018 values are missing so I decided to not include them
ictserv_exp = ictserv_exp[ictserv_exp['year'] < '2018']

#Query the countries included in the top ten exporters previously
ictserv_top = ictserv_exp[ictserv_exp['country'].isin(top_countries)].dropna()

#We create a line plot to display the values over these years and compare in between countries
servexp = px.line(ictserv_top, x="year", y="ictserv_exp", color='country',line_group="country", hover_name="country",
              title="ICT Service Exports as a Percent of Service Exports for the Top Ten in Exports - USD",
            labels=dict(ictserv_exp='ICT Service Exports % of Service Exports', country='Country', year='Year'))

servexp.show()


# # 3.5 Internet Usage
# 
# We continue with analyzing a very important factor in telecommunications. There are two main variables in this section that include the percentage of total population that uses the internet a amount of secure internet servers per 1 million people.
# 
# Findings:
# 
# - Despite being a top country in ICT service exports, India shows very poor levels of internet access for its population. The association between these two variables is unknown, however, we can clearly identify a relationship between this and a low GDP per capita. One possible reason could be a lack of income to afford internet. 
# - In 2018, non of these countries went over 70% of internet access.
# - Panama has a significantly higher GDP per capita but its internet percentages are low.
# - Countries like Algeria, India, Egypt, and Paraguay, in addition to having low internet access percentages, they also have signifcantly low secure internet servers.

# In[25]:


#Create dataframe for internet usage only for the year 2018 as it is the most recent data point available
internet_usage = df.loc[(df['series'] == 'internet_usage')]
internet_usage = internet_usage.drop(['series'], axis=1)
internet_usage = pd.melt(internet_usage, id_vars=['country','code','region'], var_name="year", value_name="internet_usage")
internet_usage = internet_usage[internet_usage['year'] == '2018']

#Merge internet usage data with GDP data to illustrate relationships
#We select the the bottom countries in this opportunity
gdp_internet = pd.merge(gdppc, internet_usage, how='left', on=['country', 'code', 'region','year'])
gdp_internet = gdp_internet.sort_values(by='internet_usage', ascending=True).dropna()
gdp_internet = gdp_internet[:10]

#We create a dataframe only for the year 2018 to illustrate the number of secure servers
sec_internet = df.loc[(df['series'] == 'sec_internet')]
sec_internet = sec_internet.drop(['series'], axis=1)
sec_internet = pd.melt(sec_internet, id_vars=['country','code','region'], var_name="year", value_name="sec_internet")
sec_internet = sec_internet[sec_internet['year'] == '2018']

#Merge secure servers data with GDP to illustrate the bottom 10 countries
gdp_secinternet = pd.merge(gdppc, sec_internet, how='left', on=['country', 'code', 'region','year'])
gdp_secinternet = gdp_secinternet.sort_values(by='sec_internet', ascending=True).dropna()
gdp_secinternet = gdp_secinternet[:10]

#Create a choropleth graph to illustrate the levels of internet access in 2018 for all the countries
inte = px.choropleth(internet_usage,
                   locations='code',
                   color = 'internet_usage',
                    hover_name="country",
                   color_continuous_scale='Magma',
                    projection='natural earth',
                   labels=dict(internet_usage='Internet Usage'),
                   title = 'Percentage of Total Population that Uses the Internet in 2018')

#Create a bar graph to display the bottom countries for internet access and its respective levels of GDP per capita
inte1 = px.bar(gdp_internet, x='country', y='internet_usage',
             hover_data=['internet_usage', 'gdppc'], color='gdppc', height=500, 
             title='Percentage of Total Population that Uses the Internet in 2018 - Bottom Countries',
            labels=dict(internet_usage='Internet Usage', country='Country', gdppc='GDP Per Capita'))

#Create a bar graph to display the bottom countries for secure internet server and its respective levels of GDP per capita
inte2 = px.bar(gdp_secinternet, x='country', y='sec_internet',
             hover_data=['sec_internet', 'gdppc'], color='gdppc', height=500, 
             title='Number of Secure Internet Servers per 1 Million People in 2018 - Bottom Countries',
            labels=dict(sec_internet='Secure Internet Servers', country='Country', gdppc='GDP Per Capita'))


inte.show()

inte1.show()

inte2.show()


# # 3.6 Mobile and Fixed Phone Usage
# 
# Findings:
# 
# - Evidently, there is a significant decline in fixed phone subscriptions.
# - Two particular cases, Monaco and Canada. Despite their increase in mobile subscriptions, these countries are keeping the fixed phone subscriptions values considerably high over the years.
# - Several countries that have had low numbers, they also have the tendency of having low GDP levels.

# In[27]:


#Create dataframe for fixed phone subscriptions
phone_usage = df.loc[(df['series'] == 'phone_usage')]
phone_usage = phone_usage.drop(['series'], axis=1)
phone_usage = pd.melt(phone_usage, id_vars=['country','code','region'], var_name="year", value_name='phone_usage')

#Create a dataframe for mobile phone subscriptions
mobile_usage = df.loc[(df['series'] == 'mobile_usage')]
mobile_usage = mobile_usage.drop(['series'], axis=1)
mobile_usage = pd.melt(mobile_usage, id_vars=['country','code','region'], var_name="year", value_name='mobile_usage')

#Sorting by countries that in 2018 had less mobile phone subscriptions
less_usage = mobile_usage.loc[(mobile_usage['year'] == '2018')]
less_usage = less_usage.sort_values(by='mobile_usage', ascending=True).dropna()
less_usage = less_usage[:10]
less_usage_countries = list(less_usage['country'])

#Sorting by countries that in 2018 had more mobile phone subscriptions
more_usage = mobile_usage.loc[(mobile_usage['year'] == '2018')]
more_usage = more_usage.sort_values(by='mobile_usage', ascending=False).dropna()
more_usage = more_usage[:10]

#Merging mobile and fixed phone data for countries that had less mobile phone subscriptions
phone_data = (pd.merge(phone_usage, mobile_usage, how='left', on=['country', 'code', 'region','year']))
phone_data = phone_data[phone_data['country'].isin(less_usage_countries)].dropna()

#Create a bar graph for the countries with less mobile phone susbscriptions
phone1 = px.bar(less_usage, x='mobile_usage', y='country',orientation='h', 
              title="Mobile Phone Subscriptions per 100 People in 2018 - Bottom Countries",
            labels=dict(mobile_usage='Mobile Subscriptions', country='Country'), hover_name="country")
phone1.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)

#Create a bar graph for countries with more mobile phone subscriptions
phone2 = px.bar(more_usage, x='mobile_usage', y='country',orientation='h', 
              title="Mobile Phone Subscriptions per 100 People in 2018 - Top Countries",
            labels=dict(mobile_usage='Mobile Subscriptions', country='Country'), hover_name="country")
phone2.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)

#Create animated bar graph for changes over time for countries with less mobile subscriptions
phone3 = px.bar(phone_data, x='mobile_usage', y='country',orientation='h', animation_frame='year',
             hover_data=['country','mobile_usage', 'phone_usage'], color='phone_usage', height=500, 
             title='Change of Mobile Subscriptions vs Fixed Subscriptions',
             range_x=[0,150],
            labels=dict(mobile_usage='Mobile Subscriptions', country='Country', phone_usage='Fixed Phone Subscriptions'))
phone3.update_layout(transition = {'duration': 50000})

phone2.show()
phone1.show()
phone3.show()


# # 4. Conclusion
# 
# 
# We have seen that countries that have tendency of higher GDP per Capita levels tend to have the stronger infrastructure overall. 
# Asian countries are among the top importers and exporters of ICT goods, while Latin American, African and Oceanian countries tend to have the opposite behavior.
# 
# In terms of telecommunication services, Europeans are considered big importers over the years while Asian countries such as India have been presenting very high numbers of exports over time. Additionally, exports of these services represent a very high percentage of total service exports for countries such as Ireland, Israel, and India.
# 
# Lastly, while looking at the internet and phone usage, despite the overall increase over time, the tendency shows that countries from Latin America, Africa and some from Asia have low levels of usage, in which not surprisingly, these are also among the group with the lowest GDP per capita levels.
# 

# # 5. References
# 
# 
# The World Bank Group. (2018, April 18). Retrieved from Access to Energy is at the Heart of Development: https://www.worldbank.org/en/news/feature/2018/04/18/access-energy-sustainable-development-goal-7
# 
# Lapatinas, A. (2018). The effect of the internet on economic sophistication: An empirical analysis. Economic Letters, 1-4.
# 
# Choi, C., & Yi, M. H. (2009). The effect of the Internet on economic growth: Evidence from cross-country panel data. Economics Letters, 39-41.

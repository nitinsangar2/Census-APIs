#This is the script we use to download data from the Census API. The census API urls change often so there are many listed here to call the different variables/tables we needed for analysis.
#It is recommend to make API calls state-by-state so as not to cause server timeout.


import pandas as pd
import requests
import json
#we generated this API key for the research center
apikey = "[Your Census key]"
#Each of these base APIs have different syntax. 
baseAPI = "https://api.census.gov/data/2017/acs/acs5?get=NAME,%s&for=tract:*&in=state:%s&key=[Your Census key]"
baseAPI1 = "https://api.census.gov/data/2017/acs/acs1?get=NAME,group(S0801)&for=tract:*&key=[Your Census key]"
baseAPI2 = "https://api.census.gov/data/2017/acs/acs1/subject?get=NAME,S0801_C01_046E&for=tract:*&for=state:01&key=[Your Census key]"
api3 = "https://api.census.gov/data/2017/acs/acs1?get=NAME,S0801_C01_046E&for=state:*&key=[Your Census key]"
#This is to get education table 
api4 = "https://api.census.gov/data/2017/acs/acs5?get=NAME,group(B15002)&for=tract:*&in=state:%s&key=[Your Census key]"
#Poverty
poverty_api = "https://api.census.gov/data/2017/acs/acs5?get=NAME,group(C17002)&for=tract:*&in=state:%s&key=[Your Census key]"
#Unemployed
unemployed_api = "https://api.census.gov/data/2017/acs/acs5?get=NAME,group(B23001)&for=tract:*&in=state:%s&key=[Your Census key]"
#Population Counts
people_api = "https://api.census.gov/data/2017/acs/acs5?get=NAME,group(B01001)&for=tract:*&in=state:%s&key=[Your Census key]"
#Rents & incomes
rent_and_income_api= "https://api.census.gov/data/2017/acs/acs5?get=NAME,group(B25070)&for=tract:*&in=state:%s&key=[Your Census key]"
#Households that Speak English Well
speak_english_well = "https://api.census.gov/data/2017/acs/acs5?get=NAME,group(C16001)&for=tract:*&in=state:%s&key=[Your Census key]"
#Housing Tenure
homeowners = "https://api.census.gov/data/2017/acs/acs5?get=NAME,group(B25003)&for=tract:*&in=state:%s&key=[Your Census key]"
# No. of vehicles per HH
vehicles = "https://api.census.gov/data/2017/acs/acs5?get=NAME,group(B25044)&for=tract:*&in=state:%s&key=[Your Census key]"
#Commute time to work 
avg_time = "https://api.census.gov/data/2017/acs/acs5?get=NAME,group(S0802)&for=tract:*&in=state:%s&key=[Your Census key]"

total_population = "B01003_001E"
black_population = "B02001_003E"
white_population = "B02001_002E"
hispanic_population ="B03001_003E"
without_college = ""
with_bachelors_college = "B06009_005E"
poverty_percentage = "B06012_002E"  # Below 100 percent of the poverty level
unemployed = "B18120_012E"  # Estimate!!Total!!In the labor force!!Unemployed
unemployed_non_white = ""
avg_commute_time = "B08013_001E"  # Estimate!!Aggregate travel time to work (in minutes)
avg_number_of_vehicles = "B08015_001E"  # Estimate!!Aggregate number of vehicles (car, truck, or van) used in commuting
number_under_18_male = "B05003_003E"
number_under_18_female = "B05003_014E"
number_under_18 = "B09001_001E"
number_over_65 = "B08101_008E"
total_households = "B11006_001E"
time_per_tract = "S0801_C01_046E"
vehicles_avg = "B25044"

#We exclude codes 3,7,11,14,43 and 52. These are FIPS codes for places we do not care about so we exclude from data. 
res_df = pd.DataFrame()
for code in range(1,57):
    if code == 3 or code == 7 or code == 11 or code == 14 or code == 43 or code == 52:
        continue
    state = str(code).zfill(2)
    print("state is {}".format(state))
    calledAPI = avg_time%(state)
    response = requests.get(calledAPI)
    if response == None:
        print("No response~")
        continue
    formattedResponse = json.loads(response.text)
    headers = formattedResponse.pop(0)
    df = pd.DataFrame(formattedResponse, columns=headers)
    tracts = []
    for index,df_row in df.iterrows():
        county = str(df_row['county'])
        tract = str(df_row['tract'])
        county = county.zfill(3)
        res_tract = state + county + tract
    #    print("res_tract is {}".format(res_tract))
        tracts.append(res_tract)

    df['Tract'] = tracts
    df.to_csv("M:\\Research\\Price CSI\\Research\\Projects\\CensusAPI\\source\\State\\"+state+".csv")

#res_df.to_csv("Education_data.csv")

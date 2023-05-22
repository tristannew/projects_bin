
#import packages
import pandas as pd
from urllib.request import urlretrieve
import numpy as np
import seaborn as sns
import statsmodels.formula.api as smf
import re

# retrieve data from web so that analysis can be replicated anywhere
urlretrieve("https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/global-shark-attack/exports/csv?lang=en&timezone=Europe%2FLondon&use_labels=true&delimiter=%3B", "global-shark-attack.csv")

# create DataFrame for easy manipulation
df = pd.read_csv("global-shark-attack.csv", sep = ";")

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)

# these columns were not necessary for the analysis
df = df.drop(columns=["Investigator or Source", "pdf", "href formula", "href"])

df = df.rename(columns={"Sex ":"Sex"}) # removing space for ease

#this analysis was only interested in Unprovoked attacks in recent years (attacks pre 1950 often were strange in nature)
df = df[df['Type'] == 'Unprovoked']
df = df[df['Year'] > 1950]

df['Year'] = df['Year'].astype('int')
df['Activity'] = df['Activity'].astype('str')
df['Time'] = df['Time'].astype('str')


# %% [markdown]
# ### Area Cleaning

# %%
# Replacing incorrect values so that we could groupby region and country
df['Country'] = df['Country'].str.title()

df['Country'] = df['Country']\
    .replace("England", "United Kingdom")\
    .replace("Egypt / Israel", "Egypt")\
    .replace("Okinawa", "Japan")\
    .replace("Persian Gulf", "Iran")\
    .replace("Red Sea", "Jordan")\
    .replace("Reunion", "Reunion Island")\
    .replace("United Arab Emirates (Uae)", "United Arab Emirates")

df['Area'] = df['Area'].replace(["Baja California Sur", "Baja", "Baja California"], "California")\
    .replace("New South ales", "New South Wales")\
    .replace(["New Ireland, Bismarck Archipelago", "New Britain, Bismarck Archipelago",\
        "New Ireland Province, Bismarck Archipelago"], "Bismarck Archipelago")\
    .replace("KwaZulu-Natal between Port Edward and Port St Johns", "KwaZulu-Natal")\
    .replace(["South Devon", "Devon", "Cornwall"], "South West")\
    .replace(["Franklin County, Florida", "Florida Straits"], "Florida")\
    .replace(["Eastern Cape  Province", "Eastern Province"], "Eastern Cape Province")\
    .replace("Hurghada, Red Sea Governorate", "Red Sea")\
    .replace("Sharjah,", "Sharjah")

# %% [markdown]
# ### Datetime cleaning

# %%
# # displaying all rows for visibility
# pd.set_option('display.max_rows', 10000)
# lst = []
# for string in df["Time"].drop_duplicates():
#     if re.search("!?\d{2}h\d{2}", string) == None:
#         lst.append(string)

# %%
# lst =  ['After noon',
#  'Noon',
#  'Just before dawn',
#  '10j30',
#  'A.M.',
#  'Just before noon',
#  'P.M.',
#  'Midnight',
#  'Dawn',
#  '',
#  '2 hours after Opperman',
#  '1600',
#  'Daybreak',
#  '10jh45',
#  'Mid-morning',
#  '11hoo',
#  '9h00',
#  'Early  morning',
#  'X',
#  '1300.0',
#  'AM',
#  'After Dusk',
#  'Mid afternoon',
#  'Just before sundown',
#  'Midday.',
#  'After dark',
#  'night',
#  '0500',
#  'Late morning',
#  '30 minutes after 1992.07.08.a',
#  '06j00']

# for item in lst:
#     print(f".replace('{item}', '____')\\")

# %%
df["Time"] = df["Time"].replace("Afternoon", "15h00")\
    .replace("Morning", "09h00")\
    .replace("Lunchtime", "13h00")\
    .replace("0830", "08h30")\
    .replace(["Early Morning", "Early morning"], "08h00")\
    .replace("Midday", "12h00")\
    .replace(["Dusk", "19h00, Dusk"], "19h00")\
    .replace("14h00 - 15h00", "14h30")\
    .replace(["Late Afternoon", "Late afternoon", "16h30 or 18h00"], "16h30")\
    .replace("Evening", "18h30")\
    .replace("11h115", "11h15")\
    .replace(["Early Afternoon", "Early afternoon"], "14h00")\
    .replace("Night", "19h00")\
    .replace("15h00 or 15h45", "15h30")\
    .replace("08h00 / 09h30", "08h45")\
    .replace("Before 10h00", "09h30")\
    .replace(["14h00  -15h00", "14h00-15h00"], "14h30")\
    .replace("--", "")\
    .replace(["Mid morning", "09h00-10h00"], "09h30")\
    .replace("10h00 -- 11h00", "10h30")\
    .replace("8:04 pm", "20h00")\
    .replace('Sunset', "19h00")\
    .replace('After noon', '15h00')\
    .replace('Noon', '12h00')\
    .replace('Just before dawn', '05h30')\
    .replace('10j30', '10h30')\
    .replace('A.M.', '10h30')\
    .replace('Just before noon', '11h30')\
    .replace('P.M.', '17h00')\
    .replace('Midnight', '00h00')\
    .replace('Dawn', '6h30')\
    .replace('', "")\
    .replace('2 hours after Opperman', '')\
    .replace('1600', '16h00')\
    .replace('Daybreak', '06h30')\
    .replace('10jh45', '10h45')\
    .replace('Mid-morning', '10h30')\
    .replace('11hoo', '11h00')\
    .replace('9h00', '09h00')\
    .replace('Early  morning', '07h00')\
    .replace('X', '')\
    .replace('1300.0', '13h00')\
    .replace('AM', '08h00')\
    .replace('After Dusk', '19h00')\
    .replace('Mid afternoon', '15h00')\
    .replace('Just before sundown', '17h30')\
    .replace('Midday.', '12h00')\
    .replace('After dark', '20h00')\
    .replace('night', '21h00')\
    .replace('0500', '05h00')\
    .replace('Late morning', '11h30')\
    .replace('30 minutes after 1992.07.08.a', '')\
    .replace('06j00', '06h00')

df['Date'] = df['Date'].replace("1018-06-01", "2018-06-01")\
    .replace("202-07-10", "2020-07-10")


# %%
df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")

# %% [markdown]
# ### Activity Cleaning

# %%
def cleaning_activity(activity):
    # if pd.isnull(activity):
    #     return "Unknown"
    # else:
    activity = str(activity).lower()
    if re.search("(body|boogie).*?(boarding|surfing)", activity):
        return "Body Boarding"
    elif re.search("kite.*?(boarding|surfing)", activity):
        return "Kite Surfing"
    elif re.search("wind.*?surfing", activity):
        return "Wind Surfing"
    elif re.search("(paddle|surf).*?ski", activity):
        return "Surf Skiing"
    elif re.search("paddle.*?boarding|sup", activity):
        return "SUP"
    elif re.search("wade|wading", activity):
        return "Wading"
    elif re.search("swim", activity):
        return "Swimming"
    elif re.search("kayak", activity):
        return "Kayaking"
    elif re.search("spear", activity):
        return "Spearfishing"
    elif re.search("snorkel", activity):
        return "Snorkeling"
    elif re.search("diving", activity):
        return "Diving"
    elif re.search("fishing", activity):
        return "Fishing"
    elif re.search("foil", activity):
        return "Foiling"
    elif re.search("float", activity):
        return "Wading"
    elif re.search("\bsurf|surf[a-z]*", activity):
        return "Surfing"
    else:
        return str(activity)

# %%
df["Activity"] = df['Activity'].apply(cleaning_activity)

# %%
def drop_low_counts(df, column):
    for value in df[column]:
        if df[df[column] == value][column].count() < 5:
            df = df.drop(df[df[column] == value].index, axis=0)
    return df

# %%
df = drop_low_counts(df, 'Activity')

# %%



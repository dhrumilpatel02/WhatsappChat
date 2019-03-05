# Cleaning WhatsApp log
import os
import re
import pandas as pd
import numpy as np

watsup_file = 'WAChat.txt'

# Read WhatsApp file
if os.path.exists(watsup_file):
    file_data = open(watsup_file, 'r', encoding="utf8")
    watsup_content = file_data.read()

# Get date
date_regex = re.compile(r'(\d+/\d+/\d+)')
date = date_regex.findall(watsup_content)

# Get time
time_regex = re.compile(r'(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])')
time = time_regex.findall(watsup_content)

# Get Users
user_regex = re.compile(r'-(.*?):')
user = user_regex.findall(watsup_content)

# Get Message
message_regex = re.compile(r"(\n)(?<=)(\d+/\d+/\d+)(.*)")
message = message_regex.findall(watsup_content)

data = []
for w, x, y, z in zip(date, time, user, message):
    data.append([str(w), str(x), str(y), str(z)])

# Create DataFrame from WhatsApp content
df = pd.DataFrame(data, columns=("Date", "Time", "User", "Message"))

# Let's clean our Message
df['Message'] = df['Message'].str.replace('\'(.*?): ', '')

# Get Year from Date
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

# Get Month from Date
df['Month'] = df['Date'].dt.month

# Get Day from Date
df['Day'] = df['Date'].dt.day

# Get Hours of the Day
df['Time'] = pd.to_datetime(df['Time'])
df['Hours'] = df.Time.apply(lambda x: x.hour)

# Message words
df['Words'] = df['Message'].str.strip().str.split('[\W_]+')

# Word length
df['Word Length'] = df['Words'].apply(len) - 2

# Get the Length of Message
df['Message Characters'] = df['Message'].map(str).apply(len) - 3

# Get Media shared in the Message
df['Media'] = df['Message'].str.contains('<Media omitted>')

#Describe the DataFrame
print(df.describe())

# Save the DataFrame to a csv file
df.to_csv("sam.csv")
import pandas as pd
import csv

url=r"C:\Users\kaeli\Downloads\40knews_clean_covid.csv"
try:
    df = pd.read_csv(url, encoding='utf-8',on_bad_lines='warn',low_memory=False)
    df=df.drop_duplicates()
except pd.errors.ParserError as e:
    print("Error parsing CSV file:", e)
df=df.iloc[270:310]
df.to_csv(r"C:\Users\kaeli\Downloads\40knews_clean_covidVALID.csv", index=False)
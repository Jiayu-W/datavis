import pandas as pd
import requests

all_data = None
data_by_team = {}
summaries_by_team = {}


api_key = '8wIJiuRVA565E415VcjYQVuKJNIL76XyMMFOEGsaLC4RDI4uBGUBA4hi3lanWYEr' #
headers = {'X-TBA-Auth-Key': api_key} #


def update_data():
    global all_data
    global data_by_team

    all_data = pd.read_excel('WorldScouting2025Data.xlsx').drop_duplicates() #load the data
    
    #split data by team
    first_col = all_data.columns[0]
    data_by_team.clear()
    for _, row in all_data.iterrows():
        team_number = int(pd.Series(row[first_col]).str.extract(r'_(\d+)_')[0])
        if team_number not in data_by_team:
            data_by_team[team_number] = pd.DataFrame(columns=all_data.columns)
        data_by_team[team_number] = pd.concat([data_by_team[team_number], pd.DataFrame([row])], ignore_index=True)
    
    #generate team summaries

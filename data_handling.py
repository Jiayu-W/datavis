import pandas as pd
import requests
import streamlit as st

if 'data_by_team' not in globals():
    data_by_team = {}
if 'used_data_by_team' not in globals():
    used_data_by_team = {}
if 'all_data' not in globals():
    all_data = pd.DataFrame()

tba_api_key = tba_api_key = st.secrets["TBA_API_KEY"]
headers = {'X-TBA-Auth-Key': tba_api_key}


def update_data():
    global all_data
    global data_by_team

    # import new data
    data_import = pd.read_excel('WorldScouting2025Data.xlsx').drop_duplicates().dropna(how='all')
    data_import['Use Data'] = True
    data_import['Team Number'] = data_import[data_import.columns[0]].str.extract(r'_(\d+)_')[0].astype(int)

    # add new data
    all_data = pd.concat([all_data, data_import], ignore_index=True)
    all_data = all_data.drop_duplicates(subset=all_data.columns.difference(['use_data']), keep='first', ignore_index=True)

    # split data by team
    for team_number in all_data['Team Number'].unique():
        if team_number not in data_by_team:
            data_by_team[team_number] = all_data[all_data['Team Number'] == team_number].copy()
        else:
            data_by_team[team_number] = pd.concat([data_by_team[team_number], all_data[all_data['Team Number'] == team_number].copy()], ignore_index=True)
            data_by_team[team_number] = data_by_team[team_number].drop_duplicates(subset=all_data.columns.difference(['use_data']), keep='first', ignore_index=True)
        data_by_team[team_number].reset_index(drop=True, inplace=True)
        data_by_team[team_number].index+=1

def update_data_visibility(team, df):
    global data_by_team
    global used_data_by_team
    used_data_by_team[team] = df.drop(df[df['Use Data'] == False].index)
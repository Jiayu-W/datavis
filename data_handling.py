import pandas as pd
import requests
import streamlit as st

all_data = pd.DataFrame()
data_by_team = None
summaries_by_team = None

tba_api_key = tba_api_key = st.secrets["TBA_API_KEY"]
headers = {'X-TBA-Auth-Key': tba_api_key}


def update_data():
    global all_data
    global data_by_team

    # Load new data
    data_import = pd.read_excel('WorldScouting2025Data.xlsx').drop_duplicates().dropna(how='all')
    data_import['use_data'] = True  # Mark new rows as "used"
    data_import['team_number'] = data_import[data_import.columns[0]].str.extract(r'_(\d+)_')[0].astype(int)

    # add new data
    all_data = pd.concat([all_data, data_import], ignore_index=True)
    all_data = all_data.drop_duplicates(subset=all_data.columns.difference(['use_data']), keep='first', ignore_index=True)

    # split data by team
    data_by_team = {}
    for team_number in all_data['team_number'].unique():
        data_by_team[team_number] = all_data[all_data['team_number'] == team_number].copy()


def generate_summary(team):
    global data_by_team
    global summaries_by_team
    if summaries_by_team is None:
        summaries_by_team = {}
    df = data_by_team.get(team)
    if df is not None:
        means_by_team = df.mean(numeric_only=True)
        maxes_by_team = df.max(numeric_only=True)
        summaries_by_team[team] = {'mean': means_by_team.to_dict(), 'max': maxes_by_team.to_dict()}
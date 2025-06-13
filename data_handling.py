import pandas as pd
import requests
import streamlit as st

all_data = None
data_by_team = None
summaries_by_team = None

tba_api_key = tba_api_key = st.secrets["TBA_API_KEY"]
headers = {'X-TBA-Auth-Key': tba_api_key}


def update_data():
    global all_data
    global data_by_team

    all_data = pd.read_excel('WorldScouting2025Data.xlsx').drop_duplicates().dropna(how='all')  # load the data

    # add a column for team numbers
    all_data['team_number'] = all_data[all_data.columns[0]].str.extract(r'_(\d+)_')[0].astype(int)

    # split data by team
    data_by_team = pd.Series()
    for team_number in all_data['team_number'].unique():
        data_by_team[team_number] = all_data[all_data['team_number'] == team_number].copy()


def generate_summary(team):
    global data_by_team
    global summaries_by_team
    summaries_by_team = {}
    for team_number, df in data_by_team.items():
        means_by_team = df.mean(numeric_only=True)
        maxes_by_team = df.max(numeric_only=True)
        summaries_by_team[team_number] = pd.Series({'mean': means_by_team, 'max': maxes_by_team})
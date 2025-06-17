import data_handling as data

data_by_team = data.used_data_by_team
if 'summaries_by_team' not in globals():
    summaries_by_team = {}

def generate_summary(team):
    df = data_by_team.get(team)
    if df is not None:
        means_by_team = df.mean(numeric_only=True)
        maxes_by_team = df.max(numeric_only=True)
        summaries_by_team[team] = {'mean': means_by_team.to_dict(), 'max': maxes_by_team.to_dict()}
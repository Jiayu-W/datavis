import streamlit as st
import data_handling as data

data.update_data()

st.title("Data Visualizer")

# all data
st.header("All Data")
st.dataframe(data.all_data)

# team selector
team_numbers = list(data.data_by_team.keys())
selected_team = st.selectbox("Select a team", team_numbers)

# selected team data
st.header(f"Data for Team {selected_team}")
st.dataframe(data.data_by_team[selected_team])

# summary for selected team
st.header(f"Summary for Team {selected_team}")
st.write(data.summaries_by_team[selected_team])
import streamlit as st
import data_handling as data
import pandas as pd

data.update_data()

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="top-bar">
        <h1>Data Visualizer</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# initialize session states
if "show_charts" not in st.session_state:
    st.session_state["team_data"] = True

# 4 buttons
cols = st.columns(3)
button_labels = ["Team Data", "Compare Teams", "Settings"]

for i, col in enumerate(cols):
    with col:
        if st.button(button_labels[i], key=f"btn{i+1}"):
            st.session_state["team_data"] = (i == 0)

# team datavis
if st.session_state["team_data"]:
    st.header("Team Data")

    team_numbers = sorted(data.data_by_team.keys())
    selected_team = st.selectbox("Select a team", team_numbers)

    data.generate_summary(selected_team)

    #st.header(f"Summary for Team {selected_team}")
    #st.write(data.summaries_by_team[selected_team])

    st.header(f"Data for Team {selected_team}")
    team_df = data.data_by_team[selected_team]
    
    team_df = st.data_editor(
        team_df,
        column_order=['Use Data'] + [col for col in team_df.columns if col != 'Use Data' and col != 'team_number'],
        column_config={
            'Use Data': st.column_config.CheckboxColumn(
                "Use Data",
            )
        }
    )
    print(team_df['Use Data'])
    data.data_by_team[selected_team]=team_df
    data.update_data_visibility(selected_team, team_df)
    print(data.used_data_by_team[selected_team]['Use Data'])

else:
    print(data.data_by_team[58]['Use Data'])
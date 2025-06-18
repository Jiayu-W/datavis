import streamlit as st
import data_handling as handling
import data_analysis as analysis
import pandas as pd

if "loaded" not in st.session_state:
    handling.update_data()
    st.session_state["loaded"] = True

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
if "team_data" not in st.session_state:
    st.session_state["team_data"] = False
if "compare_teams" not in st.session_state:
    st.session_state["compare_teams"] = False
if "settings" not in st.session_state:
    st.session_state["settings"] = False


# 4 buttons
cols = st.columns(3)
button_labels = ["Team Data", "Compare Teams", "Settings"]

for i, col in enumerate(cols):
    with col:
        if st.button(button_labels[i], key=f"btn{i+1}"):
            st.session_state["team_data"] = (i == 0)
            st.session_state["compare_teams"] = (i == 1)
            st.session_state["settings"] = (i == 2)

# team datavis
if st.session_state["team_data"]:
    st.header("Team Data")

    team_numbers = sorted(handling.data_by_team.keys())
    selected_team = st.selectbox("Select a team", team_numbers)

    analysis.generate_summary(selected_team)

    st.header(f"Summary for Team {selected_team}")
    st.table()

    st.header(f"Data for Team {selected_team}")
    team_df = handling.data_by_team[selected_team]
    
    team_df = st.data_editor(
        team_df,
        column_order=['Use Data'] + [col for col in team_df.columns if col != 'Use Data' and col != 'team_number'],
        column_config={
            'Use Data': st.column_config.CheckboxColumn(
                "Use Data",
            )
        }
    )
    handling.data_by_team[selected_team]=team_df
    handling.update_data_visibility(selected_team, team_df)
    print(handling.data_by_team[selected_team])
    print(team_df)

elif st.session_state['settings']:
    print("Hello Wolrd!")
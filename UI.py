import streamlit as st
import data_handling as data
from st_aggrid import AgGrid, GridOptionsBuilder
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
cols = st.columns(4)
button_labels = ["Team Data", "Match Strategy", "Picklist", "Rankings"]

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
    team_df = data.data_by_team[selected_team].drop(columns="team_number", errors="ignore").reset_index(drop=True)

    st.header(f"Summary for Team {selected_team}")
    st.write(data.summaries_by_team[selected_team])

    st.header(f"Data for Team {selected_team}")

    st.subheader("Match Data Table (with Checkboxes)")

    selected_rows = team_df[team_df.get('use_data', pd.Series([False] * len(team_df))).fillna(False) == True].to_dict('records')
    display_df = team_df.drop(columns=['use_data'], errors='ignore').reset_index(drop=True)

    # make scroll table
    gb = GridOptionsBuilder.from_dataframe(display_df)
    gb.configure_selection('multiple', use_checkbox=True)
    gb.configure_grid_options(domLayout='normal')
    grid_options = gb.build()

    grid_response = AgGrid(
        display_df,
        gridOptions=grid_options,
        update_mode='SELECTION_CHANGED',
        allow_unsafe_jscode=True,
        theme='streamlit',
        height=400,
        selected_rows=selected_rows
    )
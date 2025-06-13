import streamlit as st
import data_handling as data

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

# initialize session state
if "show_charts" not in st.session_state:
    st.session_state["team_data"] = True


# 4 symmetrical buttons in a row
cols = st.columns(4)
button_labels = ["Team Data", "Match Strategy", "Picklist", "Rankings"]

for i, col in enumerate(cols):
    with col:
        if st.button(button_labels[i], key=f"btn{i+1}"):
            st.session_state["team_data"] = (i == 0)

# show/hide data
if st.session_state["team_data"]:
    st.header("Team Data")

    team_numbers = list(data.data_by_team.keys().sort_values())
    selected_team = st.selectbox("Select a team", team_numbers)

    data.generate_summary(selected_team)
    team_df = data.data_by_team[selected_team].drop(columns="team_number", errors="ignore").reset_index(drop=True)

    st.header(f"Summary for Team {selected_team}")
    st.write(data.summaries_by_team[selected_team])

    st.header(f"Data for Team {selected_team}")

    for index, row in team_df.iterrows():
        checkbox_label = f"Match {row['Scouting ID'].rsplit('_', 1)[-1]}"  # Customize label based on a column
        if st.checkbox(checkbox_label, key=f"checkbox_{index}"):
            team_df.at[index, 'team_number'] = 0
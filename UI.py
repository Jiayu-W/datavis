import streamlit as st
import data_handling as data

data.update_data()

# Remove Streamlit's default top padding and style
st.markdown(
    """
    <style>
        .block-container { padding-top: 5rem !important; }
        .top-bar { background-color:#003366; padding:5px 0 5px 0; margin-bottom:0px; }
        .top-bar h1 { color:white; text-align:center; margin:0; }
        .stButton>button {
            width: 100%;
            background-color: #0055aa;
            color: white;
            border-radius: 0;
            border: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Top bar
st.markdown(
    """
    <div class="top-bar">
        <h1>Data Visualizer</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "show_charts" not in st.session_state:
    st.session_state["team_data"] = False


# 4 symmetrical buttons in a row
cols = st.columns(4)
button_labels = ["Team Data", "Place Holder", "Place Holder", "Place Holder"]

for i, col in enumerate(cols):
    with col:
        if st.button(button_labels[i], key=f"btn{i+1}"):
            st.session_state["team_data"] = (i == 0)

# Show/hide charts and data
if st.session_state["team_data"]:
    st.header("Team Data")

    team_numbers = list(data.data_by_team.keys())
    selected_team = st.selectbox("Select a team", team_numbers)

    st.header(f"Summary for Team {selected_team}")
    st.write(data.summaries_by_team[selected_team])

    st.header(f"Data for Team {selected_team}")
    st.dataframe(data.data_by_team[selected_team])
import streamlit as st
import pandas as pd

# Load datasets for all 5 leagues
df_epl = pd.read_csv(
    "D:\\Player Shot Map and Analysis\\data\\EPL_final.csv")
df_bundesliga = pd.read_csv(
    "D:\\Player Shot Map and Analysis\\data\\Bundesliga_final.csv")
df_ligue1 = pd.read_csv(
    "D:\\Player Shot Map and Analysis\\data\\Ligue1_final.csv")
df_seriea = pd.read_csv(
    "D:\\Player Shot Map and Analysis\\data\\SerieA_final.csv")
df_laliga = pd.read_csv(
    "D:\\Player Shot Map and Analysis\\data\\LaLiga_final.csv")
# Combine datasets into a dictionary for easy selection
leagues = {
    "Premier League": df_epl,
    "Bundesliga": df_bundesliga,
    "Ligue 1": df_ligue1,
    "Serie A": df_seriea,
    "La Liga": df_laliga
}

# Title for the separate page
st.markdown(
    """
    <h1 style="font-family: 'Helvetica Neue', Arial, sans-serif; 
               color: #000000; 
               text-align: center;
               font-size: 36px;">
    Overperformers and Underperformers Ranking
    </h1>
    """,
    unsafe_allow_html=True
)

# Sidebar for filters
with st.sidebar:
    selected_league = st.selectbox('Select a League:', list(leagues.keys()))
    df_league = leagues[selected_league]


# Defines the ranking function for overperformers and underperformers
def rank_over_underperformers(df):
    # Add a column for actual goals (1 if goal, 0 otherwise)
    df['actual_goals'] = df['result'].apply(lambda x: 1 if x == 'Goal' else 0)

    # Group by player to calculate total xG and actual goals
    player_stats = df.groupby('player').agg(
        total_xG=('xG', 'sum'),
        total_goals=('actual_goals', 'sum'),
        team=('Player_Team', 'first')
    ).reset_index()

    # Calculate overperformance or underperformance
    player_stats['xG_diff'] = player_stats['total_goals'] - player_stats['total_xG']

    # Rename columns for display
    player_stats = player_stats.rename(columns={
        'player': 'Player',
        'team': 'Team',
        'total_xG': 'Total xG',
        'total_goals': 'Total Goals',
        'xG_diff': 'xG Diff'
    })

    # Get top 10 overperformers (players with most goals above xG)
    overperformers = player_stats.sort_values(by='xG Diff', ascending=False).head(10)
    overperformers = overperformers.reset_index(drop=True)  # Reset index
    overperformers.index += 1  # Start numbering from 1

    # Get top 10 underperformers (players with fewest goals relative to xG)
    underperformers = player_stats.sort_values(by='xG Diff', ascending=True).head(10)
    underperformers = underperformers.reset_index(drop=True)  # Reset index
    underperformers.index += 1  # Start numbering from 1

    # Display the top 10 overperformers
    st.write("### Top 10 Overperformers")
    st.dataframe(overperformers[['Player', 'Team', 'Total xG', 'Total Goals', 'xG Diff']])

    # Display the top 10 underperformers
    st.write("### Top 10 Underperformers")
    st.dataframe(underperformers[['Player', 'Team', 'Total xG', 'Total Goals', 'xG Diff']])


# Button to display the ranking
if st.sidebar.button("Show Over/Underperformers Ranking"):
    rank_over_underperformers(df_league)

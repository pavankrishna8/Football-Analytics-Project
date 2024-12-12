import streamlit as st

def main():
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column widths as needed

    with col1:
        st.image("D:\\Player Shot Map and Analysis\\woxsen logo.png", width=150)  # Adjust width as necessary

    with col3:
        st.image("D:\Player Shot Map and Analysis\COE logo.jpeg", width=100)  # Adjust width as necessary

    st.markdown("<h1 style='font-size: 34px;'>European Football Shot Analysis: A Deep Dive</h1>",
                unsafe_allow_html=True)

    st.write("""
    **Project Overview**

    Welcome to your ultimate tool for football performance analysis in the 2023-24 season! 
    This project offers in-depth insights into player performances across Europe’s top 5 leagues, 
    combining advanced data with powerful visualizations to help you explore the game like never before.
    """)

    st.write("""
    **Core Features:**

    - **Interactive Shot Maps:** Filter by league, team, player, and match situations to explore detailed shot maps. 
      Visualize where players take their shots, and uncover key stats such as total shots, goals, xG, xG per shot, and conversion rates. 
      Plus, break down goals by location (home vs. away) and body part (left foot, right foot, head, etc.).

    - **Shot vs. Minute Analysis:** Understand a player’s impact over time with a graph showing their shot activity throughout the season. 
      Each bar represents the number of shots in specific time intervals, with goals highlighted by a soccer ball icon. 
      This analysis reveals patterns in a player’s performance during different phases of a match.

    - **Top Overperformers and Underperformers:** Quickly identify the top 10 players who are either surpassing expectations or underperforming based on xG and goals scored. 
      This feature helps pinpoint which players are making the most of their chances and who might need improvement.
    """)

    st.write("""
    **Why This Project Matters for Football Analytics:**

    This tool goes beyond traditional statistics, offering a comprehensive view of player performance through data-driven insights. 
    Whether you're analyzing tactics, scouting talent, or simply exploring the game from a new perspective, this project provides the depth and flexibility needed to enhance your football analysis. 
    With these insights, you can make more informed decisions, spot trends, and better understand the nuances of player performance across different scenarios.
    """)

    st.write("""
        **Disclaimer:**

        This project is intended for educational purposes only. The data used in this analysis has been scraped from [Understat](https://understat.com/) and is provided without warranty. 
        The creators of this project do not claim ownership of the data and are not responsible for any inaccuracies or omissions. """)


if __name__ == "__main__":
    main()

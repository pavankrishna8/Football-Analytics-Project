import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import streamlit as st
from mplsoccer import VerticalPitch
import matplotlib.font_manager as font_manager
from PIL import Image

# Load the soccer ball image
soccer_img_path = "D:\\Player Shot Map and Analysis\\soccer.png"
soccer_img = plt.imread(soccer_img_path)

# Load all league datasets
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

# Combine datasets into a dictionary
leagues = {
    "Premier League": df_epl,
    "Bundesliga": df_bundesliga,
    "Ligue 1": df_ligue1,
    "Serie A": df_seriea,
    "La Liga": df_laliga
}

# Scale coordinates in all datasets
for league_name, df in leagues.items():
    df['X'] = df['X'] * 100
    df['Y'] = df['Y'] * 100
    leagues[league_name] = df

# Streamlit app
st.markdown(
    """
    <h1 style="font-family: 'Helvetica Neue', Arial, sans-serif; 
               color: #000000; 
               text-align: center;
               font-size: 36px;">
    Precision Strikes: Player Shot Maps Across Top Football Leagues
    </h1>
    """,
    unsafe_allow_html=True
)



#st.sidebar.image(woxsen_logo, use_column_width=True)
# Sidebar for filters
with st.sidebar:
    # Display Woxsen logo at the top of the sidebar
    selected_league = st.selectbox('Select a League:', list(leagues.keys()))
    df_league = leagues[selected_league]

    # Sort the teams in alphabetical order
    sorted_teams = sorted(df_league['Player_Team'].unique())
    selected_team = st.selectbox('Select a Team:', sorted_teams)

    df_team = df_league[df_league['Player_Team'] == selected_team]
    selected_player = st.selectbox('Select a Player:', df_team['player'].unique())
    selected_situation = st.selectbox('Select a Situation:', df_team['situation'].unique())

# Filter the data based on selected player and situation
df_player = df_team[(df_team['player'] == selected_player) & (df_team['situation'] == selected_situation)]

# Shot Map Visualization
def shot_map():
    total_shots = df_player.shape[0]
    total_goals = df_player[df_player['result'] == 'Goal'].shape[0]
    total_xG = df_player['xG'].sum()
    xG_per_shot = total_xG / total_shots if total_shots > 0 else 0
    points_average_distance = df_player['X'].mean()
    actual_average_distance = 120 - (df_player['X'] * 1.2).mean()
    conversion_rate = (total_goals / total_shots) * 100 if total_shots > 0 else 0
    home_goals = df_player[(df_player['result'] == 'Goal') & (df_player['h_a'] == 'h')].shape[0]
    away_goals = df_player[(df_player['result'] == 'Goal') & (df_player['h_a'] == 'a')].shape[0]
    background_color = '#0C0D0E'

    goals_by_left_foot = df_player[(df_player['result'] == 'Goal') & (df_player['shotType'] == 'LeftFoot')].shape[0]
    goals_by_right_foot = df_player[(df_player['result'] == 'Goal') & (df_player['shotType'] == 'RightFoot')].shape[0]
    goals_by_head = df_player[(df_player['result'] == 'Goal') & (df_player['shotType'] == 'Head')].shape[0]
    goals_by_other = df_player[(df_player['result'] == 'Goal') & (df_player['shotType'] == 'OtherBodyPart')].shape[0]

    font_path = "D:\\Player Shot Map and Analysis\\fonts\\Arvo-Regular.ttf"
    font_props = font_manager.FontProperties(fname=font_path)

    pitch = VerticalPitch(
        pitch_type='opta',
        half=True,
        pitch_color=background_color,
        pad_bottom=.5,
        line_color='white',
        linewidth=.75,
        axis=True, label=True
    )

    fig = plt.figure(figsize=(8, 12))
    fig.patch.set_facecolor(background_color)

    ax1 = fig.add_axes([0, 0.7, 1, .2])
    ax1.set_facecolor(background_color)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)

    ax1.text(
        x=0.5,
        y=.85,
        s=selected_player,
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='center'
    )
    ax1.text(
        x=0.5,
        y=.7,
        s=f'All shots in the {selected_league} 2023-24',
        fontsize=14,
        fontweight='bold',
        fontproperties=font_props,
        color='white',
        ha='center'
    )
    ax1.text(
        x=0.25,
        y=0.5,
        s=f'Low Quality Chance',
        fontsize=12,
        fontproperties=font_props,
        color='white',
        ha='center'
    )

    for i, size in enumerate([100, 200, 300, 400, 500], start=1):
        ax1.scatter(
            x=0.36 + 0.05 * i,
            y=0.53,
            s=size,
            color=background_color,
            edgecolor='white',
            linewidth=.8
        )

    ax1.text(
        x=0.8,
        y=0.5,
        s=f'High Quality Chance',
        fontsize=12,
        fontproperties=font_props,
        color='white',
        ha='center'
    )

    ax1.text(
        x=0.45,
        y=0.27,
        s=f'Goal',
        fontsize=10,
        fontproperties=font_props,
        color='white',
        ha='right'
    )
    ax1.scatter(
        x=0.47,
        y=0.3,
        s=100,
        color='red',
        edgecolor='white',
        linewidth=.8,
        alpha=.7
    )

    ax1.scatter(
        x=0.53,
        y=0.3,
        s=100,
        color=background_color,
        edgecolor='white',
        linewidth=.8
    )

    ax1.text(
        x=0.55,
        y=0.27,
        s=f'No Goal',
        fontsize=10,
        fontproperties=font_props,
        color='white',
        ha='left'
    )

    ax1.set_axis_off()

    ax2 = fig.add_axes([.05, 0.25, .9, .5])
    ax2.set_facecolor(background_color)

    pitch.draw(ax=ax2)

    ax2.scatter(
        x=90,
        y=points_average_distance,
        s=100,
        color='white',
        linewidth=.8
    )
    ax2.plot(
        [90, 90],
        [100, points_average_distance],
        color='white',
        linewidth=2
    )

    ax2.text(
        x=90,
        y=points_average_distance - 4,
        s=f'Average Distance\n{actual_average_distance:.1f} yards',
        fontsize=10,
        fontproperties=font_props,
        color='white',
        ha='center'
    )

    for x in df_player.to_dict(orient='records'):
        pitch.scatter(
            x['X'],
            x['Y'],
            s=300 * x['xG'],
            color='red' if x['result'] == 'Goal' else background_color,
            ax=ax2,
            alpha=.7,
            linewidth=.8,
            edgecolor='white'
        )

    ax2.set_axis_off()

    ax3 = fig.add_axes([0, .2, 1, .05])
    ax3.set_facecolor(background_color)
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)

    ax3.text(
        x=0.1,
        y=.5,
        s='Shots',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='left'
    )

    ax3.text(
        x=0.13,
        y=0,
        s=f'{total_shots}',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='left'
    )

    ax3.text(
        x=0.24,
        y=.5,
        s='Goals',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='left'
    )

    ax3.text(
        x=0.28,
        y=0,
        s=f'{total_goals}',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='left'
    )

    ax3.text(
        x=0.38,
        y=.5,
        s='xG',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='left'
    )

    ax3.text(
        x=0.375,
        y=0,
        s=f'{total_xG:.2f}',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='left'
    )

    ax3.text(
        x=0.48,
        y=.5,
        s='xG/Shot',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='left'
    )

    ax3.text(
        x=0.52,
        y=0,
        s=f'{xG_per_shot:.2f}',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='left'
    )

    ax3.text(
        x=0.64,
        y=.5,
        s='Conversion Rate',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='left'
    )

    ax3.text(
        x=0.73,
        y=0,
        s=f'{conversion_rate:.2f}%',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='left'
    )

    ax3.text(
        x=0.2,
        y=-0.5,
        s='Goals at Home',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='left'
    )

    ax3.text(
        x=0.32,
        y=-1,
        s=f'{home_goals}',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='left'
    )

    ax3.text(
        x=0.61,
        y=-0.5,
        s='Goals Away',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='left'
    )

    ax3.text(
        x=0.705,
        y=-1,
        s=f'{away_goals}',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='left'
    )

    ax3.text(
        x=0.1,
        y=-1.5,
        s='Goals with:',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='left'
    )

    ax3.text(
        x=0.3,
        y=-1.5,
        s='Left Foot',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='left'
    )

    ax3.text(
        x=0.36,
        y=-2,
        s=f'{goals_by_left_foot}',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='left'
    )

    ax3.text(
        x=0.48,
        y=-1.5,
        s='Right Foot',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='left'
    )

    ax3.text(
        x=0.56,
        y=-2,
        s=f'{goals_by_right_foot}',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='left'
    )

    ax3.text(
        x=0.68,
        y=-1.5,
        s='Head',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='left'
    )

    ax3.text(
        x=0.72,
        y=-2,
        s=f'{goals_by_head}',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='left'
    )

    ax3.text(
        x=0.8,
        y=-1.5,
        s='Other',
        fontsize=20,
        fontproperties=font_props,
        fontweight='bold',
        color='white',
        ha='left'
    )

    ax3.text(
        x=0.84,
        y=-2,
        s=f'{goals_by_other}',
        fontsize=16,
        fontproperties=font_props,
        color='red',
        ha='left'
    )

    ax3.set_axis_off()
    st.pyplot(fig)

    player_name_clean = selected_player.replace(" ", "_")  # Replaces spaces with underscores
    img_path = f'{player_name_clean}_shot_map.png'

    # Save the figure as an image file with the dynamic filename
    fig.savefig(img_path, bbox_inches='tight', dpi=300)

    # Provide a download button for the saved image
    with open(img_path, "rb") as img_file:
        btn = st.download_button(
            label="Download Shot Map",
            data=img_file,
            file_name=img_path,
            mime="image/png"
        )


# Shot vs Minute Analysis
def add_dynamic_image_and_text_side_by_side(ax, image, x, y, num_goals, zoom=0.05, gap=0.08):
    """
    Adds the number of goals first and then a soccer ball image side by side at the top of the bar.
    The gap between the number and the ball is adjustable.
    """
    # Calculate the position offset based on the height of the bar
    y_offset = y + (0.02 * y)  # Small offset above the bar height

    # Add number of goals first
    ax.text(x - gap, y_offset, f'{num_goals}', ha='center', fontsize=12, color='black', va='center')

    # Add soccer ball image to the right of the number
    imagebox = OffsetImage(image, zoom=zoom)
    ab = AnnotationBbox(imagebox, (x + gap, y_offset), frameon=False)  # Adjust the gap for alignment
    ax.add_artist(ab)



# Shot vs Minute Analysis
def plot_shot_vs_minute_analysis():
    """
    Plots shot distribution by minute bins and adds number of goals followed by a soccer ball side by side.
    """
    # Define the bins and labels
    bins = [0, 15, 30, 45, 60, 75, 90, 100]
    bin_labels = ['0-15', '15-30', '30-45', '45-60', '60-75', '75-90', '90+']

    # Create 'minute_bin' column
    df_player['minute_bin'] = pd.cut(df_player['minute'], bins=bins, labels=bin_labels, right=False)

    # Group by 'minute_bin' for shot and goal distribution
    shot_distribution = df_player.groupby('minute_bin').size()
    goal_distribution = df_player[df_player['result'] == 'Goal'].groupby('minute_bin').size()

    # Plot the distribution with an attractive turquoise color
    plt.figure(figsize=(10, 6))
    attractive_color = '#FF6347'  # Vibrant turquoise
    ax = sns.barplot(x=shot_distribution.index, y=shot_distribution.values, color=attractive_color)

    # Add number of goals and soccer ball beside the bars
    for i, bin_label in enumerate(shot_distribution.index):
        num_goals = goal_distribution.get(bin_label, 0)
        if num_goals > 0:
            add_dynamic_image_and_text_side_by_side(ax, soccer_img, x=i, y=shot_distribution.values[i], num_goals=num_goals)

    # Add player's name to the plot
    player_name = selected_player
    plt.title(f'Shots and Goals - Distribution Across Game Minutes: {player_name}', fontsize=16, fontweight='bold', color='#2c3e50')
    plt.xlabel('Minutes', fontsize=12, fontweight='bold', color='#2c3e50')
    plt.ylabel('Number of Shots', fontsize=12, fontweight='bold', color='#2c3e50')
    plt.xticks(rotation=0, fontsize=10, color='#2c3e50')
    plt.tight_layout()  # Ensures layout fits within the plot

    st.pyplot(plt.gcf())



# Display buttons to show visualizations
if st.sidebar.button("Show Shot Map"):
    shot_map()

if st.sidebar.button("Shot v/s Minute Analysis"):
    plot_shot_vs_minute_analysis()

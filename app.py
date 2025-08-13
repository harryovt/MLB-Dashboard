import streamlit as st
from mlb_api import get_player_info, get_player_stats, clean_stats
import plotly.express as px

st.set_page_config(page_title="MLB Player Explorer", layout="wide")
st.title("⚾ MLB Player Performance Explorer")

# Suggested enhancements
st.sidebar.markdown("### Suggested Enhancements")
st.sidebar.markdown("""
- Season-over-Season Comparisons
- Player vs. League Average
- Advanced Metrics (WAR and OPS)
""")

# Sidebar inputs
player_name = st.sidebar.text_input("Enter Player Name", "Aaron Judge")
season = st.sidebar.selectbox("Select Season", [str(y) for y in range(2020, 2024)][::-1])

if player_name:
    with st.spinner("Fetching player data..."):
        player = get_player_info(player_name)
        if player:
            stats = get_player_stats(player['id'], season)

            # Display player info
            st.subheader(f"{player['name']} ({player['team']} - {player['position']})")
            st.markdown(f"**Season:** {season}")

            # Display stats table
            if stats:
                df = clean_stats(stats)
                st.dataframe(df, use_container_width=True)

                # Extract numeric stats for charting
                numeric_df = df[df['Value'].apply(lambda x: isinstance(x, (int, float)))]

                if not numeric_df.empty:
                    # Stat selector
                    selected_stats = st.multiselect(
                        "Select stats to visualize",
                        options=numeric_df['Stat'].tolist(),
                        default=numeric_df['Stat'].tolist()[:5]
                    )

                    # Plot selected stats
                    if selected_stats:
                        filtered_df = numeric_df[numeric_df['Stat'].isin(selected_stats)]
                        fig = px.bar(
                            filtered_df,
                            x='Stat',
                            y='Value',
                            title='Selected Player Stats',
                            labels={'Value': 'Stat Value'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Select at least one stat to display the chart.")
                else:
                    st.warning("No numeric stats available to visualize.")
            else:
                st.warning("No stats found for this season.")
        else:
            st.error("Player not found.")
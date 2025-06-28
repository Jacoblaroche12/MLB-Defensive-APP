
import streamlit as st
import pandas as pd

st.set_page_config(page_title="MLB Defensive AI", layout="wide")
st.title("🧠 MLB Defensive AI: Who Should Start?")

@st.cache_data
def load_data():
    return pd.read_csv("fielding_data_2024.csv")

df = load_data()

positions = sorted(df["position"].unique())
selected_pos = st.selectbox("Choose Position", positions)
players_at_pos = df[df["position"] == selected_pos]

player_names = players_at_pos["player_name"].tolist()
compare_players = st.multiselect("Compare Players", player_names, default=player_names[:2])

st.subheader("🔍 Player Comparison")
comp_df = players_at_pos[players_at_pos["player_name"].isin(compare_players)]
st.dataframe(comp_df[['player_name', 'team', 'OAA', 'DRS', 'UZR', 'arm', 'range', 'errors']], use_container_width=True)

st.subheader("✅ AI Recommender")

def recommend_player(df):
    df = df.copy()
    df["score"] = (df["OAA"] * 0.4 + df["DRS"] * 0.3 + df["UZR"] * 0.2 + df["range"] * 0.1) - (df["errors"] * 0.2)
    top_player = df.sort_values(by="score", ascending=False).iloc[0]
    return top_player

if not comp_df.empty:
    best = recommend_player(comp_df)
    st.success(f"🏆 Recommended Starter at {selected_pos}: **{best['player_name']}** (Score: {round(best['score'],2)})")

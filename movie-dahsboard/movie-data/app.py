import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os

# Page config (UI improvement)
st.set_page_config(page_title="Movie Analytics Dashboard", layout="wide")

FILE = "data.csv"

# Create file if not exists
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["Movie", "Rating", "Mood", "Genre"])
    df.to_csv(FILE, index=False)

# Title
st.title("🎬 Movie Analytics & Mood Insight Dashboard")

st.markdown("---")

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
selected_genre = st.sidebar.selectbox(
    "Select Genre",
    ["All", "Action", "Comedy", "Drama", "Horror", "Other"]
)

# Search feature
search_movie = st.sidebar.text_input("Search Movie")

# Input Section
st.subheader("➕ Add Movie Data")

col1, col2 = st.columns(2)

with col1:
    movie = st.text_input("Movie Name")
    rating = st.slider("Rating", 1, 10)

with col2:
    mood = st.selectbox("Mood", ["Happy", "Sad", "Excited", "Bored"])
    genre = st.selectbox("Genre", ["Action", "Comedy", "Drama", "Horror", "Other"])

if st.button("Submit"):
    new_data = pd.DataFrame([[movie, rating, mood, genre]],
                            columns=["Movie", "Rating", "Mood", "Genre"])
    new_data.to_csv(FILE, mode='a', header=False, index=False)
    st.success("✅ Data added successfully!")

st.markdown("---")

# Load Data
df = pd.read_csv(FILE)

if not df.empty:

    # Apply search filter
    if search_movie:
        df = df[df["Movie"].str.contains(search_movie, case=False)]

    # Apply genre filter
    if selected_genre != "All":
        df = df[df["Genre"] == selected_genre]

    st.subheader("📊 Dashboard")

    # Top Movies
    st.write("🏆 Top Rated Movies")
    top_movies = df.sort_values(by="Rating", ascending=False).head(5)
    st.dataframe(top_movies, use_container_width=True)

    st.markdown("---")

    col3, col4 = st.columns(2)

    # Genre Analysis
    with col3:
        st.write("🎭 Average Rating by Genre")
        genre_avg = df.groupby("Genre")["Rating"].mean()
        st.bar_chart(genre_avg)

    # Rating Distribution
    with col4:
        st.write("⭐ Rating Distribution")
        fig, ax = plt.subplots()
        ax.hist(df["Rating"], bins=10)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Count")
        st.pyplot(fig)

    st.markdown("---")

    # Mood vs Rating
    st.write("😊 Mood vs Rating")
    mood_map = {"Happy":1, "Excited":2, "Sad":3, "Bored":4}
    df["Mood_Num"] = df["Mood"].map(mood_map)

    fig2, ax2 = plt.subplots()
    ax2.scatter(df["Rating"], df["Mood_Num"])
    ax2.set_yticks([1,2,3,4])
    ax2.set_yticklabels(["Happy","Excited","Sad","Bored"])
    ax2.set_xlabel("Rating")
    ax2.set_ylabel("Mood")
    st.pyplot(fig2)

    st.markdown("---")

    # 🔥 INSIGHTS SECTION (Resume booster)
    st.subheader("📌 Insights")

    avg_rating = df["Rating"].mean()
    most_common_mood = df["Mood"].mode()[0]
    best_genre = df.groupby("Genre")["Rating"].mean().idxmax()

    st.write(f"✔️ Average Rating is {avg_rating:.2f}, indicating overall user satisfaction.")

    if avg_rating > 7:
        st.write("🔥 Most movies are highly rated by users.")
    else:
        st.write("⚠️ Ratings are generally moderate or low.")

    st.write(f"😊 Most users felt '{most_common_mood}' after watching movies.")
    st.write(f"🎭 '{best_genre}' genre performs best based on average ratings.")

else:
    st.warning("⚠️ No data available. Please add movie entries.")
import streamlit as st
import pickle
import pandas as pd
import requests

# PAGE CONFIG
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

#LOAD DATA
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

API_KEY = "86d216087c0ae643ed3a8709a3295cf2"

# CACHE POSTERS (FAST)
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    except:
        pass

    return "https://via.placeholder.com/300x450?text=No+Image"

#  RECOMMEND FUNCTION 
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    names = []
    posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters

# UI HEADER
st.markdown(
    """
    <h1 style='text-align:center;'>🎬 Movie Recommender System</h1>
    <p style='text-align:center; color:gray;'>
    Find movies similar to your favorite one instantly 🍿
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------------- MOVIE SELECT ----------------
movie_titles = movies['title'].values

selected_movie_name = st.selectbox(
    "🎥 Select a movie you like",
    movie_titles
)

# ---------------- BUTTON ----------------
if st.button("✨ Recommend Movies", use_container_width=True):
    with st.spinner("Finding best matches for you..."):
        names, posters = recommend(selected_movie_name)

    st.markdown(
        f"<h3 style='margin-top:20px;'>Because you liked <span style='color:#ff4b4b'>{selected_movie_name}</span>:</h3>",
        unsafe_allow_html=True
    )

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.markdown(
                f"<p style='text-align:center; font-weight:600;'>{names[idx]}</p>",
                unsafe_allow_html=True
            )

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "<p style='text-align:center; color:gray;'>Built with ❤️ using Streamlit & Machine Learning</p>",
    unsafe_allow_html=True
)

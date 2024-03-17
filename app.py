import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch images for a movie
def fetch_movie_images(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YTg3NGZlYzIxNTRkM2JlYTY3MTRiMTBmMGIzOWY3ZCIsInN1YiI6IjY1ZjY3MTUyNjY0NjlhMDE3ZTdhMjI5MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-Mh_p9Cu2y0-J_sOOdAPcyBA2vb80JzP6J90ohGV6lE",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        posters = [f"https://image.tmdb.org/t/p/original{img['file_path']}" for img in data.get("posters", [])]
        return posters
    else:
        print("Failed to fetch images:", response.text)
        return []

# Function to recommend similar movies
def recommend(movie):
    movie_i = movies[movies["title"] == movie].index[0]
    dist = similarity[movie_i]
    movies_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:6]
    l = []
    for i in movies_list:
        movie_id = i[0]
        l.append(movies.iloc[i[0]].title)
    return l

# Load similarity data
similarity = pickle.load(open("similarity.pkl", "rb"))

# Load movies data
movies_list = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_list)

# Streamlit app title and sidebar
st.set_page_config(page_title="Movie Recommender System", page_icon="🎬", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-image: url('https://source.unsplash.com/collection/10344286/1920x1080');
            font-family: 'Roboto', sans-serif;
            color: #FFFFFF;
        }
        .title-section {
            background: linear-gradient(to right, #000000, #434343);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .title-text {
            font-size: 36px;
            text-align: center;
            margin: 0;
        }
        .movie-title:hover {
            color: #FFD700;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# Title section with gradient background
st.markdown('<div class="title-section"><p class="title-text">Movie Recommender System</p></div>', unsafe_allow_html=True)

# Selectbox to choose a movie
selected_movie_name = st.sidebar.selectbox(
    "Select a movie",
    movies["title"].values
)

# Button to recommend movies
if st.sidebar.button("Recommend"):
    # Fetch recommendations
    recom = recommend(selected_movie_name)
    for movie_title in recom:
        # Display recommended movie title
        st.write(f"<p class='movie-title'>{movie_title}</p>", unsafe_allow_html=True)
        # Fetch and display poster for the recommended movie
        movie_id = movies[movies["title"] == movie_title]["id"].iloc[0]
        posters = fetch_movie_images(movie_id)
        if posters:
            # Display only one poster at a time
            st.image(posters[0], caption="Poster", width=300)
        else:
            st.write("No posters available")

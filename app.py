import streamlit as st
import pickle
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def fetch_poster(movie_id):
  url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US'
  try:
    response = requests.get(url, timeout=30)
    data = response.json()
    # Use .get() to safely avoid KeyError if TMDB returns an error or missing key
    poster_path = data.get('poster_path')
    if poster_path:
      return f'https://image.tmdb.org/t/p/w500/{poster_path}'
  except Exception:
    pass

  # Fallback image if poster fails or doesn't exist
  return 'https://via.placeholder.com/500x750?text=No+Poster'

movies  = pickle.load(open('movies.pkl', 'rb'))


similarity = pickle.load(open('similarty.pkl', 'rb'))

def recomended(movie) :
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:6]

    recomended_movies = []
    recomended_posters = []
    for i in movie_list :
        movie_id = movies.iloc[i[0]].id

        #fetch poster using APIs
        recomended_movies.append(movies.iloc[i[0]].title)
        recomended_posters.append(fetch_poster(movie_id))

    return recomended_movies,recomended_posters

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select Movie",
    movies["title"].values,
)

if st.button("Recommend"):
  names, posters = recomended(selected_movie_name)

  cols = st.columns(5)
  for col, name, poster in zip(cols, names, posters):
    with col:
      # Render poster first for a clean top alignment
      st.image(poster, use_container_width=True)

      # Styled title container with fixed height and text truncation
      st.markdown(
          f"""
            <div style="
                font-weight: 600; 
                font-size: 15px; 
                text-align: center; 
                margin-top: 8px; 
                height: 45px; 
                overflow: hidden; 
                text-overflow: ellipsis; 
                display: -webkit-box; 
                -webkit-line-clamp: 2; 
                -webkit-box-orient: vertical;">
                {name}
            </div>
            """,
          unsafe_allow_html=True,
      )

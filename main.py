import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(mv_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=5e5f065d08b8a4fb812b77f3187bf8e9&language=en-US'.format(mv_id))
    data=response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(mv):
    movie_idx = movies[movies['title'] == mv].index[0]
    distances = similarity[movie_idx]
    movies_lst = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    rec = []
    rec_pstrs = []
    for mv in movies_lst:
        rec.append(movies.iloc[mv[0]].title)
        rec_pstrs.append(fetch_poster(movies.iloc[mv[0]].movie_id))
    return rec, rec_pstrs


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies)

print(movies)
st.title('Movie Recommendation System')

option = st.selectbox(
    'What movie do you like the most?',
    movies['title'].values)

st.write('You selected:', option)

if st.button('Recommend'):
    rc,pstr = recommend(option)
    for r in rc:
        st.write(r)
    # st.write('You clicked the button!', option)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(rc[0])
        st.image(pstr[0])
    with col2:
        st.text(rc[1])
        st.image(pstr[1])
    with col3:
        st.text(rc[2])
        st.image(pstr[2])
    with col4:
        st.text(rc[3])
        st.image(pstr[3])
    with col5:
        st.text(rc[4])
        st.image(pstr[4])

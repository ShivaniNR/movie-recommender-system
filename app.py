import streamlit as st
import pickle
import requests

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_movie_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    poster = "https://image.tmdb.org/t/p/w500/"+data['poster_path']
    return poster


def recommend(movie):
    recommended_list = []
    movie_index = movies[movies['title'] == movie].index[0]    #fetching the id  of the given movie name
    distances = similarity[movie_index]
    movies_index_list = sorted(list(enumerate(distances)), reverse = True, key=lambda x: x[1])[1:6]    #getting the movie based on the index name in reverse order

    
    recommended_movie_posters = []
    for i in movies_index_list:
        recommended_list.append(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_movie_poster(movie_id))
    return recommended_list, recommended_movie_posters

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    "Select the movie",
    movies_list,
)

#st.write("You selected:", selected_movie)
if st.button('RECOMMEND'):
    recommendations, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(posters[1])

    with col3:
        st.text(recommendations[2])
        st.image(posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(posters[4])
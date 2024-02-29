import pickle
import streamlit as st
import requests

st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white; /* Change text color to white for better visibility */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

st.header('Movie Recommender System')
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Display the recommended movies in two columns
    cols = st.columns(2)
    for i in range(0, len(recommended_movie_names), 2):
        with cols[0]:
            if i < len(recommended_movie_names):
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i], use_column_width=True)
                # Add an expander for each movie to show details
                with st.expander(f"Details for {recommended_movie_names[i]}"):
                    movie_details = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movies.iloc[i]['movie_id'])).json()
                    st.write("Release Date:", movie_details['release_date'])
                    st.write("Overview:", movie_details['overview'])
                    st.write("Vote Average:", movie_details['vote_average'])
                    st.write("Vote Count:", movie_details['vote_count'])
                    st.write("Popularity:", movie_details['popularity'])
                    st.write("Original Language:", movie_details['original_language'])
                    st.write("---")
        with cols[1]:
            if i + 1 < len(recommended_movie_names):
                st.text(recommended_movie_names[i + 1])
                st.image(recommended_movie_posters[i + 1], use_column_width=True)
                # Add an expander for each movie to show details
                with st.expander(f"Details for {recommended_movie_names[i + 1]}"):
                    movie_details = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movies.iloc[i + 1]['movie_id'])).json()
                    st.write("Release Date:", movie_details['release_date'])
                    st.write("Overview:", movie_details['overview'])
                    st.write("Vote Average:", movie_details['vote_average'])
                    st.write("Vote Count:", movie_details['vote_count'])
                    st.write("Popularity:", movie_details['popularity'])
                    st.write("Original Language:", movie_details['original_language'])
                    st.write("---")


from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from fastapi.middleware.cors import CORSMiddleware
import requests

# Load the necessary data
with open("movies_list.pkl", "rb") as f:
    movies = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust to match the URL of your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input data model
class RecommendRequest(BaseModel):
    liked_movies: list

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path

# Recommendation function
def recommend(movie_title):
    try:
        index = movies[movies['title'] == movie_title].index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
        # recommended_movies = [new_data.iloc[i[0]].title for i in distance[1:6]]  # Exclude the input movie
        # return recommended_movies
        recommend_movie=[]
        recommend_poster=[]
        for i in distance[1:6]:
            movies_id=movies.iloc[i[0]].id
            recommend_movie.append(movies.iloc[i[0]].title)
            recommend_poster.append(fetch_poster(movies_id))
        return recommend_movie, recommend_poster
    except IndexError:
        return []

# FastAPI route
@app.post("/recommend")
async def recommend_movies(request: RecommendRequest):
    # Assume the user sends at least one liked movie, modify if more complex handling needed
    recommendations = recommend(request.liked_movies[0])  # Using the first liked movie
    return {"recommendations": recommendations}

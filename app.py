# Import necessary libraries
from flask import Flask, render_template, request
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load and preprocess data
def load_data():
    conn = sqlite3.connect('movies.db')
    movies_df = pd.read_sql_query("SELECT * FROM movies", conn)
    conn.close()
    return movies_df

# Create TF-IDF matrix
def create_tfidf_matrix(movies_df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['genres'])
    return tfidf_matrix

# Get movie recommendations
def get_recommendations(movie_id, cosine_sim, movies_df):
    idx = movies_df.index[movies_df['id'] == movie_id].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movies_df['title'].iloc[movie_indices].tolist()

# Load data and create TF-IDF matrix
movies_df = load_data()
tfidf_matrix = create_tfidf_matrix(movies_df)
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

@app.route('/')
def home():
    return render_template('index.html', movies=movies_df['title'].tolist())

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['movie']
    movie_id = movies_df[movies_df['title'] == movie_title]['id'].values[0]
    recommendations = get_recommendations(movie_id, cosine_sim, movies_df)
    return render_template('recommendations.html', movie=movie_title, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
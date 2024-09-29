from flask import Flask, render_template, request
import pickle
import numpy as np

# Loading necessary pickle files
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_score.pkl', 'rb'))

app = Flask(__name__)

# Index route to render the homepage
@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values),
                           year_of_publication=list(popular_df['Year-Of-Publication'].values)  # Added this line
                           )

# Route to render the recommendation UI
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

# Recommendation route
@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    # Check if the user_input exists in the index
    if user_input in pt.index:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))

            data.append(item)
        print(data)  # Check if the year is being appended

        return render_template('recommend.html', data=data)

    # If the book is not found, handle gracefully
    else:
        return render_template('recommend.html', error="Book not found! Please try another one.")

if __name__ == '__main__':
    app.run(debug=True)

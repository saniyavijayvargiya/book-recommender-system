from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

populardf = pickle.load(open("book-recommender-system\Top50Books.pkl", "rb"))
finaldf = pickle.load(open("book-recommender-system\FinalList.pkl", "rb"))
books = pickle.load(open("book-recommender-system\Books.pkl", "rb"))
similarity_score = pickle.load(open("book-recommender-system\SimilarityScore.pkl", "rb"))

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html",
                           book_name = list(populardf["Book-Title"].values),
                           author = list(populardf["Book-Author"].values),
                           image = list(populardf["Image-URL-M"].values),
                           votes = list(populardf["Num-Ratings"].values),
                           rating = list((populardf["Avg-Rating"].values).round(decimals = 3)))


@app.route("/recommend")
def recommendpage():
    books = list(finaldf.index.values)
    return render_template("recommend.html",
                    book_names = books)


@app.route("/recommendbooks", methods = ["post"])
def recommendbooks():
    book_name = request.form.get("book_name")
    index = np.where(finaldf.index == book_name)[0][0]    #gives the index of the parameter book name 
    
    distances = similarity_score[index]
    
    similar_books = sorted(list(enumerate(distances)), key = lambda x: x[1], reverse = True)[1:6]
    
    suggestions = []
    for i in similar_books:
        item = [] 
        temp = books[books["Book-Title"] == finaldf.index[i[0]]]
        temp = temp.drop_duplicates("Book-Title")
       
        item.append(list(temp["Book-Title"].values)[0])
        item.append(list(temp["Book-Author"].values)[0])
        item.append(list(temp["Image-URL-M"].values)[0])
        
        suggestions.append(item)
    
    return render_template("recommend.html", suggestions = suggestions)


if __name__ == "__main__":
    app.run(debug = True)
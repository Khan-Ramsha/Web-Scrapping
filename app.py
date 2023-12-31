from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen 
import pymongo
import pandas as pd

app = Flask(__name__)  # initializing a flask app


@app.route("/", methods=["GET"])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route("/review", methods=["POST", "GET"])  
@cross_origin()
def index():
    if request.method == "POST":
        searchString = request.form["content"].replace(" ", "")
        url = "https://www.nike.com/in/w?q=" + searchString

        filename = searchString + ".csv"
        fw = open(filename, "w", encoding='utf-8')
        headers = "Product_Name,Prices,Product_Subtitle,Product_Color_Count\n"
        fw.write(headers)

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser') 
        Product_name = [i.text for i in soup.find_all("a", class_="product-card__link-overlay")]
        Price = [i.text for i in soup.find_all("div", class_="product-price")]
        subtitle = [i.text for i in soup.find_all("div", class_="product-card__subtitle")]
        Color = [i.text for i in soup.find_all("div", class_="product-card__product-count")]

        # Create a DataFrame from the dictionary with NaN for missing values
        mydict = {"Product_Name": Product_name, "Prices": Price, "Product_Subtitle": subtitle, "Product_Color_Count": Color}
        df = pd.DataFrame.from_dict(mydict, orient='index').transpose()

        # Save DataFrame to CSV
        df.to_csv(filename, index=False, encoding='utf-8')
        # Convert DataFrame to a list of dictionaries
        records = df.to_dict(orient='records')
        client =pymongo.MongoClient('mongodb+srv://khan-ramsha:<password>@cluster0.gnvdais.mongodb.net/?retryWrites=true&w=majority')
        db=client['scrap']
        col=db['scrap_data']
        col.insert_many(records) # Insert records into MongoDB
        return render_template('results.html', mydict=mydict) 
    
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

	
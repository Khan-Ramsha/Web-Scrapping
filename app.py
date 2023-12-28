from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen 
import pymongo

app = Flask(__name__)  # initializing a flask app


@app.route("/", methods=["GET"])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route(
    "/review", methods=["POST", "GET"]
)  # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == "POST":
        searchString = request.form["content"].replace(" ", "")
        url = "https://www.nike.com/in/w?q=" + searchString
        
        filename = searchString + ".csv"
        fw = open(filename, "w")
        headers = "Product_Name,Prices,Product_Subtitle,Product_Color_Count  \n"
        fw.write(headers)
        reviews = []

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser') 
        Product_name=[]
        names=soup.find_all("a",class_="product-card__link-overlay")
        for i in names:
           name= i.text
           print(name)
           Product_name.append(name)
        
        Price=[]
        soup = BeautifulSoup(r.text, 'html.parser') 
        price=soup.find_all("div",class_="product-price")
        for i in price:
            prices = i.text
            Price.append(prices)
        #d-sm-ib pl4-sm
        # Stars=[]
        # stars=soup.find_all("div",class_="detail")
        # for i in stars:
        #   star = i.text
        # Stars.append(star)
        
        subtitle=[]
        soup = BeautifulSoup(r.text, 'html.parser') 
        sub=soup.find_all("div",class_="product-card__subtitle")
        for i in sub:
            sub = i.text
            subtitle.append(sub)
        
        Color=[]
        soup = BeautifulSoup(r.text, 'html.parser') 
        color=soup.find_all("div",class_="product-card__product-count")
        for i in color:
            color = i.text
            # print(color)
            Color.append(color)
        mydict = {"Product_Name": Product_name, "Prices": Price, "Product_Subtitle": subtitle, "Product_Color_Count": Color}
        print(mydict)
        return render_template('results.html',  mydict=mydict) 
    
    else:
        return render_template('index.html')
    
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5001, debug=True)
	#app.run(debug=True)


# tune band kar di print() ??haa chalu kar 
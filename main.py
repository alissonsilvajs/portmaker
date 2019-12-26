# -*- coding: utf-8 -*-

# Import the libraries
import os
import time
from termcolor import colored
from progress.bar import Bar
import Algorithmia
from google_images_search import GoogleImagesSearch
from progress.bar import ShadyBar
import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# Open the keys 
with open('keys/algorithimia.json') as f:
  keyAlgorithimia = json.load(f)

with open('keys/google-search.json') as f:
  keyGoogleSearch = json.load(f)

# Define the key of Google Search Engine
gis = GoogleImagesSearch(keyGoogleSearch['key'], keyGoogleSearch['cx'])

# Define the key of Algorithmia
client = Algorithmia.client(keyAlgorithimia['key'])

# Import the template of portfolio
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("templates/index.html")

# Function for search article on Wikipedia
def searchArticle(article):

    input = {
    "articleName": article,
    "lang": "pt"
    }
    
    algo = client.algo('web/WikipediaParser/0.1.2')
    algo.set_options(timeout=300)

    result = algo.pipe(input).result['summary']

    if(result.find('(') == -1):
        findDot = result.find('. ')
        findDot = findDot + 1

        if(findDot < 200):
            findDot = result.find('. ', findDot)

        resultReplaced = result[:findDot]
    else:
        cutLineA = result.find('(')
        cutLineA = cutLineA - 1

        cutLineB = result.find(')')
        cutLineB = cutLineB + 1

        cutReplaceA = result[:cutLineA]

        findDot = result.find('. ')
        findDot = findDot + 1

        if(findDot < 300):
            findDot = result.find('. ', findDot)
            findDot = findDot + 1 

        if(findDot < 300):
            findDot = result.find('. ', findDot)
            findDot = findDot + 1 

        resultReplaced = cutReplaceA + result[cutLineB:findDot]
    return resultReplaced

# Function for search image of article
def searchImageArticle(imageArticle):

    _search_params = {'q': imageArticle, 'num': 1}

    gis.search(search_params=_search_params)
    for image in gis.results():
        url = image.url

    return url

def searchArticlesandImages(array):

    arrayImage = []
    arrayArticle = []

    arrayBar = len(array)
    bar = ShadyBar('Processing', max=arrayBar)

    for x in array:
        resultImage = searchImageArticle(x)
        arrayImage.append(resultImage)
        resultArticle = searchArticle(x)
        arrayArticle.append(resultArticle)

        bar.next()
        pass 
    bar.finish()

    return arrayArticle, arrayImage 

def generateOutput(name,title,content):

    getVars = {
        'title': title,
        'name': name,
    }

    print(colored('v1.3.0', 'magenta'))
    print('')
    print(colored('github => alissonsilvajs', 'red'))
    print(colored('instagram => alissonsilva.py', 'red'))
    print(colored('All right reserved © Copyright 2019. Developed by Alisson Silva.', 'red'))

    print('')

    arrayArticle, arrayImage = searchArticlesandImages(content)

    lenImage = len(content)

    for x in range(lenImage): 

        content = "content" + str(x)
        getVars[content] = arrayArticle[x]
        article = "article" + str(x)
        getVars[article] = content[x]
        image = "image" + str(x)
        getVars[image] = arrayImage[x]  

        pass

    html_out = template.render(getVars)

    print(colored("Sucessfull!", 'yellow'))
    HTML(string=html_out).write_pdf("output/portfolio.pdf")

# Main script

if __name__ == '__main__':

    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("-n", "--name", dest="name", help="Name")
    parser.add_option("-t", "--title", dest="title", help="Title")
    parser.add_option("-c", "--content", dest="content", help="Articles = Geometria,Aquecimento Global")

    options, args = parser.parse_args()

    name = options.name
    title = options.title
    content = []
    content = options.content
    content = content.split(',')

    generateOutput(name, title, content)
                                                                                                                                                                           
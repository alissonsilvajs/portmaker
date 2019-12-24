# -*- coding: utf-8 -*-
import os
from termcolor import colored
from progress.bar import Bar
import time
import Algorithmia
from google_images_search import GoogleImagesSearch
from progress.bar import ShadyBar
import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

with open('keys/algorithimia.json') as f:
  keyAlgorithimia = json.load(f)

with open('keys/google-search.json') as f:
  keyGoogleSearch = json.load(f)

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("templates/index.html")

gis = GoogleImagesSearch(keyGoogleSearch['key'], keyGoogleSearch['cx'])
client = Algorithmia.client(keyAlgorithimia['key'])

clear = lambda: os.system('clear')
clear()

print (colored('''
,-.----.                                                                                          
\    /  \                         ___              ____                   ,-.                     
|   :    \                      ,--.'|_          ,'  , `.             ,--/ /|                     
|   |  .\ :   ,---.    __  ,-.  |  | :,'      ,-+-,.' _ |           ,--. :/ |             __  ,-. 
.   :  |: |  '   ,'\ ,' ,'/ /|  :  : ' :   ,-+-. ;   , ||           :  : ' /            ,' ,'/ /| 
|   |   \ : /   /   |'  | |' |.;__,'  /   ,--.'|'   |  || ,--.--.   |  '  /      ,---.  '  | |' | 
|   : .   /.   ; ,. :|  |   ,'|  |   |   |   |  ,', |  |,/       \  '  |  :     /     \ |  |   ,' 
;   | |`-' '   | |: :'  :  /  :__,'| :   |   | /  | |--'.--.  .-. | |  |   \   /    /  |'  :  /   
|   | ;    '   | .; :|  | '     '  : |__ |   : |  | ,    \__\/: . . '  : |. \ .    ' / ||  | '    
:   ' |    |   :    |;  : |     |  | '.'||   : |  |/     ," .--.; | |  | ' \ \'   ;   /|;  : |    
:   : :     \   \  / |  , ;     ;  :    ;|   | |`-'     /  /  ,.  | '  : |--' '   |  / ||  , ;    
|   | :      `----'   ---'      |  ,   / |   ;/        ;  :   .'   \;  |,'    |   :    | ---'     
`---'.|                          ---`-'  '---'         |  ,     .-./'--'       \   \  /           
  `---`                                                 `--`---'                `----'            
''', 'yellow'))                                                                                                                                                                                    
print(colored('v1.3.0', 'magenta'))
print('')
print(colored('github => alissonsilvajs', 'red'))
print(colored('instagram => alissonsilva.py', 'red'))
print(colored('All right reserved © Copyright 2019. Developed by Alisson Silva.', 'red'))

print('')

with Bar('Processing', max=20) as bar:
    for i in range(20):
        bar.next()
        time.sleep(.100)
    pass

bar.finish()

time.sleep(1)

print(colored('Type the topics for portfolio.', 'yellow'))
array = []
array = input(colored('Example => Geometria,Aquecimento Global \n> ', 'magenta'))
array = array.split(',')

print('')
print(colored(array, 'red'))
print('')
sure = input(colored('Are you sure? Y/n \n> ' ,'yellow'))

if (sure == "n" or sure == "N"):
    exit()


def searchArticle(article):

    input = {
    "articleName": article,
    "lang": "pt"
    }
    
    algo = client.algo('web/WikipediaParser/0.1.2')
    algo.set_options(timeout=300) # optional

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

def searchImageArticle(imageArticle):

    _search_params = {'q': imageArticle, 'num': 1}

    gis.search(search_params=_search_params)
    for image in gis.results():
        url = image.url

    return url

maxbar = len(array)
print('')
bar = ShadyBar('Processing', max=maxbar)

arrayImage = []
arrayArticle = []

for x in array:
    #resultImage = searchImageArticle(x)
    #arrayImage.append(resultImage)
    resultArticle = searchArticle(x)
    arrayArticle.append(resultArticle)

    bar.next()
    pass 
bar.finish()
print('')
portfolio_name = input(colored("What's your name? \n> " ,'yellow'))
print('')
portfolio_id = input(colored("How do you want calls this portfolio? \n> " ,'magenta'))
print('')
getVars = {
    'title': portfolio_id,
    'name': portfolio_name, 
}

lenArray = len(arrayImage)

bar = ShadyBar('Generating', max=maxbar)
for x in range(lenArray): 

    content = "content" + str(x)
    getVars[content] = arrayArticle[x]
    article = "article" + str(x)
    getVars[article] = array[x]
    image = "image" + str(x)
    getVars[image] = arrayImage[x]  
    bar.next()

    pass

bar.finish()

html_out = template.render(getVars)
HTML(string=html_out).write_pdf("output/portfolio.pdf")

print('')

print(colored("Sucessfull!", 'yellow'))
print(colored('All right reserved © Copyright 2019. Developed by Alisson Silva.', 'magenta'))
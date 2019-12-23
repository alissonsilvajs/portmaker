import Algorithmia
from google_images_search import GoogleImagesSearch
from progress.bar import ShadyBar
import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("index.html")

gis = GoogleImagesSearch('AIzaSyB4hmYFpThrSIhn8idx94Z67w7zi6VWn6Q', '002280090757924293604:fs75zw78et9')
client = Algorithmia.client('simNstF6swzH7mgCRl6i9AWP3t91')

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

array = ['Geometria', 'Aquecimento Global']
maxbar = len(array)
bar = ShadyBar('Processing', max=maxbar)

arrayImage = []
arrayArticle = []

for x in array:
    resultImage = searchImageArticle(x)
    arrayImage.append(resultImage)
    resultArticle = searchArticle(x)
    arrayArticle.append(resultArticle)

    bar.next()
    pass 
bar.finish()

portfolio_id = "Humanas"
portfolio_name = "Alisson" 

getVars = {
    'title': portfolio_id,
    'name': portfolio_name, 
}

lenArray = len(arrayImage)

for x in range(lenArray): 

    content = "content" + str(x)
    getVars[content] = arrayArticle[x]
    article = "article" + str(x)
    getVars[article] = array[x]
    image = "image" + str(x)
    getVars[image] = arrayImage[x]    
    pass

print(getVars)

html_out = template.render(getVars)
HTML(string=html_out).write_pdf("report.pdf")

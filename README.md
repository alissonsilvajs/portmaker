# Portmaker

Bot for create portfolios. 📁 

# How does it works

The bot uses Algorithmia and Google Search Engine to create portfolios with school subjects.

# Algorithmia

The Algorithmia is used to search articles in Wikipedia using WikipediaParser.

- Create an Algorithmia account and then generate a API KEY.

![portmaker](https://raw.githubusercontent.com/alissonsilvajs/portmaker/master/imgs/algorithmia.png)

# Google Search API

The Google Search API is used to images on Google.

- Create a project on Google Cloud Platform and activate the Custom Search API.

![portmaker](https://raw.githubusercontent.com/alissonsilvajs/portmaker/master/imgs/googlecloudplatform.png)

- After that, create a new search engine on Google Custom Search Engine and copy the search engine ID.

![portmaker](https://raw.githubusercontent.com/alissonsilvajs/portmaker/master/imgs/googlecustomsearchcreate.png)

![portmaker](https://raw.githubusercontent.com/alissonsilvajs/portmaker/master/imgs/googlecustomsearchkey.png)

# Requeriments

To install the requeriments: `pip install -r requirements.txt`

# Usage

To run the script:

```
Usage: main.py [options]

Options:
  -h, --help            show this help message and exit
  -n NAME, --name=NAME  Name
  -t TITLE, --title=TITLE
                        Title
  -c CONTENT, --content=CONTENT
                        Articles = Geometria,Aquecimento Global
```

Example: `python main.py -n Alisson -t Humanas -c Geometria,Aquecimento Global`

# Credits

- [Alisson Silva](https://github.com/alissonsilvajs)

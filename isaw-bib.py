# isaw-bib.py

from flask import Flask, render_template
import requests
import json
from chainmap import ChainMap
from pprint import pprint

from pyzotero import zotero

app = Flask(__name__, instance_relative_config=True)

# *** File with Zotero parameters need to be in 'instance/zotero.cfg' for app to work ***
app.config.from_pyfile('zotero.cfg')
app.config['DEBUG'] = True


@app.route('/')
def homepage():

    # Store keys elsewhere
    #params = {
    #    'library_id': app.config['LIBRARY_ID'], 
    #    'library_type': app.config['LIBRARY_TYPE'], 
    #    'api_key': app.config['API_KEY']
    #}
    
    # Access Zotero library via API
    # zotero.Zotero(ID, 'user', KEY)
    z = zotero.Zotero(app.config['LIBRARY_ID'],app.config['LIBRARY_TYPE'],app.config['API_KEY'])
    isawbib = z.everything(z.top())
    count = len(isawbib)
    tags = get_tags(isawbib)
    return render_template('isaw-bib.html', isawbib=isawbib, count=count)


@app.route('/<fac>')
def bibliography(fac):
    # Store keys elsewhere
    # Access Zotero library via API
    # zotero.Zotero(ID, 'user', KEY)
    z = zotero.Zotero(app.config['LIBRARY_ID'],app.config['LIBRARY_TYPE'],app.config['API_KEY'])
    #isawbib = z.everything(z.top())
    # Note that you can get bib info with this:
    isawdata = z.everything(z.top())
    isawbib = z.everything(z.top(content='bib', style='chicago-author-date'))
    
    test = []
    
    for i, item in enumerate(isawdata):
        for tag in item['data']['tags']:
            if tag['tag'] == fac:
                test.append(isawbib[i])    
    return render_template('faculty.html', isawbib=test, fac=_format_fac(fac))


def _format_fac(name):
    names = name.split('-')
    names = [name.title() for name in names]
    names = " ".join(names)
    return names


def get_tags(collection):
    tags = []
    for item in collection:
        if item['data']['tags']:
          tags.extend(item['data']['tags'])
    return set([v for d in tags for k, v in d.items()])


if __name__ == '__main__':
  app.run()
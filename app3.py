from flask import Flask, render_template, request, json
from elasticsearch import Elasticsearch
import re

app = Flask(__name__)
es = Elasticsearch()

@app.route('/',methods=["GET","POST"])
def index():
    q = request.values.get("q")
    catval = request.values.get("catval")
    #print(type(catval))
    print(q)
    if q is not None:
        if catval == "allcat":
            resp = es.search(index='ayushmanidx', body={"query": {"simple_query_string": {"query": q, "fields":["NAME","SYNONYMS.Sanskrit","SYNONYMS.Assamese","SYNONYMS.Bengali","SYNONYMS.English","SYNONYMS.Gujrati","SYNONYMS.Hindi","SYNONYMS.Kannada","SYNONYMS.Kashmiri","SYNONYMS.Malayalam","SYNONYMS.Marathi","SYNONYMS.Oriya","SYNONYMS.Punjabi","SYNONYMS.Tamil","SYNONYMS.Telugu","SYNONYMS.Urdu","CONSTITUENTS","DESCRIPTION.Macroscopic","DESCRIPTION.Microscopic","PROPERTIES AND ACTION.Rasa","PROPERTIES AND ACTION.Guna","PROPERTIES AND ACTION.Sita","PROPERTIES AND ACTION.Vipaka","PROPERTIES AND ACTION.Karma","IMPORTANT FORMULATIONS","THERAPEUTIC USES","ABOUT"]}}},size=10000)
        elif catval == "constit":
            resp = es.search(index='ayushmanidx', body={"query": {"multi_match": {"query": q, "fields":["CONSTITUENTS"]}}},size=10000)
        elif catval == "theruse":
            resp = es.search(index='ayushmanidx', body={"query": {"multi_match": {"query": q, "fields":["THERAPEUTIC USES"]}}},size=10000)
        elif catval == "panda":
            resp = es.search(index='ayushmanidx', body={"query": {"multi_match": {"query": q, "fields":["PROPERTIES AND ACTION.Rasa","PROPERTIES AND ACTION.Guna","PROPERTIES AND ACTION.Sita","PROPERTIES AND ACTION.Vipaka","PROPERTIES AND ACTION.Karma"]}}}, size=10000)
        elif catval == "synon":
            resp = es.search(index='ayushmanidx', body={"query": {"multi_match": {"query": q, "fields":["SYNONYMS.Sanskrit","SYNONYMS.Assamese","SYNONYMS.Bengali","SYNONYMS.English","SYNONYMS.Gujrati","SYNONYMS.Hindi","SYNONYMS.Kannada","SYNONYMS.Kashmiri","SYNONYMS.Malayalam","SYNONYMS.Marathi","SYNONYMS.Oriya","SYNONYMS.Punjabi","SYNONYMS.Tamil","SYNONYMS.Telugu","SYNONYMS.Urdu"]}}},size=10000)
        #for io in resp['hits']['hits']:
            #print(io)
        return render_template('index.html', q=q, response=resp['hits']['hits'])

    return render_template('index.html')



@app.route('/index2',methods=["GET","POST"])
def index2():
    andwords = request.values.get("andwords")
    exactwords = request.values.get("exactwords")
    orwords = request.values.get("orwords")
    notwords = request.values.get("notwords")

    if andwords is not None:
        andwords = andwords.strip()
        andwords = "+" + andwords.replace(" ", " +")
    else:
        andwords = ""


    if exactwords is not None:
        exactwords = exactwords.strip()
        exactwords = ' +" ' + exactwords + ' "'
    else:
        exactwords = ""

    if orwords is not None:
        orwords = orwords.strip()
        orwords = orwords.replace(" ", " |")
    else:
        orwords = ""

    if notwords is not None:
        notwords = notwords.strip()
        notwords = ' +-' + notwords.replace(" ", " +-")
    else:
        notwords = ""

    q = orwords + andwords + exactwords + notwords
    print(q)

    if q is not None:
        resp = es.search(index='ayushmanidx', body={"query": {"simple_query_string": {"query": q, "fields":["NAME","SYNONYMS.Sanskrit","SYNONYMS.Assamese","SYNONYMS.Bengali","SYNONYMS.English","SYNONYMS.Gujrati","SYNONYMS.Hindi","SYNONYMS.Kannada","SYNONYMS.Kashmiri","SYNONYMS.Malayalam","SYNONYMS.Marathi","SYNONYMS.Oriya","SYNONYMS.Punjabi","SYNONYMS.Tamil","SYNONYMS.Telugu","SYNONYMS.Urdu","CONSTITUENTS","DESCRIPTION.Macroscopic","DESCRIPTION.Microscopic","PROPERTIES AND ACTION.Rasa","PROPERTIES AND ACTION.Guna","PROPERTIES AND ACTION.Sita","PROPERTIES AND ACTION.Vipaka","PROPERTIES AND ACTION.Karma","IMPORTANT FORMULATIONS","THERAPEUTIC USES","ABOUT"]}}},size=10000)
        return render_template('index2.html', q=q, response=resp['hits']['hits'])
    return render_template('index2.html')

if __name__ =="__main__":
    app.run(debug=True)


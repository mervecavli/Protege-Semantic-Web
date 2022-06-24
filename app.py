from flask import Flask, render_template, request, redirect, session, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)
app.secret_key = 'danceschoolontologyproject'


prefixquery = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX test:<http://www.dance-school.com/ontology#>
                """

sparqlendpoint = SPARQLWrapper("http://localhost:3030/DanceSchoolOnto/sparql")


@app.route('/')
def hi():
    return "Hi"


@app.route('/home')
def myhome():
    try:
        sparqlendpoint.setQuery(prefixquery + """
                                    SELECT DISTINCT ?class ?label ?description
                                    WHERE {
                                      ?class a owl:Class.
                                      OPTIONAL { ?class rdfs:label ?label}
                                      OPTIONAL { ?class rdfs:comment ?description}
                                    }
                                    """)
        sparqlendpoint.setReturnFormat(JSON)
        results = sparqlendpoint.query().convert()

        sparqlendpoint.setQuery(prefixquery + """
                                            SELECT DISTINCT ?individual ?class ?label
                                            WHERE { 
                                                ?individual rdf:type owl:NamedIndividual .
                                                   
                                            }
                                            """) #?class rdf:type owl:Class .
        sparqlendpoint.setReturnFormat(JSON)
        results1 = sparqlendpoint.query().convert()
        #print(results)

        sparqlendpoint.setQuery(prefixquery + """
                                                    SELECT ?indv ?schedule
                                                    where {
                                                        ?indv a test:Beginner .
                                                        ?indv test:schedule ?schedule .
                                                    }
                                                    """)
        sparqlendpoint.setReturnFormat(JSON)
        results2 = sparqlendpoint.query().convert()
        # print(results)

        sparqlendpoint.setQuery(prefixquery + """
                                                SELECT ?indv ?stdgender ?stdlevel ?placement
                                                where {
                                                    ?indv a test:Student .
                                                    ?indv test:studentGender ?stdgender .
                                                    ?indv test:studentLevel ?stdlevel .
                                                    ?indv test:takesPlacementTest ?placement .
                                                }            
                                              """)
        sparqlendpoint.setReturnFormat(JSON)
        results3 = sparqlendpoint.query().convert()
        # print(results)

        return render_template("index.html", data=results, data1=results1, data2=results2, data3=results3)
    except Exception as msg:
        print("error",msg)


if __name__ == "__main__":
    app.run(debug=True)


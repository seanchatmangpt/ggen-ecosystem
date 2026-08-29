from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("language-tag", '''PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?value WHERE { ?s rdfs:label ?label . BIND(LANG(?label) AS ?value) } ORDER BY ?value''', 2)


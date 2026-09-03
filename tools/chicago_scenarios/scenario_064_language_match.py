from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("language-match", '''PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?value WHERE { ?s rdfs:label ?value . FILTER(LANGMATCHES(LANG(?value), "en")) } ORDER BY ?value''', 2)


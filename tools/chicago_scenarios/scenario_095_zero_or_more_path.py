from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("zero-or-more-path", '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?value WHERE { ?s rdf:type* ?value } ORDER BY ?value''', 5)


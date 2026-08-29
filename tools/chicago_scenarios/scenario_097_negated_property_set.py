from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("negated-property-set", '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?value WHERE { ?s !rdf:type ?value } ORDER BY ?value''', 10)


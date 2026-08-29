from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("group-by-type", '''SELECT (COUNT(?s) AS ?value) WHERE { ?s a ?type } GROUP BY ?type ORDER BY ?value''', 3)

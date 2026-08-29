from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("distinct-type", '''SELECT DISTINCT ?value WHERE { ?s a ?value } ORDER BY ?value''', 3)

from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("predicate-inventory", '''SELECT DISTINCT ?value WHERE { ?s ?value ?o } ORDER BY ?value''', 10)

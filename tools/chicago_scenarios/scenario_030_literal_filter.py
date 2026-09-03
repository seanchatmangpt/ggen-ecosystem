from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("literal-filter", '''SELECT ?value WHERE { ?s ?p ?value . FILTER(isLiteral(?value)) } ORDER BY ?value''', 1)

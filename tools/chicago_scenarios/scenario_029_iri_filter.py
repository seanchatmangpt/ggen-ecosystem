from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("iri-filter", '''SELECT ?value WHERE { ?value ?p ?o . FILTER(isIRI(?value)) } ORDER BY ?value''', 1)

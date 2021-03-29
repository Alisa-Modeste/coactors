from py2neo.matching import NodeMatch

class AugmentedNodeMatch:
    def __init__(self, graph, labels=frozenset(), predicates=tuple(), order_by=tuple(), skip=None, limit=None):
        self.graph = graph
        self._labels = frozenset(labels)
        self._predicates = tuple(predicates)
        self._order_by = tuple(order_by)
        self._skip = skip
        self._limit = limit
        self.has_raw_query = False
        self.partial_raw_query = ""
        self.query_params = {}

    def __len__(self):
        """ Return the number of nodes matched.
        """
        if self.has_raw_query:
            return self.graph.evaluate(self.partial_raw_query + " RETURN count(_)", self.query_params)

        else:
            return self.graph.evaluate(*self._query_and_parameters(count=True))


    def __iter__(self):
        """ Iterate through all matching nodes.
        """
        if self.has_raw_query:
            for record in self.graph.run(self.partial_raw_query + " RETURN _", self.query_params):            
                yield record[0]

        else:
            for record in self.graph.run(*self._query_and_parameters()):
                yield record[0]

    def raw_query(self, query, params = {}):
        """ Evaluate the selection and return a list of all matched
        :class:`.Node` objects.
        :param query: A raw Cypher query without the RETURN clause

        :return: list of matching :class:`.Node` objects
        """
        self.has_raw_query = True
        self.partial_raw_query = query
        self.query_params = params
        
        return list(self)


NodeMatch.__init__ = AugmentedNodeMatch.__init__
NodeMatch.__len__ = AugmentedNodeMatch.__len__
NodeMatch.__iter__ = AugmentedNodeMatch.__iter__
NodeMatch.raw_query = AugmentedNodeMatch.raw_query
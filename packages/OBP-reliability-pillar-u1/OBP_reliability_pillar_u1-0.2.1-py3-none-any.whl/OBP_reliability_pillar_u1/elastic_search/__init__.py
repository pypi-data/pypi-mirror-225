class elastic_search:
    def __init__(self, session):
        """
        :param session:
        """
        self.session = session

    from .compliance import elastic_search_compliance

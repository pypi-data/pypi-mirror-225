
class dynamodb:
    def __init__(self, session):
        """

        :param session:
        """
        self.session = session

    from .compliance import dynamodb_compliance
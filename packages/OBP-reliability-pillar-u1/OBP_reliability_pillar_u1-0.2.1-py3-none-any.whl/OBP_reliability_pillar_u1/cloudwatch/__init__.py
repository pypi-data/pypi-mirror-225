
class cloudwatch:
    def __init__(self, session):
        """

        :param session:
        """
        self.session = session

    from .compliance import cloudwatch_compliance

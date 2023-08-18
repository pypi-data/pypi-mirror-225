
class elastic_beanstalk:
    def __init__(self, session):
        """

        :param session:
        """
        self.session = session

    from .compliance import elastic_beanstalk_compliance
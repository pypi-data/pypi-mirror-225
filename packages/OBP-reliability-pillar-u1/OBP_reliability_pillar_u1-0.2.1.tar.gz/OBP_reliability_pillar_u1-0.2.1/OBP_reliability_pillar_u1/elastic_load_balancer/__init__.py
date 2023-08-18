class elb:
    def __init__(self, session):
        """

        :param session:
        """
        self.session = session

    from .compliance import elb_compliance

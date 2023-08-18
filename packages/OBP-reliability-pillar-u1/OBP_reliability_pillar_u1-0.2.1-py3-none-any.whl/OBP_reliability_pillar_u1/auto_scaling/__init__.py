
class auto_scaling:
    def __init__(self, session):
        """

        :param session:
        """
        self.session = session

    from .compliance import auto_scaling_compliance

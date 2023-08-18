
class ec2:
    def __init__(self, session):
        """
        :param session:
        """
        self.session = session

    from .compliance import ec2_compliance

class guard_duty:
    def __init__(self, session):
        """
        :param session:
        :return:
        """
        self.session = session

    from .compliance import guard_duty_compliance

from OBP_reliability_pillar_u1.guard_duty.guard_duty_enabled import *


# returns the consolidated guard duty compliance
def guard_duty_compliance(self):
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside guard_duty :: guard_duty_compliance()")

    response = [
        # Already covered in monitoring module, hence commenting here
        # guard_duty_enabled(self)
    ]

    return response

from OBP_reliability_pillar_u1.auto_scaling.launch_config_public_ip_disabled import *
from OBP_reliability_pillar_u1.auto_scaling.asg_elb_healthcheck_required import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks autoscaling compliance
def auto_scaling_compliance(self, regions) -> list:
    logger.info(" ---Inside auto_scaling_compliance()")
    response = [
        launch_config_public_ip_disabled(self, regions),
        # Already covered in monitoring module, hence commenting here
        # asg_elb_healthcheck_required(self)
    ]

    return response

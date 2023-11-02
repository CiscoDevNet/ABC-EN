import logging
from pyats import aetest

logger = logging.getLogger(__name__)

TESTBED = "./testbed.yml"

class TestPing(aetest.Testcase):
    @aetest.setup
    def connect(self, device):
        device.connect(log_stdout=False)

    @aetest.test
    def test(self, device):
        logger.info(device.custom.ping_target)
        result = device.api.ping(address=device.custom.ping_target,
                                 size=1280,
                                 count=500,
                                 timeout=0)
        logger.info(result)


if __name__ == "__main__":
    from pyats.topology import loader

    logger.setLevel(logging.INFO)
    testbed = loader.load(TESTBED)
    aetest.main(device=testbed.devices['inet-rtr1'])


import os
from typing import Dict, Any
import unittest
from sumatra.config import Config

TEST_CONFIG = "/tmp/test-sumatra-config"

TEST_STACK_SERVER_PORTS = [21005, 21015, 21025]

STACK_JSON: Dict[str, Any] = {
    "api_uri": "https://t6m7712cl6.execute-api.us-east-1.amazonaws.com/api",
    "api_vpc_endpoint_ids": [],
    "aws_region": "us-east-1",
    "console_redirect_url": "https://console.qa.sumatra.ai",
    "console_uri": "https://0rb1rea4o0.execute-api.us-east-1.amazonaws.com/console",
    "identity_pool_id": "us-east-1:c11b8475-1d4d-41fb-addf-4fca91af1627",
    "sdk_uri": "https://v7ygtp8i1m.execute-api.us-east-1.amazonaws.com/sdk",
    "sdk_vpc_endpoint_ids": [],
    "user_pool_client_id": "6gt3khjuk0u360p4bfb77jag52",
    "user_pool_domain": "sumatra-qa-user-pool-domain",
    "user_pool_id": "us-east-1_SoSs4RdGb",
}


def _delete_config():
    try:
        os.remove(TEST_CONFIG)
    except FileNotFoundError:
        pass


class TestConfigFile(unittest.TestCase):
    def test_default_instance(self) -> None:
        _delete_config()
        c = Config(TEST_CONFIG)
        c.instance = "my_instance"
        c.save()
        c2 = Config(TEST_CONFIG)
        self.assertEqual(c.instance, c2.instance)

    def test_default_branch(self) -> None:
        _delete_config()
        c = Config(TEST_CONFIG)
        c.instance = "my_instance_a"
        c.default_branch = "my_branch_a"
        c.instance = "my_instance_b"
        c.default_branch = "my_branch_b"
        c.save()
        c2 = Config(TEST_CONFIG)
        c2.instance = "my_instance_a"
        self.assertEqual(c2.default_branch, "my_branch_a")
        c2.instance = "my_instance_b"
        self.assertEqual(c2.default_branch, "my_branch_b")

    def test_stack(self) -> None:
        _delete_config()
        c = Config(TEST_CONFIG)
        c.instance = "my_stack_instance"
        c.update_from_stack(STACK_JSON)
        self.assertEqual(
            c.api_event_url,
            "https://t6m7712cl6.execute-api.us-east-1.amazonaws.com/api/event",
        )
        self.assertEqual(
            c.cognito_auth_url,
            "https://sumatra-qa-user-pool-domain.auth.us-east-1.amazoncognito.com/login",
        )

    def tearDown(self) -> None:
        _delete_config()


if __name__ == "__main__":
    unittest.main()

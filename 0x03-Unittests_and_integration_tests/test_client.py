# test_client.py
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that org returns the correct value"""

        # Arrange
        mock_get_json.return_value = {"org": org_name}

        # Act
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, {"org": org_name})

if __name__ == '__main__':
    unittest.main()

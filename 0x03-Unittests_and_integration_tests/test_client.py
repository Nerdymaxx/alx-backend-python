#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @patch('client.get_json')
    def test_org(self, mock_get_json):
        """Test the org property"""
        expected_payload = {"login": "google", "id": 1}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient("google")
        result1 = client.org
        result2 = client.org  # memoized

        mock_get_json.assert_called_once_with("https://api.github.com/orgs/google")
        self.assertEqual(result1, expected_payload)
        self.assertEqual(result2, expected_payload)

    def test_public_repos_url(self):
        """Test the _public_repos_url property"""
        expected_repos_url = "https://api.github.com/orgs/google/repos"
        payload = {"repos_url": expected_repos_url}

        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, expected_repos_url)
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method"""
        test_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_repos_payload

        mocked_url = "https://api.github.com/orgs/google/repos"

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = mocked_url
            client = GithubOrgClient("google")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(mocked_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license static method"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


# Optional: if you want to separate integration tests
from unittest.mock import patch, Mock

class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_response = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = org_payload
            elif url == org_payload["repos_url"]:
                mock_response.json.return_value = repos_payload
            else:
                mock_response.json.return_value = None
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns all repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos by license"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), apache2_repos)


if __name__ == '__main__':
    unittest.main()

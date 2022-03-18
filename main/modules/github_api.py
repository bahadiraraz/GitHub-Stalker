from github import Github
import github.GithubException

class GithubApi:
	def __init__(self, api_key) -> None:
		self.api_key = api_key
	
	def get_api_followers_info(self):
		"""
		This function get user followers info from GitHub REST API
		"""
		try:
			github_api_info = Github(self.api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().get_followers()

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_api_star_info(self):
		"""
		This function get user star info from GitHub REST API
		"""
		try:
			github_api_info = Github(self.api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().get_repos(visibility="public", affiliation="owner")

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_user_info(self):
		"""
		This function get user info from GitHub REST API
		"""
		try:
			github_api_info = Github(self.api_key)
			github_api_info.get_user().login
			return github_api_info.get_user()

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_following_info(self):
		"""
		This function get user following info from GitHub REST API
		"""
		try:
			github_api_info = Github(self.api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().get_following()

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_user_id(self):
		"""
		This function get user id info from GitHub REST API
		"""
		try:
			github_api_info = Github(self.api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().id

		except github.GithubException:
			raise "missing or incorrect API key"

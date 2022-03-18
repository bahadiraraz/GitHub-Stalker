import os, sys
import github.GithubException
import pandas as pd
from dotenv import load_dotenv
from github import Github
from pick import pick

pd.set_option("display.max_rows", None, "display.max_columns", None)


class GithubApi:

	def get_api_followers_info(self):
		"""
		This function get user followers info from GitHub REST API
		"""
		try:
			github_api_info = Github(api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().get_followers()

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_api_star_info(self):
		"""
		This function get user star info from GitHub REST API
		"""
		try:
			github_api_info = Github(api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().get_repos(visibility="public", affiliation="owner")

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_user_info(self):
		"""
		This function get user info from GitHub REST API
		"""
		try:
			github_api_info = Github(api_key)
			github_api_info.get_user().login
			return github_api_info.get_user()

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_following_info(self):
		"""
		This function get user following info from GitHub REST API
		"""
		try:
			github_api_info = Github(api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().get_following()

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_user_id(self):
		"""
		This function get user id info from GitHub REST API
		"""
		try:
			github_api_info = Github(api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().id

		except github.GithubException:
			raise "missing or incorrect API key"


github_api = GithubApi()


class Functions():

	def __init__(self):
		self.user_csv_path = lambda: os.path.abspath(f"{os.getcwd()}/csvs/{github_api.get_user_id()}.csv")
		self.user_followers_path = lambda: os.path.abspath(
			f"{os.getcwd()}/csvs/{github_api.get_user_id()}_follower_info.csv")
		self.user_following_path = lambda: os.path.abspath(
			f"{os.getcwd()}/csvs/{github_api.get_user_id()}_following.csv")
		self.user_star_path = lambda: os.path.abspath(
			f"{os.getcwd()}/csvs/{github_api.get_user_id()}_stargazers_info.csv")

	def creates_csv(self) -> None:
		"""
		This function create csv files if not exist

		:return: None
		"""
		try:
			self.user_csv().to_csv(self.user_csv_path(), index=False)
			self.user_followers_csv().to_csv(self.user_followers_path(), index=False)
			self.user_following_csv().to_csv(self.user_following_path(), index=False)
			self.user_star_csv().to_csv(self.user_star_path(), index=False)
		except FileNotFoundError:
			os.makedirs(os.path.abspath(f"{os.getcwd()}/csvs"))
			self.creates_csv()
		except OSError:
			os.makedirs(os.path.abspath(f"{os.getcwd()}/csvs"))
			self.creates_csv()

	def update_csv(self, file_name: str) -> None:
		"""
		This function is used to update the csv files.

		:param file_name: The name of the file to be updated.
		:type file_name: str
		:return: None
		:rtype: None
		"""
		options = {self.user_csv_path(): self.user_csv(), self.user_followers_path(): self.user_followers_csv(),
				   self.user_following_path(): self.user_following_csv(), self.user_star_path(): self.user_star_csv()}
		options[file_name].to_csv(file_name, index=False)

	def check_csv(self) -> None:
		"""
		This function check csv file exist or not exist

		:return: None
		"""
		if os.path.isfile(fr"{os.getcwd()}/csvs/{github_api.get_user_id()}.csv") == False:
			print("creating csv file..")
			self.creates_csv()
			MainMenu().run()
		else:
			MainMenu().run()

	def user_csv(self) -> pd.DataFrame:
		"""
		This function create user info csv.

		:return: A dataframe
		"""
		user_df = pd.DataFrame(columns=["id", "user_name"])
		user = github_api.get_user_info()
		user_df = user_df.append({
			"id": user.id,
			"user_name": user.login,
		}, ignore_index=True)

		return user_df

	def user_followers_csv(self) -> pd.DataFrame:
		"""
		This function create user followers info csv.

		:return: A dataframe
		"""
		df = pd.DataFrame(columns=["id", "user_name"])
		for i in github_api.get_api_followers_info():
			df = df.append({
				"id": i.id,
				"user_name": i.login,
			}, ignore_index=True)

		return df

	def user_following_csv(self) -> pd.DataFrame:
		"""
		This function create user following info csv.

		:return: A dataframe
		"""
		df = pd.DataFrame(columns=["id", "user_name"])
		for i in github_api.get_following_info():
			df = df.append({
				"id": i.id,
				"user_name": i.login,
			}, ignore_index=True)

		return df

	def user_fork_csv(self) -> pd.DataFrame:
		"""
		This function create user repo forker info csv .

		:returns: A dataframe
		"""
		df = pd.DataFrame(columns=["id", "forker_name", "repo_name"])
		for i in github_api.get_api_star_info():
			if i.name == "copilot-preview":
				pass
			else:
				for j in i.get_forks():
					df = df.append({
						"id": j.id,
						"forker_name": j.full_name.split("/")[0],
						"repo_name": i.name
					}, ignore_index=True)

		return df

	def user_star_csv(self) -> pd.DataFrame:
		"""
		This function create user stargazers info dataframe csv.

		:return: A dataframe
		"""
		df = pd.DataFrame(columns=["id", "user_name", "repo_name"])
		for i in github_api.get_api_star_info():
			if i.name == "copilot-preview":
				pass
			else:
				for j in i.get_stargazers_with_dates():
					df = df.append({
						"id": j.user.id,
						"user_name": j.user.login,
						"repo_name": i.name
					}, ignore_index=True)

		return df

	def compare_csv(self, df: pd.DataFrame, file_name: str) -> pd.DataFrame:
		"""
		Compares two csv files and prints the differences between them.

		:param df: A dataframe.
		:param file_name: A string.
		:return: A dataframe.
		"""
		id = github_api.get_user_id()

		options = {"1": f"{id}_follower_info.csv", "2": f"{id}_stargazers_info.csv", "3": f"{id}_following.csv"}

		def path() -> os.path:
			return os.path.abspath(os.path.join(rf"{os.getcwd()}/csvs", options.get(file_name)))

		a = pd.read_csv(path())
		a = a.sort_values(by="id")
		# fill nan value with zeros
		df = df.fillna(0)
		df = df.sort_values(by="id")
		if df.equals(a):
			print("no new changes detected")
		elif pd.concat([a, df]).drop_duplicates(keep=False).empty:
			print("no new changes detected")
		else:

			# Find difference between two data frames
			new_df = pd.concat([a, df]).drop_duplicates(keep=False)
			# difference between new_df and a with new data frame with id numbers and user names with fill nan values with old values
			added_df = new_df[~new_df.isin(a)].dropna(axis=0, how='all').fillna(a).reset_index(drop=True)
			try:
				added_df.columns = ["id", "new added users"]
			except ValueError:
				added_df.columns = ["id", "new added users", "repo_name"]
			# print different added rows
			print("no new users added" if added_df.empty else added_df, sep="\n")
			print()
			# difference between new_df and df with new data frame with id numbers and user names with fill nan values with old values
			removed_df = new_df[~new_df.isin(df)].dropna(axis=0, how='all').fillna(df).reset_index(drop=True)
			try:
				removed_df.columns = ["id", "new removed users"]
			except ValueError:
				removed_df.columns = ["id", "new removed users", "repo_name"]
			# print different removed rows
			print("no new remowed users" if removed_df.empty else removed_df, sep="\n")
			# asking if the old data frame will be updated
			a = input("update data Y/N :")
			if a.upper() == "Y":
				functions.update_csv(path())
			elif a.upper() == "N":
				pass

	def most_starred_user(self) -> pd.DataFrame:
		"""
		This function returns a dataframe with the most starred users.

		:return: A dataframe
		"""
		df = pd.DataFrame(columns=["id", "user_name", "repo_name"])
		for i in github_api.get_api_star_info():
			if i.name == "copilot-preview":
				pass
			else:
				for j in i.get_stargazers_with_dates():
					df = df.append({
						"id": j.user.id,
						"user_name": j.user.login,
						"repo_name": i.name
					}, ignore_index=True)
		df = df.groupby("user_name").count()["id"].sort_values(ascending=False).to_frame()
		df.columns = ["star_count"]
		return df.reset_index()

	def most_starred_repo(self) -> pd.DataFrame:
		"""
		This function return most starred repo

		:return: A dataframe
		"""
		df = pd.DataFrame(columns=["id", "user_name", "repo_name"])
		for i in github_api.get_api_star_info():
			if i.name == "copilot-preview":
				pass
			else:
				for j in i.get_stargazers_with_dates():
					df = df.append({
						"id": j.user.id,
						"user_name": j.user.login,
						"repo_name": i.name
					}, ignore_index=True)

		df = df.groupby("repo_name").count()["id"].sort_values(ascending=False).to_frame().reset_index()
		df.columns = ["repo_name", "star_count"]
		return df

	def gt_info(self) -> pd.DataFrame:
		"""
		This function return who doesn’t follow you back

		:return: A dataframe
		"""
		df = self.user_followers_csv().merge(self.user_following_csv(), on="id", how="outer").drop_duplicates(
			keep=False).fillna(0)
		df = df[df["user_name_x"] == 0].drop(columns=["user_name_x"])
		df.rename(columns={"user_name_y": "not follow back users"}, inplace=True)
		return df.reset_index(drop=True)


functions = Functions()


class MainMenu:
	try:

		def __init__(self):
			self.secenek = {
				"1": lambda: functions.compare_csv(functions.user_followers_csv(), "1"),
				"2": lambda: functions.compare_csv(functions.user_star_csv(), "2"),
				"3": lambda: functions.compare_csv(functions.user_following_csv(), "3"),
				"4": lambda: print(functions.gt_info()),
				"5": lambda: print(functions.most_starred_user()),
				"6": lambda: print(functions.most_starred_repo()),
				"7": lambda: print(functions.user_fork_csv()),
				"q": self.quit
			}

		def show_menu(self):
			"""
			This function print main menu
			"""
			print("""
menu
1.followers
2.star
3.following
4.Who doesn’t follow you back
5.who scored the most stars
6.most starred repo
7.who forked your repos
exit to q
    """)

		def run(self):
			"""
			This function run main menu loop
			"""
			while True:
				#title = "Main Menu"
				#options = ['followers', 'star', 'following', 'gt', 'most starred user', 'most starred repo', 'fork','exit']
				#index =pick(options,title)[1]
				self.show_menu()
				options = input("select options: ")
				check_options = self.secenek.get(options.lower())
				if check_options:
					check_options()
				else:
					print(rf"{options} wrong options")

		def quit(self):
			print("byyy")
			sys.exit(0)

	except FileNotFoundError:
		pass

	def main(self):
		"""
		This function create .env file if not exist
		:return:
		"""
		try:
			if os.path.isfile(fr"{os.getcwd()}/env/.env"):
				pass
			else:
				r = os.open("env/.env", os.O_CREAT | os.O_WRONLY)
				key = input("api_key: ")
				os.write(r, f"API_KEY={key}".encode())
				os.close(r)
				print("hello")
		except FileNotFoundError:
			os.makedirs("env")
			self.main()


main_menu = MainMenu()

if __name__ == "__main__":
	main_menu.main()
	load_dotenv(dotenv_path=os.path.abspath(f"env\.env"))
	api_key = os.environ['API_KEY']
	functions.check_csv()

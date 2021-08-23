import os, sys

import github.GithubException
import pandas as pd
from dotenv import load_dotenv
from github import Github

pd.set_option("display.max_rows", None, "display.max_columns", None)


class github_api:
	def __init__(self):
		load_dotenv()
		self.api_key = os.environ["API_KEY"]

	def get_api_followers_info(self):
		try:
			github_api_info = Github(self.api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().get_followers()

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_api_star_info(self):
		try:
			github_api_info = Github(self.api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().get_repos(visibility="public")

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_user_info(self):
		try:
			github_api_info = Github(self.api_key)
			github_api_info.get_user().login
			return github_api_info.get_user()

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_following_info(self):
		try:
			github_api_info = Github(self.api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().get_following()

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_user_id(self):
		try:
			github_api_info = Github(self.api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().id

		except github.GithubException:
			raise "missing or incorrect API key"


github_api = github_api()


def star():
	df = pd.DataFrame(columns=["id", "user_name", "repo_name"])
	for i in github_api.get_api_star_info():
		for j in i.get_stargazers_with_dates():
			df = df.append({
				"id": j.user.id,
				"user_name": j.user.login,
				"repo_name": i.name
			}, ignore_index=True)
	# df = df.sort_values(by=["id"])
	# df.to_csv(f"{os.getcwd()}/star_info.csv",index=False)
	# print(df)
	##who scored how many stars
	# a= df.groupby("user_name").count()["user_id"].sort_values(ascending=False)
	##which repo has how many stars
	# b= df.groupby("repo_name").count()["user_id"].sort_values(ascending=False)
	# print(a)
	# print(b)
	return df


bahadir = github_api.get_user_info()


class Functions:

	def check_csv(self):
		if fr"{github_api.get_user_id()}.csv" not in os.listdir():
			self.bahdir_csv().to_csv(f"{os.getcwd()}/{github_api.get_user_id()}.csv", index=False)
			self.github_data_csv().to_csv(f"{os.getcwd()}/{github_api.get_user_id()}_follower_info.csv", index=False)
			self.bahadir_following_csv().to_csv(f"{os.getcwd()}/{github_api.get_user_id()}_following.csv", index=False)
			self.star().to_csv(f"{os.getcwd()}/{github_api.get_user_id()}_stargazers_info.csv", index=False)
			return os.listdir()
		else:
			Main_Menu().asil()

	def bahdir_csv(self) -> pd.DataFrame:
		bahadir_df = pd.DataFrame(columns=["id", "user_name"])
		bahadir_df = bahadir_df.append({
			"id": bahadir.id,
			"user_name": bahadir.login,
		}, ignore_index=True)
		return bahadir_df

	def github_data_csv(self) -> pd.DataFrame:
		# create new dataframe
		df2 = pd.DataFrame(columns=["id", "user_name"])
		for i in github_api.get_api_followers_info():
			df2 = df2.append({
				"id": i.id,
				"user_name": i.login,
			}, ignore_index=True)

		return df2

	def bahadir_following_csv(self) -> pd.DataFrame:
		df3 = pd.DataFrame(columns=["id", "user_name"])
		for i in github_api.get_following_info():
			df3 = df3.append({
				"id": i.id,
				"user_name": i.login,
			}, ignore_index=True)
		return df3

	def star(self) -> pd.DataFrame:
		df = pd.DataFrame(columns=["id", "user_name", "repo_name"])
		for i in github_api.get_api_star_info():
			for j in i.get_stargazers_with_dates():
				df = df.append({
					"id": j.user.id,
					"user_name": j.user.login,
					"repo_name": i.name
				}, ignore_index=True)
		return df

	def create_csv(self, df: pd.DataFrame, file_name: str):
		id = github_api.get_user_id()

		options = {"1": f"{id}_follower_info.csv", "2": f"{id}_stargazers_info.csv", "3": f"{id}_following.csv"}

		def path():
			return os.path.join(os.getcwd(), options.get(file_name))
		a = pd.read_csv(fr"{path()}")
		a = a.sort_values(by="id")
		df = df.fillna(0)
		df = df.sort_values(by="id")
		if df.equals(a):
			print("same")
		elif pd.concat([a, df]).drop_duplicates(keep=False).empty:
			print("same")
		else:
			df1 = pd.concat([a, df]).drop_duplicates(keep=False)
			print(df1)
			print("differencei")


functions = Functions()


# bahadir_csv_path = os.path.join(os.getcwd(), "bahadir.csv")
#
# github_data_csv_path = os.path.join(os.getcwd(), "github_data.csv")
#
# bahadir_following_csv_path = os.path.join(os.getcwd(), "following.csv")
#
# bahadir_star_info = os.path.join(os.getcwd(), "star_info.csv")
#
# create_csv(bahdir_csv(), bahadir_csv_path)
# create_csv(github_data_csv(), github_data_csv_path)
# create_csv(bahadir_following_csv(), bahadir_following_csv_path)
# create_csv(star(), bahadir_star_info)


class Main_Menu:
	try:

		def __init__(self):

			self.secenek = {
				"1": lambda :functions.create_csv(functions.github_data_csv(),"1"),
				"2": lambda :functions.create_csv(functions.star(),"2"),
				"3": lambda :functions.create_csv(functions.bahadir_following_csv(),"3"),
				"q": self.quit
			}

		def menu_goster(self):
			print("""
menu
1.followers
2.star
3.following
exit to q
    """)

		def asil(self):
			while True:
				self.menu_goster()
				secenek = input("sellect options: ")
				dogrulama = self.secenek.get(secenek)
				if dogrulama:
					dogrulama()
				else:
					print(rf"{secenek} wrong options")

		def quit(self):
			print("byyy")
			sys.exit(0)

	except FileNotFoundError:
		pass


if __name__ == "__main__":
	print("hello")
	functions.check_csv()

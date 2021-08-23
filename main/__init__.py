import os, sys
import github.GithubException
import pandas as pd
from dotenv import load_dotenv
from github import Github

pd.set_option("display.max_rows", None, "display.max_columns", None)


class github_api:

	def get_api_followers_info(self):
		try:
			github_api_info = Github(api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().get_followers()

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_api_star_info(self):
		try:
			github_api_info = Github(api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().get_repos(visibility="public")

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_user_info(self):
		try:
			github_api_info = Github(api_key)
			github_api_info.get_user().login
			return github_api_info.get_user()

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_following_info(self):
		try:
			github_api_info = Github(api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().get_following()

		except github.GithubException:
			raise "missing or incorrect API key"

	def get_user_id(self):
		try:
			github_api_info = Github(api_key)
			github_api_info.get_user().login
			return github_api_info.get_user().id

		except github.GithubException:
			raise "missing or incorrect API key"


github_api = github_api()


class Functions:

	def creates_csv(self):
		try:
			self.bahdir_csv().to_csv(f"{os.getcwd()}\\csvs\\{github_api.get_user_id()}.csv", index=False)
			self.github_data_csv().to_csv(f"{os.getcwd()}\\csvs\\{github_api.get_user_id()}_follower_info.csv",
										  index=False)
			self.bahadir_following_csv().to_csv(f"{os.getcwd()}\\csvs\\{github_api.get_user_id()}_following.csv",
												index=False)
			self.star().to_csv(f"{os.getcwd()}\\csvs\\{github_api.get_user_id()}_stargazers_info.csv", index=False)
		except FileNotFoundError:
			os.makedirs(f"{os.getcwd()}\\csvs")
			self.creates_csv()

	def check_csv(self):
		if os.path.isfile(fr"{os.getcwd()}/csv/{github_api.get_user_id()}.csv") == False:
			print("creating csv file..")
			self.creates_csv()
			Main_Menu().asil()
			return os.listdir()
		else:
			Main_Menu().asil()

	def bahdir_csv(self) -> pd.DataFrame:
		bahadir_df = pd.DataFrame(columns=["id", "user_name"])
		bahadir = github_api.get_user_info()
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

	def create_csv(self, df: pd.DataFrame, file_name: str) -> pd.DataFrame:
		id = github_api.get_user_id()

		options = {"1": f"{id}_follower_info.csv", "2": f"{id}_stargazers_info.csv", "3": f"{id}_following.csv"}

		def path():
			print(os.getcwd())
			return os.path.join(os.getcwd() + "\\csvs", options.get(file_name))

		a = pd.read_csv(fr"{path()}")
		a = a.sort_values(by="id")
		df = df.fillna(0)
		df = df.sort_values(by="id")
		if df.equals(a):
			print("no new followers")
		elif pd.concat([a, df]).drop_duplicates(keep=False).empty:
			print("no new followers")
		else:

			df1 = pd.concat([a, df]).drop_duplicates(keep=False)
			print(df1.loc[df1["id"].isin(df1["id"].drop_duplicates(keep=False)) == False]
				  .sort_values(by="id")
				  .to_string(index=False))

			print(df1, "difference", sep="\n")
			a = input("update data Y/N")
			if a.upper() == "Y":
				functions.creates_csv()
			elif a.upper() == "N":
				pass

	def most_star(self):
		df = pd.DataFrame(columns=["id", "user_name", "repo_name"])
		for i in github_api.get_api_star_info():
			for j in i.get_stargazers_with_dates():
				df = df.append({
					"id": j.user.id,
					"user_name": j.user.login,
					"repo_name": i.name
				}, ignore_index=True)

		return df.groupby("user_name").count()["id"].sort_values(ascending=False)

	def most_starred_repo(self):
		df = pd.DataFrame(columns=["id", "user_name", "repo_name"])
		for i in github_api.get_api_star_info():
			for j in i.get_stargazers_with_dates():
				df = df.append({
					"id": j.user.id,
					"user_name": j.user.login,
					"repo_name": i.name
				}, ignore_index=True)

		return df.groupby("repo_name").count()["id"].sort_values(ascending=False)


functions = Functions()


class Main_Menu:
	try:

		def __init__(self):
			self.secenek = {
				"1": lambda: functions.create_csv(functions.github_data_csv(), "1"),
				"2": lambda: functions.create_csv(functions.star(), "2"),
				"3": lambda: functions.create_csv(functions.bahadir_following_csv(), "3"),
				"4": lambda: print(functions.most_star()),
				"5": lambda: print(functions.most_starred_repo()),
				"q": self.quit
			}

		def menu_goster(self):
			print("""
menu
1.followers
2.star
3.following
4.who scored the most stars
5.most starred repo
exit to q
    """)

		def asil(self):
			while True:
				self.menu_goster()
				secenek = input("sellect options: ")
				dogrulama = self.secenek.get(secenek.lower())
				if dogrulama:
					dogrulama()
				else:
					print(rf"{secenek} wrong options")

		def quit(self):
			print("byyy")
			sys.exit(0)

	except FileNotFoundError:
		pass

	def main(self):
		try:
			if os.path.isfile(f"{os.getcwd()}/env/.env"):
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


main_menu = Main_Menu()

if __name__ == "__main__":
	main_menu.main()
	load_dotenv(dotenv_path="env/.env")
	api_key = os.environ['API_KEY']
	functions.check_csv()

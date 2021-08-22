import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from github import Github

pd.set_option("display.max_rows", None, "display.max_columns", None)
class github_api:
	def __init__(self):
		load_dotenv()
		self.api_key = os.environ["API_KEY"]
		self.sql_key = os.environ["SQL_KEY"]


	def get_api_followers_info(self):
		github_api_info = Github(self.api_key)
		return github_api_info.get_user().get_followers()

	def get_api_star_info(self):
		github_api_info = Github(self.api_key)
		github_api_info.get_user()
		return github_api_info.get_user().get_repos(visibility="public")

	def get_user_info(self):
		github_api_info = Github(self.api_key)
		return github_api_info.get_user()
	
	def get_following_info(self):
		github_api_info = Github(self.api_key)
		return github_api_info.get_user().get_following()

github_api = github_api()

def star():
	df = pd.DataFrame(columns=["id","user_name","repo_name"])
	for i in github_api.get_api_star_info():
		for j in i.get_stargazers_with_dates():
			df = df.append({
				"id":j.user.id,
				"user_name":j.user.login,
				"repo_name":i.name
				},ignore_index=True)
	#df = df.sort_values(by=["id"])
	#df.to_csv(f"{os.getcwd()}/star_info.csv",index=False)
	#print(df)
	##who scored how many stars
	#a= df.groupby("user_name").count()["user_id"].sort_values(ascending=False)
	##which repo has how many stars
	#b= df.groupby("repo_name").count()["user_id"].sort_values(ascending=False)
	#print(a)
	#print(b)
	return  df
bahadir = github_api.get_user_info()


def bahdir_csv():
	bahadir_df = pd.DataFrame(columns=["id","user_name"])
	bahadir_df = bahadir_df.append({
		"id":bahadir.id,
		"user_name":bahadir.login,
		},ignore_index=True)

	return bahadir_df




def github_data_csv():
#create new dataframe
	df2 = pd.DataFrame(columns=["id","user_name"])
	for i in github_api.get_api_followers_info():
		df2 = df2.append({
			"id":i.id,
			"user_name":i.login,
			},ignore_index=True)

	return df2

def bahadir_following_csv():
	df3 = pd.DataFrame(columns=["id","user_name"])
	for i in github_api.get_following_info():
		df3 = df3.append({
			"id":i.id,
			"user_name":i.login,
			},ignore_index=True)
	return df3
	


def create_csv(df,file_name):
	a=pd.read_csv(file_name)
	a=a.sort_values(by="id")
	df = df.fillna(0)
	df=df.sort_values(by="id")
	if df.equals(a):

		print("same")
	elif pd.concat([a,df]).drop_duplicates(keep=False).empty:
		print("same")
	else:
		df1 = pd.concat([a,df]).drop_duplicates(keep=False)
		print(df1)
		print("differencei")

bahadir_csv_path =os.path.join(os.getcwd(),"bahadir.csv")

github_data_csv_path =os.path.join(os.getcwd(),"github_data.csv")

bahadir_following_csv_path =os.path.join(os.getcwd(),"following.csv")

bahadir_star_info = os.path.join(os.getcwd(),"star_info.csv")


create_csv(bahdir_csv(),bahadir_csv_path)
create_csv(github_data_csv(),github_data_csv_path)
create_csv(bahadir_following_csv(),bahadir_following_csv_path)
create_csv(star(),bahadir_star_info)








#for i in github_api.get_api_followers_info():
#	print("_" * 50)
#	try:
#		print(i.id,
#			  i.following,
#			  i.email,
#			  i.location,
#			  i.followers,
#			  i.following,
#			  i.login,
#			  [x.strip() for x in i.company[1:].split('@')] if i.company.split('@')[0] == '' else i.company.split('@'),
#			  i.avatar_url,
#			  i.bio,
#			  i.name, sep="\n")
#	except Exception:
#		print(i.id,
#			  i.email,
#			  i.location,
#			  i.followers,
#			  i.following,
#			  i.login,
#			  i.company,
#			  i.avatar_url,
#			  i.bio,
#			  i.name, sep="\n")

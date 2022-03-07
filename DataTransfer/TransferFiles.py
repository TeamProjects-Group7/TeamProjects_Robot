#python 3.6
from github import Github
import json
f = open("Variables.json")
variables = json.load(f)

def uploadFile(filename):
    folder_prefix = "Data/"
    filePath = folder_prefix + filename
    with open(filePath, 'r') as file:
        content = file.read()
    repo.create_file(file, "creating test file", "", branch="main")

git_user = Github(variables["DATA_ACCESS"])
repo = git_user.get_user().get_repo("TeamProjectsIIData")
uploadFile("TestData.txt")
f.close()


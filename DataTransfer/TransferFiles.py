#python 3.6
from github import Github
import json
import os
f = open("Variables.json")
variables = json.load(f)

def uploadFile(filename, repo):
    repo_files = []
    repo_content = repo.get_contents("")
    while repo_content:
        file_content = repo_content.pop(0)
        if file_content.type == "dir":
            repo_content.extend(repo.get_contents(file_content.path))
        else:
            repo_files.append(str(file_content).replace('ContentFile(path="','').replace('")',''))
    folder_prefix = "Data/"
    filePath = folder_prefix + filename
    with open(filePath, 'r') as file:
        content = file.read()
    if filePath in repo_files:
        repo_contents = repo.get_contents(filePath)
        repo.update_file(repo_contents.path, "committing files", content, repo_contents.sha, branch="main")
    else:
        repo.create_file(filePath, "comitting files", content, branch="main")

git_user = Github("Ask Asher for the access code")
repo = git_user.get_user().get_repo("TeamProjectsIIData")
local_files = os.listdir("Data/")
for filename in local_files :
    uploadFile(filename, repo)
f.close()



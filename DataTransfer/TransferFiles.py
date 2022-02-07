#python 3.6
from github import Github
token = "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"
git_user = Github(token)
repo = git_user.get_user().get_repo("TeamProjectsIIData")
folder_prefix = "Data/"
test_file = folder_prefix + "TestData.txt"
contents = repo.get_contents("")
with open('Data/TestData.txt', 'r') as file:
    content = file.read()
repo.create_file(test_file, "creating test file", "test", branch="main")

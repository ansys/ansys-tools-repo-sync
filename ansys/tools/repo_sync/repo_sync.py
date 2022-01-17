import os

from github import Github

# use secret
PAT = os.environ('GH_PAT') 

org_name = 'pyansys'
repo_name = 'synchronization-demo'
branch_name = 'sync/sync_branch'

# should be using subprocess...
os.system(f'git clone https://{PAT}@github.com/{org_name}/{repo_name}')

os.chdir(repo_name)

# should be using subprocess...
try:
    os.system(f'git checkout -b {branch_name}')
except:
    os.system(f'git checkout {branch_name}')

# add a sample file
with open('testing.txt', 'w') as fid:
    fid.write('hello world')

# unsafe, should add specific file or directory
os.system('git add .')

# automate the messaging with something more descriptive
os.system('git commit -am "Add test file."')
os.system(f'git push -u origin {branch_name}')

# create pull request
gh = Github(PAT)
repo = gh.get_repo(f"{org_name}/{repo_name}")

body = """This is a test"""

pr = repo.create_pull(
    title="Demo for repo synchronization", body=body, head=branch_name, base="main"
)

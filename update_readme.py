import requests
from datetime import datetime
import os

username = "andre-melicio"
token = os.getenv("GITHUB_TOKEN")

def get_recent_projects(username, token):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Authorization": f"token {token}"
    }
    response = requests.get(url, headers=headers)
    repos = response.json()
    repos.sort(key=lambda x: datetime.strptime(x['updated_at'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)
    recent_repos = repos[:3]
    return recent_repos

def update_readme(recent_repos):
    with open("README.md", "r") as file:
        readme = file.read()

    projects_section = "## 🚀 Projetos Recentes\n"
    for repo in recent_repos:
        projects_section += f"\n### [{repo['name']}]({repo['html_url']})\n"
        projects_section += f"{repo['description']}\n"

    new_readme = readme.split("## 🚀 Projetos Recentes\n")[0] + projects_section + readme.split("## 🚀 Projetos Recentes\n")[1].split("\n###")[1]

    with open("README.md", "w") as file:
        file.write(new_readme)

if __name__ == "__main__":
    recent_repos = get_recent_projects(username, token)
    update_readme(recent_repos)

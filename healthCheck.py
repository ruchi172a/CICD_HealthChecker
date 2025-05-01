from tabulate import tabulate
from config import GITHUB_TOKEN
from dotenv import load_dotenv
import requests
import smtplib
from email.mime.text import MIMEText
import os

load_dotenv()

REPOS = [
    "ruchi172a/PracticeRepo2",
    "ruchi172a/testFirstRepo",
    "ruchi172a/NewRepoForAzure1"
]

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def check_latest_workflow(repo):
    url = f"https://api.github.com/repos/{repo}/actions/runs?per_page=1"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return [repo, "ERROR", res.status_code]
    data = res.json()
    if "workflow_runs" not in data or len(data["workflow_runs"]) == 0:
        return [repo, "No Runs", "-"]
    run = data["workflow_runs"][0]
    return [repo, run["status"], run["conclusion"]]

def send_email(content):
    sender = os.getenv("EMAIL_USER")
    recipient = os.getenv("EMAIL_TO")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEText(content)
    msg["Subject"] = "CI/CD Health Report"
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

def main():
    results = [check_latest_workflow(repo) for repo in REPOS]
    report = tabulate(results, headers=["Repository", "Status", "Conclusion"])
    print(report)
    send_email(report)

if __name__ == "__main__":
    main()

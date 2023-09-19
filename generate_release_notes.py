import json
import os
from datetime import datetime

import requests

username = os.getenv("CONFLUENCE_USERNAME")
token = os.getenv("CONFLUENCE_TOKEN")
page_url = os.getenv("RELEASE_NOTES_CONFLUENCE_URL")
page_title = os.getenv("RELEASE_NOTES_PAGE_TITLE")
page_space = os.getenv("RELEASE_NOTES_PAGE_SPACE")
page_id = page_url.split("/")[-1]

response = requests.get(f"{page_url}?expand=body.storage,version", auth=(username, token))
page_json = json.loads(response.content)
old_page_content = page_json['body']['storage']['value']
old_page_version = page_json['version']['number']
new_page_version = old_page_version + 1
release_date = str(datetime.utcnow().date())
version = None
commit_details = None

with open('VERSION', "r") as version_file:
    version = str(version_file.read())
with open('COMMITDETAILS', "r") as commit_file:
    commit_details = str(commit_file.read())

if (not version) or (not commit_details):
    version = release_date
    print("Automatic Release Notes failed, please add manually and review pipeline")
    exit(0)

commit_details = commit_details.split("\n")
commit_details_list = "<ul>"
for commit_detail in commit_details:
    commit_details_list += f"<li>{commit_detail}</li>"
commit_details_list += "</ul>"
commit_details = commit_details_list
new_content = f"""<p><strong>Version {version}</strong></p><span>Release Date: {release_date}</span>{commit_details}<hr/>{old_page_content}"""

payload = {
    "id": page_id,
    "type": "page",
    "title": page_title,
    "version": {"number": new_page_version},
    "space": {"key": page_space},
    "body": {
        "storage": {
            "value": new_content,
            "representation": "storage"
        }
    }
}
headers = {"Content-Type": "application/json", 
            "Accept": "application/json", 
            "User-Agent": "release-notes-pipeline"}

response = requests.put(url=page_url, data=json.dumps(payload), headers=headers, auth=(username, token))
if response.status_code == 200:
    print("Updated release notes successfully")
else:
    print("Unable to update release notes")

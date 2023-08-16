import json
from typing import Dict, Union

import requests

from snowmate_common.sender import AUTHORIZATION_HEADER

PROJECTS_ROUTE = "/baseline/api/projects"
TIMEOUT_SECONDS = 60
SETTINGS_KEY = "settings"
PROJECT_NOT_FOUND_MESSAGE = "Project not found"


def does_project_exist(access_token: str, api_url: str, project_id: str) -> bool:
    res = fetch_project(access_token, api_url, project_id)
    return res.json().get("detail") != PROJECT_NOT_FOUND_MESSAGE


def get_project_settings(
    access_token: str, api_url: str, project_id: str
) -> Union[bool, Dict]:
    res = fetch_project(access_token, api_url, project_id)
    if res.ok:
        project = res.json()
        project_settings = project.get(SETTINGS_KEY)
        try:
            return json.loads(project_settings)
        except (TypeError, json.JSONDecodeError):
            return {}
    return False


def fetch_project(access_token: str, api_url: str, project_id: str):
    return requests.get(
        f"{api_url}/{PROJECTS_ROUTE}/{project_id}",
        timeout=TIMEOUT_SECONDS,
        headers={AUTHORIZATION_HEADER: f"Bearer {access_token}"},
    )

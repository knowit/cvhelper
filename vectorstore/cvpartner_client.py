# Imports
import requests
import os
import json
from requests_ratelimiter import LimiterSession

from typing import Iterator, Sequence, Any


class CVPartnerClient:
    def __init__(self, token: str) -> None:
        self.token = token
        self.headers = {
            "content-type": "application/json",
            "Authorization": f"Token token={token}",
        }
        self.session = LimiterSession(per_second=5, per_minute=150)

    def get(self, *args, **kwargs) -> requests.Response:
        """Make a GET request using LimiterSession. Uses standard headers if not included."""
        if "headers" not in kwargs:
            kwargs["headers"] = self.headers
        return self.session.get(*args, **kwargs)

    def post(self, *args, **kwargs) -> requests.Response:
        """Make a POST request using LimiterSession. Uses standard headers if not included."""
        if "headers" not in kwargs:
            kwargs["headers"] = self.headers
        return self.session.post(*args, **kwargs)

    def search_email(self, email: str) -> dict[str, str]:
        """Get cv id and user id from email input."""
        url = f"https://knowit.cvpartner.com/api/v1/users/find"
        r = self.get(url=url, params={"email": email})
        cv_json = r.json()
        user_info = {
            "name": cv_json["name"],
            "cv_id": cv_json["default_cv_id"],
            "user_id": cv_json["user_id"],
        }
        return user_info

    def get_cv_by_id(self, user_id: str, cv_id: str):
        """Get a CV given user_id and cv_id"""
        url = f"https://knowit.cvpartner.com/api/v3/cvs/{user_id}/{cv_id}"
        r = self.get(url)
        cv_json = r.json()
        return cv_json

    def get_cv_by_email(self, email: str):
        """Get a CV given an email."""
        user_info = self.search_email(email)
        user_id = user_info["user_id"]
        cv_id = user_info["cv_id"]
        return self.get_cv_by_id(user_id, cv_id)

    def get_cvs(self, emails: Sequence[str]) -> list[Any]:
        """Return a list of CVs given a sequence of emails"""
        return [self.get_cv_by_email(email) for email in emails]

    def iterate_users(self) -> Iterator[Any]:
        """Iterate over all active users."""
        url = "https://knowit.cvpartner.com/api/v1/users"
        offset = 0
        while True:
            r = self.get(url=url, params={"offset": offset})
            data = r.json()
            if len(data) == 0:
                break
            offset += len(data)
            for user in data:
                if user["deactivated"]:
                    continue
                yield user

    def search_cvs(self, **kwargs) -> Any:
        url = "https://knowit.cvpartner.com/api/v2/cvs/search"
        request_body = json.dumps(kwargs)
        offset = 0
        while True:
            r = self.post(url=url, params={"offset": offset}, data=request_body)
            cvs = r.json()["cvs"]
            if len(cvs) == 0:
                break
            offset += len(cvs)
            for item in cvs:
                yield item["cv"]

    def download_cv(self, user_id: str, cv_id: str, download_path: str) -> None:
        """Downlad a CV given user_id and cv_id."""
        assert os.path.exists(download_path)

        url = f"https://knowit.cvpartner.com/api/v3/cvs/{user_id}/{cv_id}"
        r = self.get(url)
        file_name = f"{user_id}.json"
        with open(os.path.join(download_path, file_name), "w") as f:
            f.write(r.text)

    def download_search_cvs(self, download_path: str, **kwargs) -> None:
        """Download a all CVs from a search result."""
        assert os.path.exists(download_path)

        for cv in self.search_cvs(**kwargs):
            user_id = cv["user_id"]
            cv_id = cv["id"]
            self.download_cv(user_id, cv_id, download_path)

    def download_all_cvs(
        self,
        download_path: str,
    ) -> None:
        """Download a all active CVs from cvpartner."""
        assert os.path.exists(download_path)

        for user in self.iterate_users():
            user_id = user["user_id"]
            cv_id = user["default_cv_id"]
            self.download_cv(user_id, cv_id, download_path)

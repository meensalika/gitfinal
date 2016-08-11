import requests
import json

from django.shortcuts import render
from django.conf import settings

from requests.exceptions import HTTPError
from gitapp.models import GITCommits, GITComments


class GitAPIServices():
    """
    """
    def get_comments(self, repository_name):
        """
        Description:
            Function to fetch comments from git. It calls the git api
            to fetch comments of a particular user in a repository
        Args:
            repository_name: name of user
            username: github username
        Returns:
            response_data: {}
        """
        try:
            response = {"error": ""}
            url = settings.GIT_HOST + 'repos/' + 'devendraratnam747' + "/" + repository_name + "/comments"
            response = requests.get(url)
            response.raise_for_status()
            response_data = response.json()
        except HTTPError as e:
            response.update({"error": str(e)})
        return response_data

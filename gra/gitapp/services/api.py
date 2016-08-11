import requests
import json


class APICall():

    """
    Description:

    """
    def api_for_each_commit(self, commit_id):
        """
        Description:
            this method getting github commit if of a user's commit in
            perticular repository example (DelhiProject)
            and calling github's commit api and returning all
            information related to that commit like : commitor github username,
            commit date etc
        Args:
            commit_id : github commit id
        """
        commit_response = requests.get('https://api.github.com/repos/'
                                       'devendraratnam747/DelhiProject/'
                                       'commits/%s' % (commit_id))
        return commit_response

    def api_for_all_repository(self, organization_name):
        """
        Description :
            This method calling github's api to listdown all repository
            of a organization and returning list of all repository
        args:
            organization_name : name of organiation example: Delhivery
        """
        response = requests.get('https://api.github.com/'
                                'orgs/delhivery/repos').json()
        repos_list = []
        for each in response:
            repos_list.push(each.get('full_name'))
        return repos_list

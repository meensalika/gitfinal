import json
import requests
import re
from datetime import datetime
from gitapp.models import GITComments, GITCommits
from django.contrib.auth.models import User


def create_commit(commit_info, repository_name):
    """
    Description:
        this function taking commit_info json data as
        argument and creating objet of the gitcommt class
    Args:
        commit_info: dictionary containing information of a commit
    """
    user, u_created = User.objects.get_or_create(username=commit_info.get(
                                                 'committer').get('login'))
    commit_obj, created = GITCommits.objects.get_or_create(
        commit_id=commit_info.get('sha'),
        defaults={
            'repository': repository_name,
            'commit_message': commit_info.get('commit').get('message'),
            'committed_by': user,
            'created_at': datetime.strptime(commit_info.get('commit').get('author').get('date').split('T')[0], '%Y-%m-%d')})
    return commit_obj


def create_comment(comment_info, user_obj, commit_obj, repository_name):
    """
    Description:
        this function taking comment_info json data
        as argument and creating objet of the gitcommt class
    Args:
        comment_info:dictionary containing information of comment
    """
    user_obj, created = User.objects.get_or_create(
        username=comment_info['user']['login'])

    try:
        rating = re.findall(r'Rating@\d{1}',
                            comment_info.get('body'), re.IGNORECASE)[0][-1]
    except:
        rating = 'NA'

    comment_obj, created = GITComments.objects.get_or_create(
        git_comment_id=comment_info.get('id'),
        defaults={'repository': repository_name,
                  'comment_message': comment_info.get('body'),
                  'comment_url': comment_info.get('html_url'),
                  'commented_by': user_obj,
                  'rating': rating,
                  'commit': commit_obj,
                  'created_at': datetime.strptime(comment_info.get(
                               'created_at').split('T')[0], '%Y-%m-%d')})
    return comment_obj

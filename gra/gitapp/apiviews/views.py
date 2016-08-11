import requests
import json
import logging

from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    )

from rest_framework import exceptions
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from django.http import Http404
from django.conf import settings
from rest_framework import generics
from rest_framework import filters
from pagination import CommentLimitOffsetPagination

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView


from gitapp.services.gitapi import *
from gitapp.models import GITComments, GITCommits
from gitapp.services.api import APICall
from gitapp.serializers import GITCommentsSerializer, GITCommitsSerializer
from gitapp.apiviews.utils import create_commit, create_comment


class GITApiCall(ViewSet):
    """
    Description :
        Service api
        Api request method :GET
    """
    def fetch_git_comments(self, *args, **kwargs):
        """
        Description:
            Method to fetch all comments or reviews from github of a specified repository
        args:
        """
        comments_list = []
        repository_name = settings.REPOSITORY
        comment_response = GitAPIServices().get_comments(repository_name)
        for each in comment_response:
            comments = GITComments.objects.filter(
                git_comment_id=each.get('id'))
            if not comments:
                commit_response = APICall().api_for_each_commit(
                    each.get('commit_id')).json()
                commit_obj = create_commit(commit_response, repository_name)
                create_comment(each, commit_obj, commit_obj, repository_name)
        return Response({"success": True})


class CommentForUser(generics.ListAPIView):
    """
    Description:
        Enter user name and get list of comment of the users
    args:
        username: github username,from_date ,to_date,repository:user
    """
    serializer_class = GITCommentsSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filter_fields = ['comment_message', 'rating']
    pagination_class = CommentLimitOffsetPagination

    def get_queryset(self):
        username = self.kwargs.get('username')
        filter_dict = {'commit__committed_by__username': username}
        if username is not None:
            if self.request.query_params.get('from_date'):
                filter_dict.update({'created_at__gte': self.request.query_params.get(
                                   'from_date')})
            if self.request.query_params.get('to_date'):
                filter_dict.update({'created_at__lte':
                                    self.request.query_params.get('to_date')})
            if self.request.query_params.get('repository'):
                filter_dict.update({'repository':
                                    self.request.query_params.get('repository')})
            try:
                user = User.objects.get(username=username)
                queryset = GITComments.objects.filter(**filter_dict)
                if not queryset:
                    raise exceptions.NotFound(detail="Comment Not Found for user {}".format(username))

            except User.DoesNotExist:
                    raise exceptions.NotFound(detail="Comments Not Found for user {}".format(username))
        return queryset


class RepositoryForUser(APIView):
    """
    Descrition:
        api to listdown all repositories in which user committed
    args:
        username : github username
        args:
        kwargs:
    """

    def get(self, request, username, *args, **kwargs):
        repo_list = []
        try:
            User.objects.get(username=username)
            repository_list = GITCommits.objects.filter(committed_by__username=username).values('repository').annotate(n=models.Count("pk"))
            status_code = status.HTTP_200_OK
            for each in repository_list:
                repo_list.append(each.get('repository'))
            response = {'Repository': repo_list,
                        'Success': True,
                        'Error': False,
                        'message': 'repositories in which user commited'}
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {'Repository': '[]',
                        'Success': False,
                        'Error': True,
                        'message': 'Invalid user {} entered or repository not found'.format(username)}

        return Response(response, status_code)

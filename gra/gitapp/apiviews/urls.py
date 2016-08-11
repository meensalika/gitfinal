from django.conf.urls import patterns, url

from gitapp.apiviews.views import GITApiCall
from gitapp.apiviews.views import CommentForUser, RepositoryForUser

urlpatterns = patterns(
    '',
    url(r'^get_comments/$', GITApiCall.as_view({'get': 'fetch_git_comments'})),
    url(r'^get_user_comment/(?P<username>[a-zA-Z0-9_.-]+)/$',
        CommentForUser.as_view(), name='get_comment_list'),
    url(r'^get_user_repository/(?P<username>[a-zA-Z0-9_.-]+)/$',
        RepositoryForUser.as_view(), name='get_comment_list'),)

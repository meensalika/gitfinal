from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.contrib.auth.models import User
from gitapp.models import GITComments, GITCommits


class UserSerializer(serializers.ModelSerializer):
    """
    Description:
        serializer for User model
    """
    class Meta:
        model = User
        fields = ('username', )


class GITCommitsSerializer(serializers.ModelSerializer):
    """
    Descrition:
        serializer for GITCommits model
    """
    committed_by = UserSerializer(read_only=True)

    class Meta:
        model = GITCommits
        fields = ('commit_id', 'committed_by')


class GITCommentsSerializer(serializers.ModelSerializer):
    """
    Descrition:
        Serializer for GITComments model
    """
    commented_by = UserSerializer(read_only=True)
    commit = GITCommitsSerializer(read_only=True)

    class Meta:
        model = GITComments
        fields = ('git_comment_id', 'comment_message', 'comment_url',
                  'repository', 'rating', 'commented_by', 'commit')

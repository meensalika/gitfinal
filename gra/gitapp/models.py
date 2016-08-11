from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class GITCommits(models.Model):
    """
    Description:
        This class is for user's commit in github's repository
    """
    commit_id = models.CharField(max_length=500)
    created_at = models.DateTimeField()
    committed_by = models.ForeignKey(User,
                                     max_length=500, blank=True, null=True)
    commit_message = models.CharField(max_length=500)
    repository = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.commit_message


class GITComments(models.Model):
    """
    Description:
        This class is for comments or reviews of  github's reposities
    """
    git_comment_id = models.IntegerField()
    comment_message = models.CharField(max_length=500)
    comment_url = models.CharField(max_length=500)
    commented_by = models.ForeignKey(User,
                                     max_length=500, null=True, blank=True)
    commit = models.ForeignKey('GITCommits',
                                max_length=500, null=True, blank=True)
    repository = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField()
    rating = models.CharField(max_length=30)

    def __str__(self):
        return self.comment_message

from django.db import models


class A(models.Model):
    name = models.TextField()


class B(models.Model):
    name = models.TextField()
    a = models.ForeignKey(to=A, related_name='bs', on_delete=models.CASCADE)
    limit = models.TextField(null=True)

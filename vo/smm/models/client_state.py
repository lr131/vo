from django.db import models


class State(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'client_state'

    def __str__(self):
        return self.name
import uuid

from djongo import models


class Weather(models.Model):

    class Meta:
        db_table = 'weather'

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    at = models.DateTimeField(db_index=True, unique=True)

    document = models.JSONField()

    def __str__(self):
        return f'Weather[{self.uuid}] at:{self.at}'

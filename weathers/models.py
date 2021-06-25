import uuid

from djongo import models


class Main(models.Model):
    temp = models.FloatField()
    feels_like = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    pressure = models.IntegerField()
    humidity = models.IntegerField()

    class Meta:
        abstract = True


class Weather(models.Model):

    class Meta:
        db_table = 'weather'

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.IntegerField()
    at = models.DateTimeField(db_index=True, unique=True)
    name = models.CharField(max_length=255)
    main = models.EmbeddedField(
        model_container=Main
    )

    def __str__(self):
        return f'{self.name} at {self.at}'

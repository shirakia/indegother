import uuid

from djongo import models


class Station(models.Model):

    class Meta:
        db_table = 'station'
        constraints = [
            models.UniqueConstraint(
                fields=['kioskId', 'at'],
                name='kioskId_at_unique'
            ),
        ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kioskId = models.IntegerField(null=False, db_index=True)
    at = models.DateTimeField(db_index=True)
    document = models.JSONField()

    def __str__(self):
        return f'{self.kioskId} at {self.at}'

from django.db import models

class TankLevel(models.Model):
    tank = models.CharField(max_length=100)
    level = models.FloatField()
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.tank} - {self.level} at {self.time}"

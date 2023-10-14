from django.db import models
class Predict(models.Model):
    prediction_image=models.ImageField(upload_to='images/')
    def __str__(self):
        return str(self.prediction_image)
from django.db import models

# Create your models here.

class DataToAnalyze(models.Model):
    user = models.IntegerField(verbose_name="L'utilisateur ayant uploadé ce fichier")
    dataset = models.FileField(upload_to="data/", verbose_name="Fichier contenant les données")

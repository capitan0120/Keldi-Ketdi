from django.db import models

class Xodimlar(models.Model):
    ismi = models.CharField(max_length=512)
    familiyasi = models.CharField(max_length=512)
    kasbi = models.CharField(max_length=512)
    img = models.ImageField(null=True, blank=True, upload_to='rasmlar/')
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.ismi} {self.familiyasi}'

    class Meta:
        verbose_name_plural = 'Xodimlar'

class KeldiKetdi(models.Model):
    xodim = models.ForeignKey(Xodimlar, on_delete=models.CASCADE)
    kelish_vaqti = models.DateTimeField(null=True, blank=True)
    ketish_vaqti = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.xodim.ismi} {self.xodim.familiyasi}'

    class Meta:
        verbose_name_plural = "KeldiKetdi"

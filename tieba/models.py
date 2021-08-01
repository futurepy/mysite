from django.db import models

# Create your models here.

class subscription(models.Model):
    baming = models.TextField()
    guanzhuliang = models.TextField()
    fatieshu = models.TextField()
    class Meta:
        db_table = "tieba_infor"
    def __str__(self):
        return self.baming
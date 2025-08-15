from django.db import models


# Create your models here.
class Short(models.Model):
    url = models.URLField()
    shortCode = models.CharField(max_length=16, unique=True)
    accessCount = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def list_resource(self):
        return {
            "id": self.id,
            "url": self.url,
            "shortCode": self.shortCode,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }

    def detail_resource(self):
        resource = self.list_resource()
        resource["accessCount"] = self.accessCount
        return resource

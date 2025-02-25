from django.db import models

#  We're not using database models for this simple example, but it's good
#  practice to have the file.  If you needed to store data persistently
#  (e.g., in a database), you would define your models here.

# Example (if you *did* want to store data):
# class WebPage(models.Model):
#     url = models.URLField()
#     content = models.TextField()
#     last_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.url
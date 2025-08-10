from django.db import models

# Create your models here.

class QueryLog(models.Model):
    case_type = models.CharField(max_length=50)
    case_number = models.CharField(max_length=50)
    filing_year = models.IntegerField()
    query_time = models.DateTimeField(auto_now_add=True)
    raw_response = models.TextField()

    # New fields to align with updated scraping logic
    # case_status = models.CharField(max_length=100, null=True, blank=True)
    # petitioner = models.CharField(max_length=255, null=True, blank=True)
    # respondent = models.CharField(max_length=255, null=True, blank=True)
    # last_hearing = models.DateField(null=True, blank=True)
    # next_hearing = models.DateField(null=True, blank=True)
    # court_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.case_type} {self.case_number}/{self.filing_year}"

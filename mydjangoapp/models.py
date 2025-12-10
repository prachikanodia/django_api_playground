from django.db import models


# Create your models here.
class form(models.Model):
    first_name=models.CharField(max_length=180)
    last_name=models.CharField(max_length=200)
    email_id=models.CharField(max_length=200)
    phone_no=models.IntegerField()
    message=models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=["email_id"])
        ]

class McqSubmission(models.Model):
    _id = models.ObjectIdField()
    questionId = models.CharField(max_length=50, blank=True, null=True)
    userId = models.CharField(max_length=50, blank=True, null=True)
    newsepickId = models.CharField(max_length=50, blank=True, null=True)
    instituteId = models.CharField(max_length=50, blank=True, null=True)
    facultyId = models.CharField(max_length=50, blank=True, null=True)
    correctAnswer = models.IntegerField(default=0)
    userSelectedAnswer = models.IntegerField(default=0)
    className = models.CharField(max_length=50, blank=True, null=True)
    subjectName = models.CharField(max_length=50, blank=True, null=True)
    topicName = models.CharField(max_length=50, blank=True, null=True)
    questionInstituteRefId = models.CharField(max_length=50, blank=True, null=True)
    questionLevel = models.CharField(max_length=50, blank=True, null=True)
    createTime = models.DateTimeField(blank=True,null=True)
    class Meta:
        db_table = "mcq_submission"
        indexes = [
            models.Index(fields=['questionId'],name='idx_mcq_questionId'),
            models.Index(fields=['userId'],name='idx_mcq_userId'),
            models.Index(fields=['newsepickId'],name='idx_mcq_newsepickId'),
            models.Index(fields=['instituteId'],name='idx_mcq_instituteId'),
            models.Index(fields=['facultyId'],name='idx_mcq_facultyId'),
            models.Index(fields=['className'],name='idx_mcq_className'),
            models.Index(fields=['subjectName'],name='idx_mcq_subjectName'),
            models.Index(fields=['topicName'],name='idx_mcq_topicName'),
            models.Index(fields=['questionInstituteRefId'],name='idx_mcq_questionInstituteRefId'),
            models.Index(fields=['questionLevel'],name='idx_mcq_questionLevel'),
            models.Index(fields=['createTime'],name='idx_mcq_createTime')  
        ]

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Course(models.Model):
    code = models.CharField(max_length=20, db_index=True)  # e.g., CP216
    title = models.CharField(max_length=120, blank=True)

    class Meta:
        unique_together = ('code', 'title')
        ordering = ['code']

    def __str__(self):
        return f"{self.code}{' — ' + self.title if self.title else ''}"

class Topic(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class StudyGroup(models.Model):
    title = models.CharField(max_length=120)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.CharField(max_length=50, help_text='e.g., Peters 2015')
    meeting_time = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    topics = models.ManyToManyField(Topic, blank=True, related_name='groups')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Membership(models.Model):
    OWNER = 'OWNER'
    MEMBER = 'MEMBER'
    ROLE_CHOICES = [(OWNER, 'Owner'), (MEMBER, 'Member')]

    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    STATUS_CHOICES = [(PENDING, 'Pending'), (APPROVED, 'Approved'), (REJECTED, 'Rejected')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user} → {self.group} ({self.status})"

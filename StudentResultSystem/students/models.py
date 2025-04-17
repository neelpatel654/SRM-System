from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    profile_image = models.ImageField(
        upload_to="profile_images/", blank=True, null=True
    )
    enrollment_number = models.CharField(max_length=15, unique=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Call the parent save method first to ensure student_id is assigned
        super().save(*args, **kwargs)

        if not self.enrollment_number:
            current_year = timezone.now().year
            # After saving the object, we now have the student_id
            self.enrollment_number = f"{current_year}{str(self.student_id).zfill(4)}"
            # Save again to update the enrollment_number field
            self.save()

    def calculate_gpa(self):
        total_marks = sum(result.marks for result in self.results.all())  # type: ignore
        total_subjects = self.results.count()  # type: ignore
        if total_subjects == 0:
            return 0
        percentage = (total_marks / (total_subjects * 100)) * 100
        return percentage

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Result(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="results"
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ("student", "subject")

    def __str__(self):
        return f"{self.student.name} - {self.subject}"

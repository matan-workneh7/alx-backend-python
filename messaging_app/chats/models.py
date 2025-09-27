import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Replace id with UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Extra fields from the spec
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=[('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')],
        default='guest'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

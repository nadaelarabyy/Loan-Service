import os
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django
import django
django.setup()

from api.models import CustomUser  # Adjust the import based on your structure
print(CustomUser.objects.all())


# Check if there's an exact match
email = "n@mail.com"  # The email you're searching for
try:
    # Compare emails in a loop for debugging
    for user in CustomUser.objects.all():
        if user.email == email:
            print(f"Exact Match Found for Email: {user.email}")
        else:
            print(f"Email '{email}' does not match Stored Email '{user.email}'")

    # Try to fetch directly using .get()
    user = CustomUser.objects.get(email=email)
    print("User Found via .get()!")
    print(f"Username: {user.username}, Email: {user.email}")
except CustomUser.DoesNotExist:
    print(f"No user found with email: {email}")
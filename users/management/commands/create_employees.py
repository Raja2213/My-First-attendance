from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from users.profiles import Profile

class Command(BaseCommand):
    help = 'Creates employees with a default password and adds them to a group.'

    def handle(self, *args, **options):
        # === YOUR LIST OF USER IDS ===
        user_ids = [
            "247916",
            "239103",
            "250685",
            "284263",
            "251937",
            "290989",
        ]
        # ============================

        group_name = "UST-Nokia"  # Change this to your group name
        default_password = "Password123"

        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Group '{group_name}' does not exist. Please create it first in the Django Admin."))
            return

        self.stdout.write(self.style.SUCCESS(f"Starting to create {len(user_ids)} users..."))

        for username in user_ids:
            user, created = User.objects.get_or_create(username=username)

            if created:
                user.set_password(default_password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"  Created user: {username}"))
            else:
                self.stdout.write(self.style.WARNING(f"  User already exists: {username}"))

            user.groups.add(group)
            if hasattr(user, 'profile'):
                user.profile.must_change_password = True
                user.profile.save()

        self.stdout.write(self.style.SUCCESS("\nProcess completed successfully."))
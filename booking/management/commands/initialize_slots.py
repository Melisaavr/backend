from django.core.management.base import BaseCommand
from booking.models import Slot
from datetime import time


class Command(BaseCommand):
    help = 'Initialize slots for the week'

    def handle(self, *args, **options):
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        start_times = [time(hour=h) for h in range(17, 23)]  # 5 PM to 10 PM

        for day in days:
            for start_time in start_times:
                end_time = time(hour=(start_time.hour + 1) % 24)
                Slot.objects.get_or_create(
                    day=day,
                    start_time=start_time,
                    end_time=end_time
                )

        self.stdout.write(self.style.SUCCESS('Successfully initialized slots'))

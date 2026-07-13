from django.core.management.base import BaseCommand
from admin_dashboard.models import RolePermission, DASHBOARD_PERMISSIONS


class Command(BaseCommand):
    help = 'Populate dashboard permissions in the database'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0
        
        for code, name in DASHBOARD_PERMISSIONS:
            permission, created = RolePermission.objects.get_or_create(
                code=code,
                defaults={'name': name}
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created permission: {code} - {name}'))
            else:
                # Update name if it changed
                if permission.name != name:
                    permission.name = name
                    permission.save()
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f'Updated permission: {code} - {name}'))
                else:
                    self.stdout.write(f'Permission already exists: {code} - {name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary: {created_count} created, {updated_count} updated, '
                f'{len(DASHBOARD_PERMISSIONS)} total permissions'
            )
        )

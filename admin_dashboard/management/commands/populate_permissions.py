from django.core.management.base import BaseCommand
from admin_dashboard.models import RolePermission, DASHBOARD_PERMISSIONS


class Command(BaseCommand):
    help = 'Populate dashboard permissions in the database'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0
        
        for code, name, category in DASHBOARD_PERMISSIONS:
            permission, created = RolePermission.objects.get_or_create(
                code=code,
                defaults={'name': name, 'category': category}
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created permission: {code} - {name} ({category})'))
            else:
                # Update name and category if they changed
                needs_update = False
                if permission.name != name:
                    permission.name = name
                    needs_update = True
                if permission.category != category:
                    permission.category = category
                    needs_update = True
                
                if needs_update:
                    permission.save()
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f'Updated permission: {code} - {name} ({category})'))
                else:
                    self.stdout.write(f'Permission already exists: {code} - {name} ({category})')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary: {created_count} created, {updated_count} updated, '
                f'{len(DASHBOARD_PERMISSIONS)} total permissions'
            )
        )

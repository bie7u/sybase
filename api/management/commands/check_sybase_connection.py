"""
Management command to check Sybase database connection.
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Check Sybase database connection'

    def handle(self, *args, **options):
        """Execute the command."""
        self.stdout.write('Checking Sybase database connection...')
        
        try:
            with connection.cursor() as cursor:
                # Try to execute a simple query
                cursor.execute("SELECT @@version")
                version = cursor.fetchone()
                
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Connection successful!')
                )
                
                if version:
                    self.stdout.write(f'Database version: {version[0]}')
                
                # Get current database name
                cursor.execute("SELECT db_name()")
                db_name = cursor.fetchone()
                if db_name:
                    self.stdout.write(f'Connected to database: {db_name[0]}')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Connection failed: {str(e)}')
            )
            self.stdout.write(
                self.style.WARNING('\nPlease check:')
            )
            self.stdout.write('  1. Sybase server is running')
            self.stdout.write('  2. Database credentials in .env are correct')
            self.stdout.write('  3. Network connection is available')
            self.stdout.write('  4. FreeTDS is properly configured')

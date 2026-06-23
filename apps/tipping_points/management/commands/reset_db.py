"""
python manage.py reset_db

A safe, reusable command for development that:
  1. Drops all app-level tables (tipping_points, claims, simulator, metrics)
  2. Clears those apps from Django's migration history
  3. Re-runs all migrations from scratch
  4. Leaves Django's own tables (auth, admin, sessions, contenttypes) untouched

Use this any time you:
  - Change model fields
  - Update seed data
  - Add or remove migrations
  - Hit migration conflicts

Usage:
  python manage.py reset_db           # prompts for confirmation
  python manage.py reset_db --yes     # skips prompt (use in scripts)
"""

import sys
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection


# All app-level tables to drop, in dependency-safe order
# (child tables before parent tables)
TABLES_TO_DROP = [
    # simulator (references tipping_points)
    'simulator_activatednode',
    'simulator_simulationrun',
    'simulator_simulationscenario',

    # claims (references tipping_points)
    'claims_claimtechniquelink',
    'claims_climateclaim_related_tipping_points',
    'claims_evidencesentence',
    'claims_climateclaim',
    'claims_claimtopic',
    'claims_misinformationtechnique',

    # tipping_points
    'tipping_points_sourcereference',
    'tipping_points_tippingpointrelationship',
    'tipping_points_tippingpoint',

    # metrics (standalone)
    'metrics_metricdatapoint',
    'metrics_climatemetric',
    'metrics_statisticcard',
]

# Apps whose migration history to clear
APPS_TO_RESET = [
    'tipping_points',
    'claims',
    'simulator',
    'metrics',
]


class Command(BaseCommand):
    help = 'Reset app database tables and re-run all migrations from scratch.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--yes',
            action='store_true',
            help='Skip confirmation prompt.',
        )

    def handle(self, *args, **options):
        if not options['yes']:
            self.stdout.write(self.style.WARNING(
                '\nThis will drop and recreate all app tables:\n'
                '  tipping_points, claims, simulator, metrics\n\n'
                'Django system tables (auth, admin, sessions) will NOT be touched.\n'
                'Your superuser account will be preserved.\n'
            ))
            confirm = input('Type "yes" to continue: ').strip().lower()
            if confirm != 'yes':
                self.stdout.write('Cancelled.')
                return

        self.stdout.write('\n--- Step 1: Dropping app tables ---')
        self._drop_tables()

        self.stdout.write('\n--- Step 2: Clearing migration history ---')
        self._clear_migration_history()

        self.stdout.write('\n--- Step 3: Re-running all migrations ---')
        call_command('migrate', verbosity=1)

        self.stdout.write(self.style.SUCCESS(
            '\nDone. All app tables recreated and seeded.\n'
        ))

    def _drop_tables(self):
        existing = self._get_existing_tables()
        with connection.cursor() as cursor:
            # Disable FK checks for the drop operation
            if connection.vendor == 'sqlite':
                cursor.execute('PRAGMA foreign_keys = OFF')
            elif connection.vendor == 'postgresql':
                cursor.execute('SET session_replication_role = replica')

            for table in TABLES_TO_DROP:
                if table in existing:
                    cursor.execute(f'DROP TABLE IF EXISTS "{table}"')
                    self.stdout.write(f'  Dropped: {table}')
                else:
                    self.stdout.write(f'  Skipped (not found): {table}')

            # Re-enable FK checks
            if connection.vendor == 'sqlite':
                cursor.execute('PRAGMA foreign_keys = ON')
            elif connection.vendor == 'postgresql':
                cursor.execute('SET session_replication_role = DEFAULT')

    def _get_existing_tables(self):
        with connection.cursor() as cursor:
            return set(connection.introspection.table_names(cursor))

    def _clear_migration_history(self):
        with connection.cursor() as cursor:
            for app in APPS_TO_RESET:
                cursor.execute(
                    "DELETE FROM django_migrations WHERE app = %s",
                    [app],
                )
                self.stdout.write(f'  Cleared migration history: {app}')

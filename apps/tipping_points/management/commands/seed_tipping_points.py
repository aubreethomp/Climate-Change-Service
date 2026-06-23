"""
python manage.py seed_tipping_points

Loads tipping_point_seed_data.csv into the TippingPoint table.
Also normalises source_urls into SourceReference rows and seeds
the hand-coded TippingPointRelationship edges.

Run this once after migrations:
    python manage.py migrate
    python manage.py seed_tipping_points
"""

import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.tipping_points.models import (
    TippingPoint,
    TippingPointRelationship,
    SourceReference,
)


# Hrelationship edges
RELATIONSHIPS = [
    # source_slug                       target_slug                      type                          strength  bidirectional
    ('gis_collapse',                    'amoc_collapse',                 'freshwater_circulation',     4,        False),
    ('wais_collapse',                   'gis_collapse',                  'sea_level',                  3,        False),
    ('gis_collapse',                    'wais_collapse',                 'sea_level',                  3,        False),
    ('abrupt_permafrost_thaw',          'gis_collapse',                  'temperature_amplification',  4,        False),
    ('permafrost_yedoma_carbon',        'abrupt_permafrost_thaw',        'carbon_feedback',            5,        False),
    ('abrupt_permafrost_thaw',          'permafrost_yedoma_carbon',      'carbon_feedback',            4,        True),
    ('amazon_rainforest_dieback',       'west_african_monsoon_shift',    'rainfall_recycling',         3,        False),
    ('amazon_rainforest_dieback',       'fisheries_collapse',            'ecosystem_cascade',          3,        False),
    ('warm_water_coral_reefs_dieoff',   'fisheries_collapse',            'habitat_livelihood',         5,        False),
    ('warm_water_coral_reefs_dieoff',   'mangrove_seagrass_dieoff',      'ocean_chemistry',            3,        False),
    ('mangrove_seagrass_dieoff',        'fisheries_collapse',            'habitat_livelihood',         4,        False),
    ('amoc_collapse',                   'west_african_monsoon_shift',    'monsoon_shift',              3,        False),
    ('amoc_collapse',                   'amazon_rainforest_dieback',     'rainfall_recycling',         3,        False),
    ('barents_sea_ice_loss',            'boreal_forest_northern_expansion', 'temperature_amplification', 3,     False),
    ('boreal_forest_southern_dieback',  'amazon_rainforest_dieback',     'carbon_feedback',            2,        False),
    ('mountain_glacier_loss',           'lake_eutrophication',           'ecosystem_cascade',          3,        False),
    ('lake_eutrophication',             'fisheries_collapse',            'ecosystem_cascade',          4,        False),
    ('southern_ocean_overturning',      'amoc_collapse',                 'ocean_chemistry',            3,        False),
    ('labrador_irminger_convection',    'amoc_collapse',                 'freshwater_circulation',     4,        False),
    ('gis_collapse',                    'labrador_irminger_convection',  'freshwater_circulation',     3,        False),
    ('sahel_greening',                  'west_african_monsoon_shift',    'monsoon_shift',              3,        True),
    ('east_antarctic_subglacial_basins','wais_collapse',                 'sea_level',                  2,        False),
]


# Domain slug mapping
DOMAIN_MAP = {
    'cryosphere':                    'cryosphere',
    'biosphere':                     'biosphere',
    'ocean-atmosphere circulation':  'ocean_atmosphere_circulation',
    'cryosphere / carbon cycle':     'cryosphere_carbon_cycle',
    'biosphere / ocean':             'biosphere_ocean',
    'cryosphere / ocean':            'cryosphere_ocean',
    'cryosphere / water systems':    'cryosphere_water',
    'atmosphere / hydrology':        'atmosphere_hydrology',
    'biosphere / hydrology':         'biosphere_hydrology',
    'biosphere / freshwater':        'biosphere_freshwater',
    'biosphere / food systems':      'biosphere_food',
    'biosphere / coastal systems':   'biosphere_coastal',
}


class Command(BaseCommand):
    help = 'Seed the database from tipping_point_seed_data.csv'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            default=str(settings.SEED_CSV),
            help='Path to the seed CSV file.',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing TippingPoint records before seeding.',
        )

    def handle(self, *args, **options):
        csv_path = Path(options['csv'])
        if not csv_path.exists():
            self.stderr.write(f'CSV not found: {csv_path}')
            return

        if options['clear']:
            deleted, _ = TippingPoint.objects.all().delete()
            self.stdout.write(f'Cleared {deleted} existing tipping point records.')

        created_count = updated_count = skipped_count = 0

        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for order, row in enumerate(reader, start=1):
                slug = row['id'].strip()

                # Map domain string to choice key
                domain_raw = row['domain'].strip()
                domain = DOMAIN_MAP.get(domain_raw.lower(), 'cryosphere')

                # Map severity to lowercase choice key
                severity_raw = row['severity'].strip().lower()

                tp, created = TippingPoint.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'name':                 row['name'].strip(),
                        'domain':               domain,
                        'domain_raw':           domain_raw,
                        'scale':                row['scale'].strip(),
                        'icon_label':           row['icon_label'].strip(),
                        'severity':             severity_raw,
                        'near_term_status':     row['near_term_status'].strip(),
                        'warming_context':      row['warming_context'].strip(),
                        'primary_causes':       row['primary_causes'].strip(),
                        'effects':              row['effects'].strip(),
                        'interactions':         row['interactions'].strip(),
                        'domino_summary':       row['domino_summary'].strip(),
                        'app_card_summary':     row['app_card_summary'].strip(),
                        'misinformation_angle': row['misinformation_angle'].strip(),
                        'suggested_ui':         row['suggested_ui'].strip(),
                        'source_urls':          row['source_urls'].strip(),
                        'display_order':        order,
                        'is_active':            True,
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

                # Seed normalised source references
                if tp.source_urls:
                    SourceReference.objects.filter(tipping_point=tp).delete()
                    for url in tp.get_source_url_list():
                        SourceReference.objects.create(tipping_point=tp, url=url)

        self.stdout.write(
            self.style.SUCCESS(
                f'Tipping points: {created_count} created, {updated_count} updated.'
            )
        )

        # Seed relationships
        rel_created = rel_skipped = 0
        tp_cache = {tp.slug: tp for tp in TippingPoint.objects.all()}

        for source_slug, target_slug, rel_type, strength, bidir in RELATIONSHIPS:
            source = tp_cache.get(source_slug)
            target = tp_cache.get(target_slug)

            if not source:
                self.stderr.write(f'  Skipping relationship: source slug not found: {source_slug}')
                rel_skipped += 1
                continue
            if not target:
                self.stderr.write(f'  Skipping relationship: target slug not found: {target_slug}')
                rel_skipped += 1
                continue

            _, created = TippingPointRelationship.objects.get_or_create(
                source=source,
                target=target,
                relationship_type=rel_type,
                defaults={
                    'strength':        strength,
                    'is_bidirectional': bidir,
                },
            )
            if created:
                rel_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Relationships: {rel_created} created, {rel_skipped} skipped.'
            )
        )

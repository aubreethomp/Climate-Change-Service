"""
python manage.py seed_claims

Seeds:
  - MisinformationTechnique  : FLICC/CARDS-style technique library
  - ClaimTopic               : topic groupings
  - ClimateClaim             : hand-curated demo claims (12 examples)
  - EvidenceSentence         : 1–3 evidence sentences per claim

In Phase 5, replace or supplement this with a CLIMATE-FEVER JSON importer.
CLIMATE-FEVER: https://github.com/tdiggelm/climate-fever-dataset
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.claims.models import (
    ClimateClaim,
    EvidenceSentence,
    MisinformationTechnique,
    ClaimTopic,
    ClaimTechniqueLink,
)
from apps.tipping_points.models import TippingPoint


TECHNIQUES = [
    {
        'slug': 'cherry_picking',
        'name': 'Cherry-Picking',
        'technique': 'cherry_picking',
        'description': 'Selecting only data or time periods that support a conclusion while ignoring contradictory evidence.',
        'example': '"Antarctic ice has been growing" — true in some regions historically, but ignores net mass loss and West Antarctic collapse risk.',
        'media_literacy_tip': 'Ask: what is the full dataset? What time period is being used, and why? Look for cherry-picked start points or geographic cherry-picks.',
        'flicc_category': 'Cherry-picking',
    },
    {
        'slug': 'fake_expert',
        'name': 'Fake Expert',
        'technique': 'fake_expert',
        'description': "Citing someone as an expert in climate science who lacks relevant credentials, or misrepresenting a real expert's position.",
        'example': 'Citing a geologist or meteorologist as a "climate scientist" who disputes warming consensus.',
        'media_literacy_tip': 'Check credentials: does the person have peer-reviewed climate research? Does their published work support the claim being made?',
        'flicc_category': 'Fake experts',
    },
    {
        'slug': 'conspiracy_framing',
        'name': 'Conspiracy Framing',
        'technique': 'conspiracy_framing',
        'description': 'Framing scientific consensus as a coordinated hoax, political conspiracy, or agenda by a powerful group.',
        'example': '"Climate change is a scheme by governments and scientists to control energy use and redistribute wealth."',
        'media_literacy_tip': 'Ask: would this conspiracy require thousands of independent scientists across hundreds of countries to coordinate silently? How plausible is that?',
        'flicc_category': 'Conspiracy theories',
    },
    {
        'slug': 'false_balance',
        'name': 'False Balance',
        'technique': 'false_balance',
        'description': 'Presenting fringe views as equally credible to the scientific consensus, implying genuine scientific controversy where little exists.',
        'example': 'Giving equal airtime to a contrarian blogger and a climate scientist to suggest 50/50 disagreement.',
        'media_literacy_tip': 'Check what proportion of relevant experts actually agree. 97%+ of publishing climate scientists agree on human-caused warming.',
        'flicc_category': 'False balance',
    },
    {
        'slug': 'misrepresentation',
        'name': 'Misrepresentation',
        'technique': 'misrepresentation',
        'description': 'Distorting or taking out of context what scientists, reports, or data actually say.',
        'example': 'Quoting "global warming paused" from an old blog to imply the IPCC said warming stopped.',
        'media_literacy_tip': 'Go to the primary source. Does the original study or report say what the claim suggests? Read the abstract or summary yourself.',
        'flicc_category': 'Misrepresentation',
    },
    {
        'slug': 'oversimplification',
        'name': 'Oversimplification',
        'technique': 'oversimplification',
        'description': 'Reducing a complex, multifactorial climate topic to a single variable, ignoring well-understood nuance.',
        'example': '"CO₂ is just plant food — more of it is good for the planet."',
        'media_literacy_tip': 'Ask what the claim leaves out. CO₂ increase has complex effects: ocean acidification, heat stress, altered precipitation patterns, and ecosystem disruption.',
        'flicc_category': 'Oversimplification',
    },
    {
        'slug': 'moving_goalposts',
        'name': 'Moving Goalposts',
        'technique': 'moving_goalposts',
        'description': 'When one piece of evidence is shown to be incorrect, switching to a new objection rather than updating the overall view.',
        'example': 'First: "it is not warming." Then: "it is warming but not human-caused." Then: "it is human-caused but not harmful."',
        'media_literacy_tip': 'Track the pattern of objections over time. If each rebuttal is met with a new objection, the person may not be engaging in good faith with evidence.',
        'flicc_category': 'Moving goalposts',
    },
    {
        'slug': 'slothful_induction',
        'name': 'Slothful Induction',
        'technique': 'slothful_induction',
        'description': 'Ignoring strong evidence to draw a weak or deliberately vague conclusion.',
        'example': '"Yes, the temperature has risen and it correlates with CO2, but we cannot be certain humans caused it."',
        'media_literacy_tip': 'Evaluate the weight of evidence. When multiple independent lines converge, "we cannot be certain" becomes an evasion, not honest uncertainty.',
        'flicc_category': 'Slothful induction',
    },
]

TOPICS = [
    'Attribution', 'Sea level', 'Arctic & ice', 'Coral reefs',
    'Temperature records', 'Permafrost & carbon', 'Ocean acidification',
    'Extreme weather', 'Consensus & expertise', 'Emissions',
]

CLAIMS = [
    {
        'claim_text': 'Climate has always changed naturally, so current warming is not caused by humans.',
        'label': 'refutes',
        'topic': 'Attribution',
        'explanation': (
            'Natural climate variability is real, but multiple independent lines of evidence — '
            'isotopic fingerprints, attribution studies, the pattern and speed of current warming — '
            'show that recent warming cannot be explained by natural factors alone and is consistent '
            'with increased greenhouse gas concentrations from human activity.'
        ),
        'difficulty': 'easy',
        'technique_slugs': ['cherry_picking', 'oversimplification'],
        'tipping_point_slugs': ['abrupt_permafrost_thaw', 'gis_collapse'],
        'evidence': [
            {
                'text': 'Multiple attribution studies distinguish natural climate variability from the greenhouse-gas-driven warming signal observed since industrialisation.',
                'stance': 'refutes',
                'source_name': 'IPCC AR6 WG1 Chapter 3',
                'source_url': 'https://www.ipcc.ch/report/ar6/wg1/',
            },
            {
                'text': 'The isotopic composition of atmospheric CO₂ — lighter carbon-13 and virtually no carbon-14 — confirms the additional CO₂ comes from fossil fuel combustion, not volcanic or oceanic sources.',
                'stance': 'refutes',
                'source_name': 'NOAA Carbon Cycle Science',
                'source_url': 'https://gml.noaa.gov/ccgg/',
            },
        ],
    },
    {
        'claim_text': 'Antarctic ice is growing, which cancels out Arctic ice losses.',
        'label': 'misleading',
        'topic': 'Arctic & ice',
        'explanation': (
            'Some parts of Antarctica have gained surface snowfall in the past, but this claim is '
            'misleading in two ways: (1) it cherry-picks East Antarctic snowfall gains while ignoring '
            'accelerating mass loss from West Antarctica and the Antarctic Peninsula; (2) total ice '
            'sheet mass balance — tracked by GRACE satellite gravity — shows net mass loss for Antarctica. '
            'Conflating sea ice extent with ice sheet mass further muddies the picture.'
        ),
        'difficulty': 'medium',
        'technique_slugs': ['cherry_picking', 'misrepresentation'],
        'tipping_point_slugs': ['wais_collapse', 'east_antarctic_subglacial_basins'],
        'evidence': [
            {
                'text': 'GRACE-FO satellite data show that Antarctica has been losing ice mass at an accelerating rate, with the largest losses concentrated in West Antarctica and the Antarctic Peninsula.',
                'stance': 'refutes',
                'source_name': 'NASA GRACE / JPL',
                'source_url': 'https://grace.jpl.nasa.gov/',
            },
        ],
    },
    {
        'claim_text': 'Coral reefs have always bleached and recovered — there is nothing unusual about current bleaching events.',
        'label': 'misleading',
        'topic': 'Coral reefs',
        'explanation': (
            'Corals can recover from bleaching events if ocean temperatures return to normal and '
            'sufficient time is given. However, the frequency, geographic scale, and severity of '
            'bleaching events have increased dramatically with ocean warming. Recovery requires '
            'typically 10–15 years; bleaching events are now recurring faster than reefs can recover, '
            'causing cumulative mortality. The 2024 fourth global bleaching event is an example of '
            'this accelerating pattern.'
        ),
        'difficulty': 'medium',
        'technique_slugs': ['cherry_picking', 'oversimplification'],
        'tipping_point_slugs': ['warm_water_coral_reefs_dieoff'],
        'evidence': [
            {
                'text': 'Bleaching frequency has increased from roughly once per 25–30 years in the 1980s to once every 5–6 years by the 2010s, faster than the recovery window for most reef systems.',
                'stance': 'refutes',
                'source_name': 'Hughes et al., Science 2018',
                'source_url': 'https://www.science.org/doi/10.1126/science.aan8048',
            },
        ],
    },
    {
        'claim_text': 'CO₂ is plant food — increasing CO₂ will make the Earth greener and more productive.',
        'label': 'misleading',
        'topic': 'Emissions',
        'explanation': (
            'CO₂ fertilisation does boost plant growth in some controlled conditions, and some '
            'satellite studies show partial greening in certain regions. However, this framing '
            'ignores that higher temperatures, drought, altered precipitation, and ocean acidification '
            'from the same CO₂ increase cause net losses in many ecosystems. Crop yield studies show '
            'that heat stress and altered rainfall patterns outweigh CO₂ fertilisation benefits at '
            'higher warming levels.'
        ),
        'difficulty': 'hard',
        'technique_slugs': ['oversimplification', 'cherry_picking'],
        'tipping_point_slugs': ['amazon_rainforest_dieback'],
        'evidence': [
            {
                'text': 'While elevated CO₂ can stimulate some plant growth, studies find that increased drought frequency, heat stress, and altered seasonality reduce agricultural yields in many staple crops at warming levels projected for mid-century.',
                'stance': 'refutes',
                'source_name': 'Lobell & Gourdji, Plant Physiology 2012',
                'source_url': 'https://doi.org/10.1104/pp.112.208298',
            },
        ],
    },
    {
        'claim_text': 'Global warming paused for 15 years after 1998, proving the models are wrong.',
        'label': 'misleading',
        'topic': 'Temperature records',
        'explanation': (
            '1998 was an unusually warm El Niño year, making it a cherry-picked baseline. '
            'Short-term variability from El Niño/La Niña cycles can mask the underlying trend '
            'when you choose such a starting point. The long-term warming trend continued throughout '
            'this period, and 2014–2024 have all been among the hottest years on record. The ocean '
            'also continued absorbing heat throughout the supposed "pause".'
        ),
        'difficulty': 'medium',
        'technique_slugs': ['cherry_picking', 'misrepresentation'],
        'tipping_point_slugs': ['warm_water_coral_reefs_dieoff', 'amoc_collapse'],
        'evidence': [
            {
                'text': 'Statistical analyses show that the apparent "hiatus" disappears when a robust start year is chosen and when internal variability (El Niño/La Niña) is accounted for; the long-term trend continued uninterrupted.',
                'stance': 'refutes',
                'source_name': 'Rahmstorf et al., Nature Climate Change 2017',
                'source_url': 'https://www.nature.com/articles/nclimate3226',
            },
        ],
    },
    {
        'claim_text': 'Permafrost contains vast amounts of carbon, but it is frozen solid and poses no near-term risk.',
        'label': 'misleading',
        'topic': 'Permafrost & carbon',
        'explanation': (
            'Much permafrost is indeed deep and frozen, but abrupt thaw processes — thermokarst '
            'lakes, retrogressive thaw slumps, and active-layer deepening — are already releasing '
            'methane and CO₂ from near-surface deposits. Yedoma deposits in Siberia and Alaska '
            'are particularly vulnerable and carbon-rich. These are not far-future risks; field '
            'measurements already show increasing emissions from Arctic permafrost regions.'
        ),
        'difficulty': 'hard',
        'technique_slugs': ['oversimplification', 'cherry_picking'],
        'tipping_point_slugs': ['abrupt_permafrost_thaw', 'permafrost_yedoma_carbon'],
        'evidence': [
            {
                'text': 'Observations from field stations across Siberia and Alaska document accelerating methane flux from permafrost regions, with abrupt thaw features forming faster than previously projected.',
                'stance': 'refutes',
                'source_name': 'Turetsky et al., Nature Geoscience 2019',
                'source_url': 'https://doi.org/10.1038/s41561-019-0527-5',
            },
        ],
    },
    {
        'claim_text': 'Sea level rise is only a few millimetres per year — too slow to matter.',
        'label': 'misleading',
        'topic': 'Sea level',
        'explanation': (
            'Current sea-level rise (~3.7 mm/year) is accelerating, not static. More importantly, '
            'even small increases in mean sea level dramatically increase the frequency of extreme '
            'flood events for low-lying coasts. A 10 cm rise can double or triple the frequency of '
            'events that used to occur once per decade. For small island nations and densely populated '
            'deltas, the cumulative effect is existential.'
        ),
        'difficulty': 'easy',
        'technique_slugs': ['oversimplification'],
        'tipping_point_slugs': ['gis_collapse', 'wais_collapse'],
        'evidence': [
            {
                'text': 'Satellite altimetry records show sea-level rise is accelerating; the rate in 2020–2023 is approximately double the rate measured in the 1990s.',
                'stance': 'refutes',
                'source_name': 'NASA Sea Level Change Portal',
                'source_url': 'https://sealevel.nasa.gov/',
            },
        ],
    },
    {
        'claim_text': 'The AMOC is a natural ocean circulation pattern and has changed before — current changes are not alarming.',
        'label': 'misleading',
        'topic': 'Attribution',
        'explanation': (
            'Yes, the AMOC has varied naturally in past climates. But the current slowdown shows '
            'fingerprints consistent with anthropogenic freshwater forcing from Greenland melt — '
            'a mechanism that was not present during past natural variability at comparable speed. '
            'Multiple proxy reconstructions suggest the AMOC is now at its weakest in over 1,000 years, '
            'and model projections warn of possible collapse under higher warming scenarios.'
        ),
        'difficulty': 'hard',
        'technique_slugs': ['cherry_picking', 'misrepresentation'],
        'tipping_point_slugs': ['amoc_collapse', 'gis_collapse'],
        'evidence': [
            {
                'text': 'Proxy-based reconstructions using sediment records suggest the AMOC is currently weaker than at any point in the last millennium, with the weakening linked to increased freshwater input from Greenland.',
                'stance': 'refutes',
                'source_name': 'Caesar et al., Nature Climate Change 2021',
                'source_url': 'https://doi.org/10.1038/s41558-021-01097-4',
            },
        ],
    },
    {
        'claim_text': 'Extreme weather events have always occurred — we cannot link individual storms or droughts to climate change.',
        'label': 'misleading',
        'topic': 'Extreme weather',
        'explanation': (
            'The field of extreme event attribution has advanced significantly. Studies can now '
            'quantify how much climate change increases the probability or intensity of specific '
            'events. For example, attribution science found that the 2021 Pacific Northwest heat '
            'dome was "virtually impossible" without climate change. The claim that no individual '
            'event can be linked to climate change was accurate in 2005 but is outdated science today.'
        ),
        'difficulty': 'medium',
        'technique_slugs': ['slothful_induction', 'moving_goalposts'],
        'tipping_point_slugs': ['west_african_monsoon_shift'],
        'evidence': [
            {
                'text': 'The World Weather Attribution initiative has published probabilistic attribution studies for dozens of extreme events, finding that climate change substantially increased the likelihood of most major heat waves and precipitation extremes studied.',
                'stance': 'refutes',
                'source_name': 'World Weather Attribution',
                'source_url': 'https://www.worldweatherattribution.org/',
            },
        ],
    },
    {
        'claim_text': 'There is no scientific consensus on climate change — thousands of scientists have signed petitions disputing it.',
        'label': 'refutes',
        'topic': 'Consensus & expertise',
        'explanation': (
            'Multiple independent analyses of the peer-reviewed literature find that 97% or more '
            'of actively publishing climate scientists agree that recent warming is primarily '
            'human-caused. Petitions like the Oregon Petition included non-climate scientists '
            '(engineers, medical doctors) and fabricated names; a fake expert technique. '
            'Consensus among domain experts, not petition signatories, is the relevant measure.'
        ),
        'difficulty': 'easy',
        'technique_slugs': ['fake_expert', 'misrepresentation'],
        'tipping_point_slugs': [],
        'evidence': [
            {
                'text': 'Cook et al. (2013) analysed 11,944 climate abstracts and found 97% of papers taking a position endorsed the consensus on human-caused warming; a follow-up study of 69,406 authors found 97.2% agreement.',
                'stance': 'refutes',
                'source_name': 'Cook et al., Environmental Research Letters 2013',
                'source_url': 'https://doi.org/10.1088/1748-9326/8/2/024024',
            },
        ],
    },
    {
        'claim_text': 'Ocean acidification is a minor concern — the ocean is still alkaline, not acidic.',
        'label': 'misleading',
        'topic': 'Ocean acidification',
        'explanation': (
            'The claim plays on terminology. "Acidification" refers to the direction of change — '
            'ocean pH has dropped from 8.2 to 8.1 since industrialisation, a 26% increase in '
            'hydrogen ion concentration. While the ocean remains alkaline, this rate of change '
            'is faster than anything in the past 300 million years, and many marine organisms '
            '(corals, pteropods, oysters, certain plankton) are highly sensitive to even small '
            'pH shifts that affect their ability to form shells and skeletons.'
        ),
        'difficulty': 'medium',
        'technique_slugs': ['misrepresentation', 'oversimplification'],
        'tipping_point_slugs': ['warm_water_coral_reefs_dieoff', 'mangrove_seagrass_dieoff'],
        'evidence': [
            {
                'text': 'Since the Industrial Revolution, ocean surface pH has decreased from approximately 8.2 to 8.1, representing a 26% increase in acidity; this rate of change is unprecedented in the geological record of the past 65 million years.',
                'stance': 'refutes',
                'source_name': 'NOAA Ocean Acidification Program',
                'source_url': 'https://oceanacidification.noaa.gov/',
            },
        ],
    },
    {
        'claim_text': 'Fisheries have always experienced boom-bust cycles — current declines are normal and will recover naturally.',
        'label': 'misleading',
        'topic': 'Sea level',
        'explanation': (
            'While fisheries do fluctuate, the combination of sustained overfishing, habitat loss '
            '(coral reef and mangrove degradation), ocean warming, deoxygenation, and acidification '
            'creates compounding stressors that were not present in previous natural cycles. '
            'Some collapsed stocks have not recovered even after decades of reduced fishing pressure, '
            'suggesting the ecological baseline itself has shifted.'
        ),
        'difficulty': 'hard',
        'technique_slugs': ['cherry_picking', 'oversimplification'],
        'tipping_point_slugs': ['fisheries_collapse', 'warm_water_coral_reefs_dieoff'],
        'evidence': [
            {
                'text': 'FAO reports that over 35% of global fish stocks are now harvested at biologically unsustainable levels, with multiple stocks showing no recovery after fishing pressure was reduced, suggesting persistent ecosystem-level change.',
                'stance': 'refutes',
                'source_name': 'FAO State of World Fisheries 2022',
                'source_url': 'https://www.fao.org/fishery/en/sofia',
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed demo climate claims, techniques, and topics'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing claims before seeding.')

    def handle(self, *args, **options):
        if options['clear']:
            ClimateClaim.objects.all().delete()
            MisinformationTechnique.objects.all().delete()
            ClaimTopic.objects.all().delete()
            self.stdout.write('Cleared existing claims data.')

        # Misinformation techniques
        tech_map = {}
        for t in TECHNIQUES:
            obj, _ = MisinformationTechnique.objects.update_or_create(slug=t['slug'], defaults=t)
            tech_map[t['slug']] = obj
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(TECHNIQUES)} misinformation techniques.'))

        # Claim topics
        topic_map = {}
        for name in TOPICS:
            obj, _ = ClaimTopic.objects.get_or_create(name=name)
            topic_map[name] = obj
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(TOPICS)} claim topics.'))

        # Tipping points (pre-load for linking) 
        tp_map = {tp.slug: tp for tp in TippingPoint.objects.all()}

        # Claims 
        created = 0
        for c in CLAIMS:
            evidence_data     = c.pop('evidence')
            technique_slugs   = c.pop('technique_slugs')
            tipping_pt_slugs  = c.pop('tipping_point_slugs')
            topic_name        = c.pop('topic')

            c['topic']          = topic_map.get(topic_name)
            c['source_dataset'] = 'hand-curated'

            claim, was_created = ClimateClaim.objects.update_or_create(
                claim_text=c['claim_text'], defaults=c
            )

            # Evidence 
            EvidenceSentence.objects.filter(claim=claim).delete()
            for ev in evidence_data:
                EvidenceSentence.objects.create(claim=claim, **ev)

            # Technique links
            ClaimTechniqueLink.objects.filter(claim=claim).delete()
            for slug in technique_slugs:
                tech = tech_map.get(slug)
                if tech:
                    ClaimTechniqueLink.objects.get_or_create(claim=claim, technique=tech)

            # Tipping point links
            claim.related_tipping_points.set(
                [tp_map[s] for s in tipping_pt_slugs if s in tp_map]
            )

            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Seeded {created} new claims ({len(CLAIMS)} total processed).'))

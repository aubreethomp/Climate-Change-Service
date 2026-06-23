"""
0002_seed_claims.py

Data migration: inserts misinformation techniques, claim topics, 12 demo
climate claims, their evidence sentences, and all cross-links to tipping points.
"""
from django.db import migrations

TECHNIQUES = [
    {
        'slug': 'cherry_picking',
        'name': 'Cherry-Picking',
        'technique': 'cherry_picking',
        'description': 'Selecting only data or time periods that support a conclusion while ignoring contradictory evidence.',
        'example': '"Antarctic ice has been growing" - true in some regions historically, but ignores net mass loss and West Antarctic collapse risk.',
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
        'example': '"CO2 is just plant food - more of it is good for the planet."',
        'media_literacy_tip': 'Ask what the claim leaves out. CO2 increase has complex effects: ocean acidification, heat stress, altered precipitation patterns, and ecosystem disruption.',
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

# Each claim: text, label, topic, difficulty, explanation, evidence list,
# technique slugs, tipping point slugs
CLAIMS = [
    {
        'claim_text': 'Climate has always changed naturally, so current warming is not caused by humans.',
        'label': 'refutes',
        'topic': 'Attribution',
        'difficulty': 'easy',
        'explanation': (
            'Natural climate variability is real, but multiple independent lines of evidence - '
            'isotopic fingerprints, attribution studies, the pattern and speed of current warming - '
            'show that recent warming cannot be explained by natural factors alone and is consistent '
            'with increased greenhouse gas concentrations from human activity.'
        ),
        'technique_slugs': ['cherry_picking', 'oversimplification'],
        'tp_slugs': ['abrupt_permafrost_thaw', 'gis_collapse'],
        'evidence': [
            {
                'text': 'Multiple attribution studies distinguish natural climate variability from the greenhouse-gas-driven warming signal observed since industrialisation.',
                'stance': 'refutes',
                'source_name': 'IPCC AR6 WG1 Chapter 3',
                'source_url': 'https://www.ipcc.ch/report/ar6/wg1/',
            },
            {
                'text': 'The isotopic composition of atmospheric CO2 confirms the additional CO2 comes from fossil fuel combustion, not volcanic or oceanic sources.',
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
        'difficulty': 'medium',
        'explanation': (
            'Some parts of Antarctica have gained surface snowfall in the past, but this claim is '
            'misleading in two ways: it cherry-picks East Antarctic snowfall gains while ignoring '
            'accelerating mass loss from West Antarctica and the Antarctic Peninsula; and total ice '
            'sheet mass balance shows net mass loss for Antarctica.'
        ),
        'technique_slugs': ['cherry_picking', 'misrepresentation'],
        'tp_slugs': ['wais_collapse', 'east_antarctic_subglacial_basins'],
        'evidence': [
            {
                'text': 'GRACE-FO satellite data show that Antarctica has been losing ice mass at an accelerating rate, with the largest losses in West Antarctica and the Antarctic Peninsula.',
                'stance': 'refutes',
                'source_name': 'NASA GRACE / JPL',
                'source_url': 'https://grace.jpl.nasa.gov/',
            },
        ],
    },
    {
        'claim_text': 'Coral reefs have always bleached and recovered - there is nothing unusual about current bleaching events.',
        'label': 'misleading',
        'topic': 'Coral reefs',
        'difficulty': 'medium',
        'explanation': (
            'Corals can recover from bleaching if ocean temperatures return to normal and sufficient '
            'time is given. However, bleaching frequency has increased dramatically with ocean warming. '
            'Recovery requires typically 10-15 years; bleaching events are now recurring faster than '
            'reefs can recover, causing cumulative mortality.'
        ),
        'technique_slugs': ['cherry_picking', 'oversimplification'],
        'tp_slugs': ['warm_water_coral_reefs_dieoff'],
        'evidence': [
            {
                'text': 'Bleaching frequency has increased from roughly once per 25-30 years in the 1980s to once every 5-6 years by the 2010s, faster than the recovery window for most reef systems.',
                'stance': 'refutes',
                'source_name': 'Hughes et al., Science 2018',
                'source_url': 'https://www.science.org/doi/10.1126/science.aan8048',
            },
        ],
    },
    {
        'claim_text': 'CO2 is plant food - increasing CO2 will make the Earth greener and more productive.',
        'label': 'misleading',
        'topic': 'Emissions',
        'difficulty': 'hard',
        'explanation': (
            'CO2 fertilisation does boost plant growth in some controlled conditions. However, this '
            'framing ignores that higher temperatures, drought, altered precipitation, and ocean '
            'acidification from the same CO2 increase cause net losses in many ecosystems. Crop '
            'yield studies show that heat stress and altered rainfall outweigh CO2 fertilisation '
            'benefits at higher warming levels.'
        ),
        'technique_slugs': ['oversimplification', 'cherry_picking'],
        'tp_slugs': ['amazon_rainforest_dieback'],
        'evidence': [
            {
                'text': 'While elevated CO2 can stimulate some plant growth, studies find that increased drought frequency, heat stress, and altered seasonality reduce agricultural yields in many staple crops at mid-century warming levels.',
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
        'difficulty': 'medium',
        'explanation': (
            '1998 was an unusually warm El Nino year, making it a cherry-picked baseline. '
            'Short-term variability from El Nino/La Nina cycles can mask the underlying trend. '
            'The long-term warming trend continued throughout this period, and 2014-2024 have all '
            'been among the hottest years on record. The ocean also continued absorbing heat '
            'throughout the supposed "pause".'
        ),
        'technique_slugs': ['cherry_picking', 'misrepresentation'],
        'tp_slugs': ['warm_water_coral_reefs_dieoff', 'amoc_collapse'],
        'evidence': [
            {
                'text': 'Statistical analyses show that the apparent "hiatus" disappears when a robust start year is chosen and when internal variability is accounted for; the long-term trend continued uninterrupted.',
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
        'difficulty': 'hard',
        'explanation': (
            'Much permafrost is indeed deep and frozen, but abrupt thaw processes - thermokarst '
            'lakes, retrogressive thaw slumps, and active-layer deepening - are already releasing '
            'methane and CO2 from near-surface deposits. Field measurements already show increasing '
            'emissions from Arctic permafrost regions.'
        ),
        'technique_slugs': ['oversimplification', 'cherry_picking'],
        'tp_slugs': ['abrupt_permafrost_thaw', 'permafrost_yedoma_carbon'],
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
        'claim_text': 'Sea level rise is only a few millimetres per year - too slow to matter.',
        'label': 'misleading',
        'topic': 'Sea level',
        'difficulty': 'easy',
        'explanation': (
            'Current sea-level rise (~3.7 mm/year) is accelerating, not static. More importantly, '
            'even small increases in mean sea level dramatically increase the frequency of extreme '
            'flood events for low-lying coasts. A 10 cm rise can double or triple the frequency of '
            'events that used to occur once per decade.'
        ),
        'technique_slugs': ['oversimplification'],
        'tp_slugs': ['gis_collapse', 'wais_collapse'],
        'evidence': [
            {
                'text': 'Satellite altimetry records show sea-level rise is accelerating; the rate in 2020-2023 is approximately double the rate measured in the 1990s.',
                'stance': 'refutes',
                'source_name': 'NASA Sea Level Change Portal',
                'source_url': 'https://sealevel.nasa.gov/',
            },
        ],
    },
    {
        'claim_text': 'The AMOC is a natural ocean circulation pattern and has changed before - current changes are not alarming.',
        'label': 'misleading',
        'topic': 'Attribution',
        'difficulty': 'hard',
        'explanation': (
            'Yes, the AMOC has varied naturally in past climates. But the current slowdown shows '
            'fingerprints consistent with anthropogenic freshwater forcing from Greenland melt. '
            'Multiple proxy reconstructions suggest the AMOC is now at its weakest in over 1,000 '
            'years, and model projections warn of possible collapse under higher warming scenarios.'
        ),
        'technique_slugs': ['cherry_picking', 'misrepresentation'],
        'tp_slugs': ['amoc_collapse', 'gis_collapse'],
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
        'claim_text': 'Extreme weather events have always occurred - we cannot link individual storms or droughts to climate change.',
        'label': 'misleading',
        'topic': 'Extreme weather',
        'difficulty': 'medium',
        'explanation': (
            'The field of extreme event attribution has advanced significantly. Studies can now '
            'quantify how much climate change increases the probability or intensity of specific '
            'events. The claim that no individual event can be linked to climate change was '
            'accurate in 2005 but is outdated science today.'
        ),
        'technique_slugs': ['slothful_induction', 'moving_goalposts'],
        'tp_slugs': ['west_african_monsoon_shift'],
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
        'claim_text': 'There is no scientific consensus on climate change - thousands of scientists have signed petitions disputing it.',
        'label': 'refutes',
        'topic': 'Consensus & expertise',
        'difficulty': 'easy',
        'explanation': (
            'Multiple independent analyses of the peer-reviewed literature find that 97% or more '
            'of actively publishing climate scientists agree that recent warming is primarily '
            'human-caused. Petitions like the Oregon Petition included non-climate scientists '
            'and fabricated names; a fake expert technique.'
        ),
        'technique_slugs': ['fake_expert', 'misrepresentation'],
        'tp_slugs': [],
        'evidence': [
            {
                'text': 'Cook et al. (2013) analysed 11,944 climate abstracts and found 97% of papers taking a position endorsed the consensus on human-caused warming.',
                'stance': 'refutes',
                'source_name': 'Cook et al., Environmental Research Letters 2013',
                'source_url': 'https://doi.org/10.1088/1748-9326/8/2/024024',
            },
        ],
    },
    {
        'claim_text': 'Ocean acidification is a minor concern - the ocean is still alkaline, not acidic.',
        'label': 'misleading',
        'topic': 'Ocean acidification',
        'difficulty': 'medium',
        'explanation': (
            'The claim plays on terminology. "Acidification" refers to the direction of change - '
            'ocean pH has dropped from 8.2 to 8.1 since industrialisation, a 26% increase in '
            'hydrogen ion concentration. This rate of change is faster than anything in the past '
            '300 million years, and many marine organisms are highly sensitive to even small pH shifts.'
        ),
        'technique_slugs': ['misrepresentation', 'oversimplification'],
        'tp_slugs': ['warm_water_coral_reefs_dieoff', 'mangrove_seagrass_dieoff'],
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
        'claim_text': 'Fisheries have always experienced boom-bust cycles - current declines are normal and will recover naturally.',
        'label': 'misleading',
        'topic': 'Sea level',
        'difficulty': 'hard',
        'explanation': (
            'While fisheries do fluctuate, the combination of sustained overfishing, habitat loss, '
            'ocean warming, deoxygenation, and acidification creates compounding stressors not present '
            'in previous natural cycles. Some collapsed stocks have not recovered even after decades '
            'of reduced fishing pressure, suggesting the ecological baseline itself has shifted.'
        ),
        'technique_slugs': ['cherry_picking', 'oversimplification'],
        'tp_slugs': ['fisheries_collapse', 'warm_water_coral_reefs_dieoff'],
        'evidence': [
            {
                'text': 'FAO reports that over 35% of global fish stocks are now harvested at biologically unsustainable levels, with multiple stocks showing no recovery after fishing pressure was reduced.',
                'stance': 'refutes',
                'source_name': 'FAO State of World Fisheries 2022',
                'source_url': 'https://www.fao.org/fishery/en/sofia',
            },
        ],
    },
]


def seed_claims(apps, schema_editor):
    MisinformationTechnique = apps.get_model('claims', 'MisinformationTechnique')
    ClaimTopic              = apps.get_model('claims', 'ClaimTopic')
    ClimateClaim            = apps.get_model('claims', 'ClimateClaim')
    EvidenceSentence        = apps.get_model('claims', 'EvidenceSentence')
    ClaimTechniqueLink      = apps.get_model('claims', 'ClaimTechniqueLink')
    TippingPoint            = apps.get_model('tipping_points', 'TippingPoint')

    # Techniques
    tech_cache = {}
    for t in TECHNIQUES:
        obj, _ = MisinformationTechnique.objects.get_or_create(slug=t['slug'], defaults=t)
        tech_cache[t['slug']] = obj

    # Topics
    topic_cache = {}
    for name in TOPICS:
        obj, _ = ClaimTopic.objects.get_or_create(name=name)
        topic_cache[name] = obj

    # Tipping points (pre-loaded for M2M)
    tp_cache = {tp.slug: tp for tp in TippingPoint.objects.all()}

    # Claims
    for c in CLAIMS:
        evidence_data  = c.pop('evidence')
        tech_slugs     = c.pop('technique_slugs')
        tp_slugs       = c.pop('tp_slugs')
        topic_name     = c.pop('topic')

        claim, _ = ClimateClaim.objects.get_or_create(
            claim_text=c['claim_text'],
            defaults={
                **c,
                'topic':          topic_cache.get(topic_name),
                'source_dataset': 'hand-curated',
                'is_active':      True,
            },
        )

        for ev in evidence_data:
            EvidenceSentence.objects.get_or_create(claim=claim, text=ev['text'], defaults=ev)

        for slug in tech_slugs:
            tech = tech_cache.get(slug)
            if tech:
                ClaimTechniqueLink.objects.get_or_create(claim=claim, technique=tech)

        for slug in tp_slugs:
            tp = tp_cache.get(slug)
            if tp:
                claim.related_tipping_points.add(tp)


def unseed_claims(apps, schema_editor):
    ClimateClaim            = apps.get_model('claims', 'ClimateClaim')
    MisinformationTechnique = apps.get_model('claims', 'MisinformationTechnique')
    ClaimTopic              = apps.get_model('claims', 'ClaimTopic')
    ClimateClaim.objects.filter(source_dataset='hand-curated').delete()
    MisinformationTechnique.objects.filter(slug__in=[t['slug'] for t in TECHNIQUES]).delete()
    ClaimTopic.objects.filter(name__in=TOPICS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_claims, reverse_code=unseed_claims),
    ]

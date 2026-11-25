"""Generate deployment URLs and search metadata for the static Caldwellings site."""
import argparse
import json
import re
from html import escape, unescape
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as XML

ROOT = Path(__file__).resolve().parents[1]
NOINDEX = {'home-om', 'about-om', 'contact-om', 'read-me-om', 'new-gallery', 'caldwellings-referral'}
DUPLICATES = {'home': '', 'closingcostsbuyers': 'new-page'}
DESCRIPTIONS = {
    '': 'Buy, sell or invest in New York real estate with Caldwellings, an independent Brooklyn brokerage led by Molly Caldwell.',
    'home-om': 'Browse the archived yoga homepage formerly hosted on the Caldwellings website.',
    'about': 'Meet Molly Caldwell, founder of Caldwellings, an independent Brooklyn brokerage serving real estate buyers, sellers and investors.',
    'buyers': 'Get help buying a New York home with Caldwellings, from starting your property search to preparing an offer and closing.',
    'before-you-buy': 'Preparing to buy a home in New York? Review the questions and decisions to consider before you start looking.',
    'first-time-buyers': 'Answers for first-time New York homebuyers on getting started, financing a purchase and working with a real estate broker.',
    'new-page': 'Review common buyer closing costs in New York, including transaction expenses for condos, co-ops and houses.',
    'sellers-1': 'Follow the steps to selling a New York property with Caldwellings, from preparing to list through offers, inspections and closing.',
    'sellers': 'Read Caldwellings’ tips on preparing, pricing and presenting your New York property for sale.',
    'new-page-1': 'Request a free market evaluation from Caldwellings and share your New York property address, condition and selling timeframe.',
    'seller-closing-costs-1': 'Review typical expenses for selling a New York condo, co-op or house with the Caldwellings seller closing cost guide.',
    'past-sales': 'Explore Caldwellings listings and its New York archive of sales and rentals. Preview available property photos or open individual listing pages.',
    'contact': 'Contact Molly Caldwell, a Brooklyn real estate broker, by phone or email for help buying, selling or investing in New York property.',
    'testimonials': 'Read client testimonials about working with Molly Caldwell and Caldwellings on New York real estate transactions.',
    'giving-back-1': 'Learn about New York community organizations and causes supported by Caldwellings.',
    'marketreports': 'Find Caldwellings’ archived 2022 real estate market reports.',
    'apartment-rental-application': 'Open the Caldwellings rental application and find the separate form used to make an offer on an apartment sale.',
    'apartment-sale-offer-form': 'Download the fillable Caldwellings apartment sale offer form and find contact information for questions about submitting an offer.',
    'agency-fair-housing-covid': 'Find Caldwellings agency disclosures and Fair Housing documents for New York property buyers and sellers.',
    'standard-operating-procedures': 'Review Caldwellings’ published standard operating procedures for prospective New York homebuyers.',
    'legal': 'Review the Caldwellings legal notices and terms for using its New York real estate website.',
}
WEB_TYPES = {'': 'WebPage', 'about': 'AboutPage', 'contact': 'ContactPage', 'past-sales': 'CollectionPage'}
META_BLOCK = re.compile(r'\n?<!-- seo:start -->.*?<!-- seo:end -->\n?', re.S)
DESCRIPTION_TAG = re.compile(r'<meta name="description" content="[^"]*">\n?')

def text_content(source):
    return ' '.join(unescape(re.sub(r'<[^>]+>', ' ', source)).split())

def tag(name, content, attribute='name'):
    return f'<meta {attribute}="{name}" content="{escape(content, quote=True)}">'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('site_url', help='Public HTTPS site base URL, optionally with a hosting subpath')
    args = parser.parse_args()
    base = args.site_url.rstrip('/')
    url = urlsplit(base)
    if url.scheme != 'https' or not url.hostname or url.query or url.fragment or url.username:
        parser.error('Provide a public HTTPS base URL without a query or fragment.')

    def route(slug):
        return base + '/' + (slug + '/' if slug else '')

    company = {
        '@type': 'RealEstateAgent', '@id': route('') + '#brokerage',
        'name': 'Caldwellings Real Estate', 'alternateName': 'Caldwellings',
        'url': route(''), 'telephone': '+1-646-265-6580', 'email': 'molly@caldwellings.com',
        'areaServed': {'@type': 'City', 'name': 'New York City'},
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Brooklyn', 'addressRegion': 'NY', 'addressCountry': 'US'},
        'founder': {'@type': 'Person', 'name': 'Molly Caldwell'},
    }
    website = {'@type': 'WebSite', '@id': route('') + '#website', 'url': route(''),
               'name': 'Caldwellings Real Estate', 'inLanguage': 'en', 'publisher': {'@id': company['@id']}}
    sitemap = XML.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for page in [ROOT / 'index.html', *sorted(ROOT.glob('*/index.html'))]:
        slug = '' if page.parent == ROOT else page.parent.name
        source = page.read_text(encoding='utf-8')
        source = DESCRIPTION_TAG.sub('', META_BLOCK.sub('\n', source))
        title = text_content(re.search(r'<title>(.*?)</title>', source, re.S)[1])
        heading = text_content(re.search(r'<h1\b[^>]*>(.*?)</h1>', source, re.S)[1])
        noindex = slug in NOINDEX or 'floorplan' in slug
        if slug in DESCRIPTIONS:
            description = DESCRIPTIONS[slug]
        elif 'floorplan' in slug:
            description = f'View the building layout for {heading} in the Caldwellings property archive.'
        elif slug in NOINDEX or slug in DUPLICATES:
            description = f'{heading} from the Caldwellings website archive.'
        else:
            description = f'Explore property photographs and listing details for {heading} in the Caldwellings New York real estate catalog.'
        canonical = route(DUPLICATES.get(slug, slug))
        property_image = re.search(r'<div class="gallery">.*?<img src="\.\./(images/catalog/[^"]+)"', source, re.S)
        image_url = base + '/' + (unescape(property_image[1]) if property_image else 'images/brooklyn.jpg')
        image_alt = f'Property photograph for {heading}' if property_image else 'Brooklyn brownstone townhouses'
        tags = [
            tag('description', description),
            f'<link rel="canonical" href="{escape(canonical, quote=True)}">',
            tag('robots', 'noindex, follow' if noindex else 'max-image-preview:large'),
            tag('og:type', 'website', 'property'), tag('og:site_name', 'Caldwellings Real Estate', 'property'),
            tag('og:title', title, 'property'), tag('og:description', description, 'property'),
            tag('og:url', canonical, 'property'), tag('og:image', image_url, 'property'),
            tag('og:image:alt', image_alt, 'property'), tag('og:locale', 'en_US', 'property'),
            tag('twitter:card', 'summary_large_image'),
        ]
        if not noindex and slug not in DUPLICATES:
            webpage = {'@type': WEB_TYPES.get(slug, 'WebPage'), '@id': canonical + '#page',
                       'url': canonical, 'name': title, 'description': description, 'inLanguage': 'en',
                       'isPartOf': {'@id': website['@id']}}
            graph = [website, company, webpage]
            if slug:
                breadcrumb = {'@type': 'BreadcrumbList', '@id': canonical + '#breadcrumb', 'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': route('')},
                    {'@type': 'ListItem', 'position': 2, 'name': heading, 'item': canonical},
                ]}
                webpage['breadcrumb'] = {'@id': breadcrumb['@id']}
                if '← Back to properties' not in source:
                    graph.append(breadcrumb)
                else:
                    webpage.pop('breadcrumb')
            data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('<', '\\u003c')
            tags.append(f'<script type="application/ld+json">{data}</script>')
            XML.SubElement(XML.SubElement(sitemap, 'url'), 'loc').text = canonical
        page.write_text(source.replace('</head>', '\n<!-- seo:start -->\n' + '\n'.join(tags) + '\n<!-- seo:end -->\n</head>', 1), encoding='utf-8')
    XML.indent(sitemap)
    XML.ElementTree(sitemap).write(ROOT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n', encoding='utf-8')

if __name__ == '__main__':
    main()

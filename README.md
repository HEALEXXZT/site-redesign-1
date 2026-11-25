# Caldwellings redesign

Extract the entire archive and open `index.html`. The English static site includes the homepage and recovered Caldwellings pages from the public menu, sitemap and internal links. The original slugs are represented by folders. The explicit `index.html` links also work when opening the files directly.

- Desktop navigation uses grouped menus. Mobile navigation uses a bottom bar and a keyboard-accessible menu.
- Contact and market evaluation forms validate the required fields, then open a mail draft. The official online forms can transmit inquiries through Caldwellings. The draft site does not store or send submissions. The rental application opens its original Jotform, and the sale offer is a local fillable PDF.
- Third-party destinations, market reports and disclosure documents can require internet access. Historic property prices and statuses reflect the original archive. The former class schedule linked from the separate yoga pages returned HTTP 404.
- The original homepage lists two street addresses. The main contact details use Brooklyn, NY and the published phone and email.
- Own-domain page transitions use the browser's View Transitions feature where supported. The site honors reduced-motion settings.

## Photography

- [Brooklyn brownstones by Bee](https://unsplash.com/photos/brownstone-townhouses-with-iron-railings-tHOYEWuIsjQ) and [Upper West Side brownstone stoop by Malia Moore](https://unsplash.com/photos/brownstone-stairs-with-potted-plant-and-trees-EhCTBJSL5Es) are neighborhood illustrations used under the [Unsplash License](https://unsplash.com/license).
- Property photos and other migrated editorial imagery are from the respective Caldwellings pages. Confirm rights to republish those originals before deployment.

## Motion and mobile navigation

The first homepage visit in a tab gets a short branded intro tied to decoding the hero image. It has a time limit and honors reduced motion. The mobile dock floats above the bottom safe area. Native page transitions are progressive enhancement.

## Search deployment

Canonical URLs, social sharing tags, structured data and the sitemap currently target `https://www.caldwellings.com`. This is the original business domain and a configuration default. If publishing elsewhere, including under a GitHub Pages project path, run `python scripts/configure-seo.py https://example.com/project` before deployment. For a subpath deployment, configure the host-root `/robots.txt` if you control it or submit the sitemap directly in Search Console. Serve the project over HTTPS. The sitemap uses directory URLs and the local links explicitly target `index.html` so they also work after extraction.

The sitemap contains preferred brokerage and listing URLs. The duplicate homepage and closing-cost page point to their preferred pages. Unrelated legacy content, the legacy referral form and stand-alone floorplan URLs are marked noindex. Floors remain reachable from the listing pages. Organization markup uses the Brooklyn locality because the original supplied conflicting street addresses. The project includes HTML content, descriptive headings and JSON-LD. Live indexing, Search Console verification and field performance data depend on deployment.

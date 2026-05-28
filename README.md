# African Sky Villas — Activity Brochure Site

A single-page Netlify-ready static site showcasing all 14 tours and activities with an integrated booking form.

## Deploy to Netlify (3 minutes)

### Option 1 — Drag & Drop (easiest)
1. Go to https://app.netlify.com/drop
2. Drag this **entire folder** onto the page
3. Done. Netlify gives you a URL like `https://random-name-12345.netlify.app`
4. In Netlify dashboard → Site settings → **Change site name** to something like `african-sky-villas`

### Option 2 — Connect via Git
1. Push this folder to a GitHub repo
2. In Netlify: **Add new site** → **Import from Git** → pick the repo
3. Leave build settings empty (`netlify.toml` handles everything)
4. Deploy

## Booking Form

The form uses **Netlify Forms** (free on the starter plan, up to 100 submissions/month).

After your first deploy:
1. In Netlify dashboard → **Forms** → you'll see "booking" listed
2. Click it → set up **notifications** to forward each submission to your email
3. Optional: connect Zapier to push submissions straight into Zoho Books as estimates

## Files

- `index.html` — the entire site (CSS, JS, content all inline)
- `netlify.toml` — security headers and cache rules
- `README.md` — this file

## Customising

### Replace tour images
All 14 tour images are pulled from Unsplash via direct URLs in the `activities` array (search for `img:` in `index.html`). To use your own photos:
1. Create an `images/` folder next to `index.html`
2. Drop in your tour photos (e.g., `kruger-safari.jpg`)
3. Change each `img:` URL to e.g. `"/images/kruger-safari.jpg"`

### Update prices or details
Find the `activities` array in `index.html` (near the bottom of the file). Each entry has `name`, `price`, `desc`, `duration`, etc. Edit and re-deploy.

### Update contact info
Phone and email are in the footer — search for `+27 76 209 5334` and replace if needed.

## Tech notes
- No build step — pure HTML/CSS/JS
- Google Fonts: Fraunces (display) + Manrope (body)
- Form submissions handled by Netlify Forms
- Fully responsive (mobile, tablet, desktop)
- Lighthouse-friendly: lazy-loaded images, semantic HTML, accessible forms

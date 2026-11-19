# Guest safari photo pages

Makes a branded African Sky Villas page for one guest's safari photos, plus a
ready-to-paste WhatsApp message and email.

```
python3 tools/guest-photos/make_gallery.py \
  --guest "Patricia Davis" --date 2026-11-16 --safari "Safári no Kruger" \
  --photos /path/to/photos --out photos --lang pt --phone 5531999417129
```

- `--lang`: `en` or `pt` (Brazilian Portuguese). Wording lives in `texts.py`.
- `--phone`: guest's WhatsApp number, digits only with country code. Adds a one-tap
  WhatsApp link to the message.
- `--donate-url`: Tap2Protect's donation page, once one exists. Until then the
  Tap2Protect button opens a WhatsApp chat with us; we never collect donations.
- The first photo (by file name) is the big photo at the top. Name it `00_...` to choose it.
- Output: `photos/<guest>-<random>/` with `index.html`, `photos/`, `thumbs/`, and
  `message.txt` (keep `message.txt` out of the site; it is for you to send).

Pages live under `/photos/`. They are hidden from search engines (`robots.txt` and an
`X-Robots-Tag` header in `netlify.toml`), and each guest folder is removed after 30 days.
"Download all" builds the zip in the guest's browser with `photos/jszip.min.js`
(JSZip 3.10.1, MIT licence).

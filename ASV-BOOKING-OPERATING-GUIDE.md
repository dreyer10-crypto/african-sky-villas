# African Sky Villas — Booking & Payment Operating Guide

**System:** Option 2 — Auto-invoice (Zoho Books via chat) + manual iKhokha pay link
**Status:** Live and proven (28 May 2026)
**Owner:** Dreyer Hoffman

---

## The system in one picture

```
1. Booking.com reservation
        ↓
2. You tap the guest's wa_link from the Google Sheet
   → guest gets a personalised activities link
        ↓
3. Guest picks tours on the site → submits
        ↓
4. Booking arrives in your WhatsApp + email   (with all details + ref)
        ↓
5. You ask Claude to invoice it
   → Claude creates a Zoho Books invoice (tour + 3.5% fee) as a DRAFT
        ↓
6. You review the draft, then create an iKhokha pay link (iKhokha app, ~30 sec)
        ↓
7. You send the guest the invoice + pay link
        ↓
8. Guest pays → you mark the Zoho invoice as paid
```

Steps 1–4 are fully built into the site. Step 5 is done via chat with Claude. Steps 6–8 are your manual actions (a few minutes per booking).

---

## Key reference details

| Thing | Value |
|---|---|
| Live site | https://african-skyvillas-activities.netlify.app/ |
| GitHub repo | github.com/dreyer10-crypto/african-sky-villas |
| Google Sheet | "ASV_Arrivals_WITH_LINKS" (in your Drive) |
| Zoho Books org | African Sky (Pty) Ltd |
| Zoho org_id | 888790812 |
| Business WhatsApp | +27 76 209 5334 |
| Reservations email | reservations@africanskyvillas.com |
| VAT | Not registered — no VAT on invoices |
| Transaction fee | 3.5% of activity subtotal, added as a separate line item |

---

## How to get an invoice created (Step 5)

In a chat with Claude, say something like:

> "Invoice this booking: [Guest name], [activity + number of guests], booking ref [ref]."

Example:
> "Invoice Giovanni Sighinolfi — Panorama Day Tour for 4 guests, ref 5975543596"

Claude will:
1. Look up the activity price
2. Calculate subtotal (price × guests)
3. Add the 3.5% transaction fee as a separate line
4. Create the invoice in Zoho Books as a **draft** (nothing sent automatically)
5. Give you the invoice number + total to review

You then open Zoho Books, check the draft, and send it.

---

## Activity price reference (per person, ZAR)

| Activity | Price | Category |
|---|---|---|
| CF Moto Sunset Drive | R500 | safari |
| Thermal Night Drive | R750 | safari |
| Komati Sunset Cruise | R995 | river |
| Komati Tiger Fishing — Half Day | R1,150 | river |
| Komati Tiger Fishing — Full Day | R1,450 | river |
| Airport Transfer | R1,700 | transfer |
| Kruger Sunrise Safari | R1,775 | safari |
| Kruger Full-Day Safari | R1,875 | safari |
| Chimp Eden & Caves | R2,500 | day-tour |
| Eswatini Cultural Day | R2,750 | day-tour |
| Bush Braai Experience | R2,795 | safari |
| Hlane Royal Safari | R2,950 | day-tour |
| Panorama Day Tour | R3,000 | day-tour |
| Maputo Day Tour | R3,050 | day-tour |

(Prices live in the site's `activities` array — update there if they change, then push to GitHub.)

### Fee calculation example
- Panorama Day Tour × 2 guests = R6,000
- 3.5% transaction fee = R210
- **Invoice total = R6,210**

---

## How the iKhokha pay link works (Step 6)

iKhokha is **not** integrated with Zoho or Zapier, so this step is manual:

1. Open the **iKhokha app** (or dashboard.ikhokha.com)
2. Payment options → **iK Pay Link** → **Request a Quick Payment**
   (or create an **iK Invoice**, which auto-embeds a pay link)
3. Enter the amount (matching the Zoho invoice total, e.g. R6,210)
4. Description: guest name + booking ref
5. **Create Link** → copy / share it
6. Send to the guest via WhatsApp alongside (or instead of) the Zoho invoice

Notes:
- iKhokha rate: 2.85% (excl VAT) per online transaction — note this differs from the 3.5% you charge the guest; the gap covers the fee
- Max R80,000 per link (activity bookings are well under)
- Guest pays on iKhokha's secure page — you never handle card details

---

## How to mark an invoice paid (Step 8)

When iKhokha shows the payment received:
- In Zoho Books: open the invoice → **Record Payment** → enter amount + date → Save
- Or ask Claude to mark invoice [number] as paid

---

## Weekly routine

1. **Booking.com Extranet** → Reservations → export CSV of upcoming arrivals
2. Paste new rows into the **ASV_Arrivals_WITH_LINKS** Google Sheet (matching columns)
3. Ask Claude to build the activities_url + wa_link for the new rows (one-off, via chat), OR build them yourself from the pattern
4. Tap each guest's **wa_link** → WhatsApp opens pre-typed → send
5. As bookings come back (WhatsApp + email), ask Claude to invoice each one
6. Review drafts in Zoho, create iKhokha links, send to guests
7. Record payments as they arrive

---

## Known limitations & honest notes

1. **Not fully hands-off.** Invoicing runs when you're in a chat with Claude; iKhokha links are manual. For a few bookings a week this is fine. For high volume, see "Future upgrades."
2. **Free Zapier plan** only allows single-step Zaps, so the standing auto-Zap isn't available. The chat-based approach replaces it.
3. **iKhokha has no API integration** in Zapier or Zoho. The only way to fully automate it is a custom Node service (see workflow doc, "Approach C / Option 3").
4. **Renate Wenghöfer** — phone flagged REVIEW-invalid. Confirm her number before messaging.
5. **The two CATTEAU rows** share a phone number — check before messaging both.
6. **Past arrivals** — some rows have arrival dates already passed; focus messaging on upcoming arrivals.

---

## Future upgrade paths (when volume justifies)

**Path 1 — Full auto with a Zoho-supported gateway**
Paid Zapier + PayPal/Stripe (instead of iKhokha) → invoice + pay button + auto-reconcile, fully hands-off. Trade-off: higher fees (~3–4%), not iKhokha.

**Path 2 — Custom iKhokha automation (Approach C)**
A hosted Node service signs iKhokha API requests + listens for payment webhooks → keeps iKhokha, fully automated. Trade-off: real dev project, ~$5–7/mo hosting, sandbox testing, multi-session build.

Decide based on actual booking volume after running Option 2 for a while.

---

## Test artifacts to clean up

- **Zoho invoice INV-000203** (Dreyer Hoffman, R6,210) — this was a system test. Void or delete it in Zoho Books once you've confirmed the setup looks right.
- **Contact "Dreyer Hoffman"** in Zoho — created during testing; keep or remove as you prefer.

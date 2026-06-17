# Films — marketing site + legal pages (GitHub Pages)

Public site for the **Films** iOS app: a marketing landing page plus the Privacy Policy,
Terms of Use, and Support pages. Hosted free on GitHub Pages.

**Live:** https://biswaskhatiwada.github.io/films-legal/

| File | Purpose |
|---|---|
| `index.html` | Marketing landing page (hero, the App Store ad panels, features, FAQ, waitlist) |
| `privacy.html` | Privacy Policy (GDPR + US/CCPA, retention, complaints) |
| `terms.html` | Terms of Use / EULA (subscriptions, content, acceptable use, DMCA/IP) |
| `support.html` | Support / FAQ + account deletion + contact |
| `shots/` | App Store ad panels (`panel-1..8.png`) + clean app-screen crops (`screen-*.png`) |

The app's paywall links to `terms.html` and `privacy.html` here (see
`Camera/UI/PaywallView.swift`).

## ⚠️ Before you launch — required edits

1. **Replace the support email.** Every page uses the placeholder
   **`support@example.com`**. Swap it for a real inbox you check (a reviewer or user may email
   it). One pass replaces them all:
   ```sh
   # from the repo root, on macOS:
   LC_ALL=C grep -rl 'support@example.com' . | xargs sed -i '' 's/support@example.com/YOUR_REAL_EMAIL/g'
   ```
2. **Wire the waitlist (optional).** The "Notify me" form currently confirms client-side and
   stores nothing. To collect emails, set `WAITLIST_URL` in `index.html` to a real endpoint
   (e.g. Formspree, or a Convex HTTP action like the SPARK site uses).
3. **Have the legal pages reviewed.** These are solid drafts, not legal advice — have a
   professional review them, and confirm the governing-law/jurisdiction and age (13+) match your
   final plan before relying on them.

## Switching to a custom domain later (one-pass checklist)

Everything is set up so that buying a domain is a clean swap. The **paths never change**
(`/privacy.html`, `/terms.html`, `/support.html`, `/join.html`) — only the host does. Today the
host is `biswaskhatiwada.github.io/films-legal`; after the swap it becomes `https://yourdomain`.

> The **app repo** holds the master one-pass swap doc (`AppStore/DOMAIN_SETUP.md`) — a single
> find/replace of `https://biswaskhatiwada.github.io/films-legal` → your new base across the app +
> App Store metadata. The table below is the **website-side** companion (this repo + the one
> absolute URL + the CNAME step).

**Every place a URL lives (the complete list):**

| # | Location | What to change |
|---|---|---|
| 1 | **This repo → GitHub Pages** | Add the domain (step A below). Internal page links are all *relative*, so they keep working untouched. |
| 2 | `index.html` → `<meta property="og:image">` | The only **absolute** URL on the site — repoint to `https://yourdomain/shots/panel-1.png`. |
| 3 | **App** `Camera/UI/PaywallView.swift` | The two legal links (`termsURL`, `privacyURL`). *Recommended:* centralize them into one `legalBase` constant (like SPARK's `SparkLegal.legalBase`) so this becomes a one-line change. |
| 4 | **App** in-film invite (when wired) | The web invite link `…/join.html?code=` — also use the same `legalBase`. The `films://join/CODE` deep-link scheme is **not** domain-based, so it's unaffected. |
| 5 | **App Store Connect** (manual fields) | Privacy Policy URL · Support URL · Marketing URL. Changing these is *metadata only* — **no new build review needed.** |
| 6 | Docs (`AppStore/SUBMISSION_CHECKLIST.md`, `APP_STORE_LISTING.md`, `LAUNCH_CHECKLIST.md`) | Cosmetic — update the URLs when convenient. |

**Steps:**

**A. Point the domain here.** Buy the domain, then either add a `CNAME` file to this repo's root
containing just the domain (e.g. `films.app`) or set Settings → Pages → Custom domain. Configure
DNS (apex → GitHub Pages A records; or a subdomain `CNAME` → `biswaskhatiwada.github.io`). GitHub
auto-provisions HTTPS. *(Don't add the CNAME until the domain exists — a placeholder breaks Pages.)*

**B.** Update items **2–5** above to the new host. Re-archive the app only so the in-app paywall
links pick up the new URLs (the ASC metadata URLs in #5 don't need a rebuild).

**Bonus once you own a domain:** you can also enable real **Universal Links** (tappable `https://`
invite links that open the app directly) by hosting an `apple-app-site-association` file at the
domain root + adding the Associated Domains entitlement — not possible on the shared
`github.io` path today, which is why invites use the `films://` scheme for now.

## Updating the screenshots
The images in `shots/` are generated from the App Store kit in the app repo
(`AppStore/exports/shot-1..8.png`). Re-crop the clean screens with the helper used to build this
site (phone geometry comes from `AppStore/build.py`).

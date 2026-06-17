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
| `blog/` | **The Journal** — generated static blog: `index.html`, 25 article pages, `art/*.svg` covers, `journal.css`, `journal.js`. Served as-is. |
| `journal-src/` | Authoring tooling for the blog (**not** served). `build.py` renders everything under `blog/`. |

The app's paywall links to `terms.html` and `privacy.html` here (see
`Camera/UI/PaywallView.swift`).

## The Journal (blog)

`/blog/` is **The Journal** — a 25-post editorial blog in the site's dark-brass film
aesthetic, each post with a custom generative SVG cover. The HTML under `blog/` is plain
static output (no build step runs on GitHub Pages); it's generated locally from the tooling
in `journal-src/`:

- `journal-src/posts.py` — manifest: title, slug, category, date, read time, dek, excerpt,
  and cover motif for each of the 25 posts (display order; entry `[0]` is the featured post).
- `journal-src/content/<slug>.html` — the long-form body of each article (HTML fragments;
  `{{divider}}` is replaced by a film-strip divider at build time).
- `journal-src/covers.py` — the generative SVG cover-art system (film-strip, aperture,
  light-leak, develop-tray, swatch, camera, halation, clock, envelope, route, printer, … motifs).
- `journal-src/build.py` — wraps fragments in the shared article template, builds the
  category-filterable index, and renders all 25 covers.

**Regenerate after any edit:**
```sh
python3 journal-src/build.py   # writes blog/index.html, blog/<slug>.html, blog/art/<slug>.svg
```

To add a post: append an entry to `posts.py`, drop a body fragment in `content/`, rerun
`build.py`. The Journal is linked from the main nav, a "From the Journal" teaser on
`index.html`, and the footer of every page.

## ⚠️ Before you launch — required edits

1. **Replace the support email.** Every page uses the placeholder
   **`support@getfilmsera.cam`**. Swap it for a real inbox you check (a reviewer or user may email
   it). One pass replaces them all:
   ```sh
   # from the repo root, on macOS:
   LC_ALL=C grep -rl 'support@getfilmsera.cam' . | xargs sed -i '' 's/support@getfilmsera.cam/YOUR_REAL_EMAIL/g'
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
| 2 | `index.html` → `<meta property="og:image">` **and** `journal-src/build.py` → `BASE` | The site's **absolute** URLs. Repoint index's `og:image` to `https://yourdomain/shots/panel-1.png`; set `BASE` in `build.py` to the new host and rerun `python3 journal-src/build.py` (the blog's `og:image`/`og:url` tags use it). |
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

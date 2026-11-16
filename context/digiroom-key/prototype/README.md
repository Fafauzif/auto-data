# Digiroom KEY — verified prototype handoff

**16 November 2026 · Responsive build and proposal evidence**

This handoff records what was implemented after the [original build brief](../digiroom-key-megaprompt.md). Keep the [solution overview](../digiroom-key-solution-overview.md), [decision record](../DECISION_RECORD.md) and [research-to-feature index](../EVIDENCE_TO_FEATURE.md) alongside it. The current research argument and pilot evidence remain in the [integrated report](../../../reports/INTEGRATED_REPORT.md) and [interview synthesis](../../../analysis/interviews/INTERVIEW_SYNTHESIS.md).

## What the demo does

| Journey | Customer experience | Handoffs and exceptions shown |
|---|---|---|
| **K · Know Your Fit** | The household explores the live WebGL Innova Zenix and bZ4X, checks garage clearance, configures seats, estimates weekly driving costs and saves a visit card. It requests a standard drive or a 48-Hour Life Test. | The sales adviser checks the demonstrator calendar, confirms the drive or proposes another slot, records pickup and accepts the return. The household saves its results. The adviser issues a dated quote, the household buyer accepts it, and the adviser records the financing decision, order and delivery. The demo covers a blocked slot, an ineligible branch and 2D recovery. |
| **E · Easy Service** | The customer compares dealer-only and eligible OtoXpert access, inspects an origin and chooses an eligible offer. The illustrated Avanza oil service shows the installed price. Diagnostic, hybrid and qualifying Home Service variants are available. | The workshop adviser reserves parts and confirms a slot, checks the vehicle in, writes a versioned estimate and marks the vehicle ready. An authorized payer can approve the current version or retain the original scope. The adviser issues a receipt at handover. A stale link prompts the payer to reopen the current version. |
| **Y · Your Next Toyota** | The owner compares a Yaris Cross Hybrid market estimate with an inspected buy offer. The upgrade terms show the loan payoff, fees, equity, cash due and instalments. The owner can purchase without a trade-in. | The upgrade adviser records inspection evidence, confirms financing and reserves a unit. The owner accepts current terms. The adviser records settlement and both handovers. Expired or withdrawn terms, a recorded deposit refund and a new appraisal path are shown. |

The four workspaces are **Customer, Sales adviser, Workshop adviser and Upgrade adviser**. Buyer and payer views model separate decisions within the sample account. **My Requests**, **Vehicle Records** and transaction history connect the journeys. A confirmed reset clears the KEY walkthrough state. The original showroom, xEV catalogue, vehicle comparison, ownership planners and local visit brief remain accessible.

### Responsive changes

- The language and workspace controls reflow on narrow screens. Long selector labels stay within their fields, including in WebKit.
- Branch & Visit stays visible on phones. The showroom controls and ownership tabs reflow, visit date inputs fit narrow dialogs, and forms have larger touch targets.
- A mobile **Jump to service offers** control takes the customer to the booking section without requiring them to scroll past the atlas.

### Evidence boundaries

Figures for vehicles, slots, finance, prices, buying offers and completed outcomes are sample demo records. KEY keeps one active case per journey in the browser. The payer link checks the estimate version within the same profile. Live dealer appointments, inventory, payments, financing, appraisal, cross-device identity and messaging require separate integrations. The visit flow can show a draft for WhatsApp. The archived examples use the in-app preview.

The oil-access study reports modeled origins more than five minutes behind the collected comparator. Across **284 paired origins**, the tail count falls from **39 to 20** when eligible Auto2000-operated OtoXpert is included. The market transitions are Bandung **17 → 14** of 78, Surabaya **10 → 6** of 59, Medan **3 → 0** of 78 and Palembang **9 → 0** of 69. This is modeled driving geometry for the defined job. Customer demand, current traffic and actual workshop volume are separate measures. [Geography report](../../../analysis/geography/GEOGRAPHY_INTEGRATION_REPORT.md)

## Proposal assets

Start with the [proposal shortlist](screenshots/README.md) and [caption index](screenshots/screenshot-index.csv). There are **169 English PNGs covering 120 numbered screens and states**. The pack includes 115 desktop viewport shots, 16 mobile viewport shots and 38 detail or full-page companions.

- For a slide that needs the two live-rendered vehicles, start with the [showroom close-up](screenshots/01-know-your-fit/K-01__customer__zenix-and-bz4x-3d-vehicles-close-up__desktop-detail__en.png). The [garage close-up](screenshots/01-know-your-fit/K-03__customer__zenix-garage-model-close-up__desktop-detail__en.png) and cabin details sit in the same folder.
- The atlas comparison includes both network layers for all four markets. Keep the on-screen attribution and the modeled-origin qualifier when using the images.
- For fresh English captures after a future app change, use the [screenshot capture prompt](SCREENSHOT_CAPTURE_PROMPT.md). The captured QR and share examples contain local preview links.

## Rebuild and verify the demo

The [40-file responsive app overlay](app-overlay/) is the source update, arranged at paths relative to the **application** root. It supersedes the earlier KEY prototype overlay. The base is the user-supplied [Auto2000-Digiroom-Demo](https://github.com/Fafauzif/Auto2000-Digiroom-Demo) source archive for commit `4610b8fa338fb6b00387d0b2bd8a878152d8e739`. Start from that source or from the earlier KEY overlay applied to it. The base provides the original 3D models, fonts and dependency lockfile.

Copy the **contents** of `prototype/app-overlay/` into the Auto2000-Digiroom-Demo root and replace matching files, including the dotfiles in the overlay. No app files need deletion. From the app root with Node.js 22.12 or newer:

```sh
npm ci
npm run build
npm run preview
```

See the [app README](app-overlay/README.md) for the judge walkthrough and the [app handoff](app-overlay/docs/KEY.md) for geographic provenance and the test commands. The original Vercel link is [auto2000demo.vercel.app](https://auto2000demo.vercel.app/). The screenshots and QA in this package came from the local production build. The Vercel deployment version was outside this update’s verification.

### Verification recorded for this build

- The overlay built after extraction over the clean app base. Type checking, formatting and 72 unit tests passed.
- Responsive checks passed at 17 viewport sizes across 12 routes in Chromium, Firefox and WebKit. The three customer/adviser journeys also passed in a 440 px touch-emulated viewport. Physical device and hardware frame-rate testing remain outside these results.
- The original showroom suite passed 76 browser checks on the responsive work before the final WebKit layout refinements. The final responsive suites and KEY touch walkthrough were then rerun after those refinements.
- Live tiles were unavailable in the original browser environment. Blocked-tile fallback, access counts, map handoffs and capture of both network layers were exercised using the bundled atlas.
- The PNG links, caption CSV, source provenance and exact update bytes are recorded in [release.json](release.json) and [FILES.sha256](FILES.sha256).

## Apply this context update to auto-data

Extract the context ZIP directly into the **auto-data repository root** and choose **Replace All**. The two replaced files are `context/START_NEXT_CHAT.txt` and `context/digiroom-key/START_HERE.md`. The first retains the earlier continuation below the new pointer. The second is preserved verbatim as [START_HERE.pre-prototype.md](../START_HERE.pre-prototype.md). No files need deletion.

This context update leaves research sources, evidence files, analyses, decision history and the historical release manifest in place. The base release verifier already flags the prior edited continuation note. The update retains that historical distinction and adds a separate inventory. From the auto-data repository root, run `sha256sum -c context/digiroom-key/prototype/FILES.sha256` to check the update contents.

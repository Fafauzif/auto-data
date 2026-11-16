# Auto2000 Digiroom KEY

**Know your fit. Book your service. Find your next Toyota.**

Digiroom KEY follows a first-time Auto2000 shopper, an owner booking a workshop job, and a returning customer upgrading their Toyota. Use the workspace switch to act as the customer, sales adviser, workshop adviser or upgrade adviser. Their decisions update the same records.

## Run

Use Node.js 22.12 or later. Extract `digiroom-key-responsive-overlay.zip` into the repository root, next to `package.json`, and choose **Replace All**. This archive also applies over the earlier KEY overlay. No source files need to be deleted.

```sh
npm ci
npm run dev
```

Open the local URL printed by Vite. To check the production bundle, run `npm run build` followed by `npm run preview`. The production output is `dist/`. The application requires no environment variables.

## Judge walkthrough

1. **Know Your Fit.** Open the 3D Life Test. Try the Zenix garage, family and driving-week controls. Save the visit card and request a 48-Hour Life Test. Switch to Sales adviser to confirm, record pickup and accept the return once the customer logs the household results. Issue a dated quote. Accept it as the household buyer, then record the lender decision, order and delivery in Sales.
2. **Easy Service.** Open Bandung. Switch from dealer workshops to the eligible OtoXpert network and inspect a modeled origin. Request an Avanza oil-and-filter service. In Workshop, confirm parts and slot, check in the vehicle and issue an additional-work estimate. Open the authorized payer view from Customer, approve the version, then close and download the receipt after Workshop marks the car ready and records collection.
3. **Your Next Toyota.** Request an inspection for the Yaris Cross Hybrid. In Upgrade, issue the inspected buy offer, record the official payoff and fees, and confirm the replacement unit and lender conditions. Accept the dated terms as the owner. In Upgrade, record settlement and both handovers.

**My requests** and **Vehicle records** show the outcomes. **Reset walkthrough** restores the starting accounts after confirmation. [Implementation and verification](docs/KEY.md)

## Existing showroom

The 3D studio retains its two articulated vehicles, interactive 2D plan, xEV catalogue, purchase and ownership planner, branch selection and visit brief. The existing QR and download export the selected visit. The optional Tasia link opens a WhatsApp draft only when chosen. Keep personal data out of links and download copies intended for projection.

Dated catalogue and pricing references, original vehicle geometry, and financial and technical assumptions are documented in [Sources](docs/SOURCES.md), [Catalogue](docs/CATALOGUE.md), [Vehicle assets](docs/ASSETS.md), [Ownership](docs/OWNERSHIP.md) and [Visit](docs/VISIT.md).

## Checks

```sh
npm test
npm run typecheck
npm run format:check
npm run build
npx playwright install chromium --only-shell
npm run test:browser
npm run test:browser:key
npm run test:browser:responsive
```

Browser reports and screenshots are local. `PLAYWRIGHT_EXECUTABLE_PATH` can select a compatible installed Chromium. The responsive suite checks phone, tablet, landscape, and desktop dimensions. Install Playwright Firefox or WebKit to run it with `QA_ENGINE=firefox` or `QA_ENGINE=webkit`. Run `QA_MOBILE=1 npm run test:browser:key` to exercise the entire KEY walkthrough in a 440 px touch viewport. The existing showroom hardware frame-rate target requires testing on that device.

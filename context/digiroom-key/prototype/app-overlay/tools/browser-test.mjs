import http from "node:http";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { chromium } from "@playwright/test";
const root = path.resolve("dist"),
  out = path.resolve(process.env.QA_OUTPUT || "qa-browser-v3");
await mkdir(out, { recursive: true });
const mime = {
  ".html": "text/html",
  ".js": "application/javascript",
  ".css": "text/css",
  ".glb": "model/gltf-binary",
  ".woff2": "font/woff2",
  ".svg": "image/svg+xml",
  ".json": "application/json",
};
const server = http.createServer(async (req, res) => {
  try {
    let p = path.resolve(
      root,
      "." + decodeURIComponent(new URL(req.url, "http://localhost").pathname),
    );
    if (!p.startsWith(root + path.sep) && p !== root) throw Error("outside");
    if (p === root) p = path.join(root, "index.html");
    let buf;
    try {
      buf = await readFile(p);
    } catch {
      if (path.extname(p)) throw Error("notfound");
      p = path.join(root, "index.html");
      buf = await readFile(p);
    }
    res.setHeader(
      "Content-Type",
      mime[path.extname(p)] || "application/octet-stream",
    );
    res.end(buf);
  } catch {
    res.statusCode = 404;
    res.end("Not found");
  }
});
await new Promise((r) => server.listen(38465, "127.0.0.1", r));
const browser = await chromium.launch({
  executablePath: process.env.PLAYWRIGHT_EXECUTABLE_PATH || undefined,
  args: ["--no-sandbox", "--enable-unsafe-swiftshader"],
});
const page = await browser.newPage({
  viewport: { width: 1920, height: 1080 },
});
const errors = [],
  requests = [],
  checks = [],
  networkLimitations = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("response", (r) => {
  if (r.status() >= 400) requests.push({ url: r.url(), status: r.status() });
});
page.setDefaultTimeout(12000);
const check = (name, ok) => {
  checks.push({ name, passed: !!ok });
  if (!ok) throw Error("Check failed: " + name);
};
const shot = async (name) => {
  await page.waitForTimeout(400);
  await page.screenshot({
    path: path.join(out, name + ".png"),
    fullPage: true,
  });
};
try {
  await page.addInitScript(() =>
    Object.defineProperty(navigator, "geolocation", {
      configurable: true,
      value: {
        getCurrentPosition: (_success, error) =>
          queueMicrotask(() =>
            error({ code: 1, message: "Denied for failure-path verification" }),
          ),
      },
    }),
  );
  await page.goto("http://127.0.0.1:38465/#studio");
  await page.locator("canvas[data-scene-ready=true]").waitFor();
  await page.waitForTimeout(1600);
  check(
    "English default",
    (await page.locator("html").getAttribute("lang")) === "en",
  );
  check(
    "WebGL scene ready",
    (await page.locator("canvas[data-scene-ready=true]").count()) === 1,
  );
  check(
    "Compact camera controls",
    await page
      .locator(".camera-controls")
      .evaluate((el) => el.getBoundingClientRect().height < 60),
  );
  await shot("01-showroom-desktop");
  await page.getByRole("button", { name: "Your garage", exact: true }).click();
  check(
    "Door constraint visible even with door closed",
    (await page
      .getByText("It fits. The door needs more space.", { exact: true })
      .count()) === 1,
  );
  await page
    .getByRole("button", { name: "Open driver’s door", exact: true })
    .click();
  await page
    .getByRole("spinbutton", { name: "Garage width", exact: true })
    .fill("4");
  await page
    .getByRole("spinbutton", { name: "Garage depth", exact: true })
    .fill("7");
  await page
    .getByRole("spinbutton", { name: "Garage depth", exact: true })
    .press("Tab");
  check(
    "All clearance envelopes update",
    (await page
      .getByText("Body, door and tailgate clear this layout.", { exact: true })
      .count()) === 1,
  );
  await page
    .getByRole("button", { name: "Add a clearance check", exact: true })
    .click();
  await shot("02-garage");
  await page.getByRole("button", { name: "Your family", exact: true }).click();
  await page
    .getByRole("button", { name: "Bring a folded stroller", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Include a child seat", exact: true })
    .click();
  await page
    .getByRole("button", { name: /Toyota bZ4X Battery electric/ })
    .click();
  await page
    .getByRole("spinbutton", { name: "People travelling", exact: true })
    .fill("7");
  check(
    "Passenger conflict retained",
    (await page
      .getByText("This arrangement has too few seats.", { exact: true })
      .count()) === 1,
  );
  await page.getByTestId("child-seat-marker").waitFor();
  check(
    "Child-seat marker shown in 3D",
    await page.getByTestId("child-seat-marker").isVisible(),
  );
  await page
    .getByRole("spinbutton", { name: "People travelling", exact: true })
    .fill("2");
  check(
    "Child seat remains in row two with two passengers",
    (await page.getByTestId("child-seat-marker").innerText()).includes("Row 2"),
  );
  await page
    .getByRole("button", { name: "Include a child seat", exact: true })
    .click();
  check(
    "Child-seat marker disappears when disabled",
    (await page.getByTestId("child-seat-marker").count()) === 0,
  );
  await page
    .getByRole("button", { name: "Include a child seat", exact: true })
    .click();
  await page.getByRole("button", { name: "2D plan", exact: true }).click();
  check(
    "Child-seat marker also present in 2D alternative",
    await page.getByTestId("child-seat-2d").isVisible(),
  );
  await page.getByRole("button", { name: "3D view", exact: true }).click();
  await page.locator("canvas[data-scene-ready=true]").waitFor();
  await shot("03-family-child-seat");
  await page.getByRole("button", { name: "Indonesia", exact: true }).click();
  check(
    "Language switch changes document language",
    (await page.locator("html").getAttribute("lang")) === "id",
  );
  check(
    "Family controls translate without resetting child seat",
    (await page
      .getByRole("button", { name: "Sertakan kursi anak", exact: true })
      .getAttribute("aria-pressed")) === "true",
  );
  check(
    "3D child marker translates",
    (await page.getByTestId("child-seat-marker").innerText()).includes(
      "Baris 2",
    ),
  );
  await shot("03b-family-indonesian");
  await page.reload();
  check(
    "Indonesian preference survives reload",
    (await page.locator("html").getAttribute("lang")) === "id",
  );
  await page
    .getByRole("button", { name: "Jelajahi semua xEV", exact: true })
    .click();
  check(
    "Catalogue heading translates",
    (await page
      .getByRole("heading", {
        name: "Bandingkan model Toyota xEV",
        exact: true,
      })
      .count()) === 1,
  );
  await page
    .getByRole("button", { name: "Pembelian & kepemilikan", exact: true })
    .click();
  check(
    "Ownership controls translate",
    (await page
      .getByRole("button", { name: "DP & cicilan", exact: true })
      .count()) === 1,
  );
  await shot("03c-ownership-indonesian");
  await page
    .getByRole("button", { name: "Cabang & kunjungan", exact: true })
    .click();
  check(
    "Visit modal translates",
    (await page
      .getByRole("heading", {
        name: "Pilih cabang. Siapkan test drive Anda.",
        exact: true,
      })
      .count()) === 1,
  );
  check(
    "BEV visit retains electricity in Indonesian",
    (await page.locator(".visit-brief-preview pre").innerText()).includes(
      "Listrik per kWh",
    ),
  );
  await page.getByLabel("Hari pilihan", { exact: true }).fill("2099-01-01");
  await page
    .getByRole("button", { name: "Buat ringkasan kunjungan", exact: true })
    .click();
  const waId = new URL(
    await page
      .getByRole("link", {
        name: "Kirim Ringkasan ke WhatsApp Auto2000 (Tasia)",
        exact: true,
      })
      .getAttribute("href"),
  );
  check(
    "Indonesian WhatsApp draft preserves BEV and translated checks",
    waId.searchParams.get("text").includes("Listrik per kWh") &&
      waId.searchParams.get("text").includes("Garasi:"),
  );
  await shot("03d-visit-indonesian");
  await page
    .getByRole("button", { name: "Tutup ringkasan kunjungan", exact: true })
    .click();
  await page.getByRole("button", { name: "EN", exact: true }).click();
  await page
    .getByRole("button", { name: "Interactive showroom", exact: true })
    .click();
  await page.getByRole("button", { name: "Your week", exact: true }).click();
  await page.getByRole("button", { name: "Scene 2", exact: true }).click();
  check(
    "BEV energy basis visible",
    (await page
      .getByText("12.13 kWh/100 km + 10% charging overhead", { exact: true })
      .count()) === 1,
  );
  await shot("04-electric-week");
  await page.getByRole("button", { name: "Save", exact: true }).click();
  await page.reload();
  check(
    "Saved vehicle survives reload",
    (await page
      .getByRole("button", { name: /Toyota bZ4X Battery electric/ })
      .getAttribute("aria-pressed")) === "true",
  );
  await page
    .getByRole("button", { name: "Explore all xEV", exact: true })
    .click();
  check(
    "Full catalogue family count",
    (await page.locator(".catalogue-item").count()) === 14,
  );
  await page
    .getByRole("textbox", { name: "Search xEV models", exact: true })
    .fill("nonexistentmodel");
  check(
    "Catalogue empty state",
    (await page
      .getByRole("heading", { name: "No matching models", exact: true })
      .count()) === 1,
  );
  await page
    .getByRole("button", { name: "Clear model search", exact: true })
    .click();
  await page.getByRole("button", { name: "PHEV", exact: true }).click();
  check(
    "PHEV no invented inventory",
    (await page
      .getByRole("heading", {
        name: "No current PHEV product listing",
        exact: true,
      })
      .count()) === 1,
  );
  await page
    .getByRole("button", { name: "Reset filters", exact: true })
    .click();
  const items = page.locator(".catalogue-item");
  await items
    .nth(0)
    .getByRole("checkbox", { name: "Compare model", exact: true })
    .check();
  await items
    .nth(1)
    .getByRole("checkbox", { name: "Compare model", exact: true })
    .check();
  await page
    .getByRole("button", { name: "Compare models", exact: true })
    .click();
  check(
    "Two-model comparison shown",
    (await page
      .getByRole("heading", { name: "Model reference comparison", exact: true })
      .count()) === 1,
  );
  check(
    "Third comparison selection disabled",
    await items
      .nth(2)
      .getByRole("checkbox", { name: "Compare model", exact: true })
      .isDisabled(),
  );
  await page
    .getByRole("button", {
      name: "View Kijang Innova Zenix details",
      exact: true,
    })
    .click();
  await page
    .getByRole("combobox", { name: "Product configuration", exact: true })
    .selectOption("q-hv");
  check(
    "Selected grade reference updates",
    (await page.locator(".catalogue-detail-price strong").innerText()) ===
      "Rp 618.400.000",
  );
  await shot("05-catalogue");
  await page
    .getByRole("button", { name: "Calculate this configuration", exact: true })
    .click();
  check(
    "Selected configuration reaches ownership",
    (await page
      .getByRole("heading", {
        name: "Calculate your Toyota ownership costs.",
        exact: true,
      })
      .count()) === 1 &&
      (await page.locator(".own-header").innerText()).includes(
        "Q HV Modellista",
      ),
  );
  const monthly = await page.locator(".own-monthly").innerText();
  await page.getByRole("slider", { name: /Down payment/ }).fill("40");
  check(
    "DP changes monthly repayment",
    (await page.locator(".own-monthly").innerText()) !== monthly,
  );
  const monthly2 = await page.locator(".own-monthly").innerText();
  await page.getByRole("slider", { name: /Loan term/ }).fill("3");
  check(
    "Tenor changes monthly repayment",
    (await page.locator(".own-monthly").innerText()) !== monthly2,
  );
  await page
    .getByRole("combobox", { name: /^Registration region/ })
    .selectOption("Bandung");
  check(
    "Unavailable regional OTR does not fabricate a quote",
    (await page.locator(".own-monthly").innerText()) === "Enter OTR",
  );
  await page
    .getByRole("spinbutton", { name: /^Vehicle OTR/ })
    .fill("620000000");
  check(
    "User regional OTR produces an illustration",
    (await page.locator(".own-monthly").innerText()) !== "Enter OTR",
  );
  await page.getByText("Apply a trade-in estimate", { exact: true }).click();
  await page
    .getByRole("spinbutton", { name: /^Estimated current-car value/ })
    .fill("100000000");
  await page
    .getByRole("spinbutton", { name: /^Outstanding settlement/ })
    .fill("125000000");
  check(
    "Negative equity is explained",
    await page
      .locator(".own-caution")
      .innerText()
      .then((t) => t.includes("Settlement exceeds")),
  );
  await shot("06-finance");
  await page
    .getByRole("button", { name: "Five-year costs", exact: true })
    .click();
  check(
    "TCO includes depreciation and no second principal",
    (await page
      .getByText("Depreciation after resale", { exact: true })
      .count()) === 1 &&
      (await page.getByText("Loan interest", { exact: true }).count()) === 1,
  );
  await shot("07-five-year-costs");
  await page
    .getByRole("button", { name: "Service & benefits", exact: true })
    .click();
  check(
    "Service benefits separate coverage from wear",
    (await page
      .getByRole("heading", { name: "Included scheduled service", exact: true })
      .count()) === 1 &&
      (await page.getByText(/Repairs, wear and optional work/).count()) === 1,
  );
  await shot("08-service-benefits");
  await page
    .getByRole("button", { name: "Branch & visit", exact: true })
    .click();
  const dialog = page.getByRole("dialog", {
    name: "Choose a branch. Prepare your test drive.",
    exact: true,
  });
  check("Named branch dialog", (await dialog.count()) === 1);
  await dialog.locator(".road-branch-marker").first().waitFor();
  check(
    "Leaflet requests the documented road-tile service",
    await dialog
      .locator(".leaflet-tile")
      .evaluateAll(
        (els) =>
          els.length > 0 &&
          els.every((el) =>
            el.src.startsWith("https://tile.openstreetmap.org/"),
          ),
      ),
  );
  await dialog.locator(".road-map:not([data-map-state=loading])").waitFor();
  const roadTilesLoaded = await dialog
    .locator(".leaflet-tile-loaded")
    .evaluateAll((els) => els.some((el) => el.naturalWidth === 256));
  if (roadTilesLoaded) check("Real road tiles loaded", true);
  else {
    networkLimitations.push(
      "Public OpenStreetMap raster tile delivery was unavailable in the test network; Leaflet pins, attribution, error recovery and the reference map were exercised.",
    );
    if (process.env.QA_REQUIRE_ROAD_TILES)
      check("Real road tiles loaded", false);
  }
  check(
    "Map attribution visible",
    await dialog.locator(".leaflet-control-attribution").isVisible(),
  );
  await dialog
    .locator('.road-branch-marker[title="Auto2000 Bekasi Timur"]')
    .click();
  check(
    "Road-map pin selects matching branch",
    (await dialog.locator(".branch-option.selected strong").innerText()) ===
      "Auto2000 Bekasi Timur",
  );
  check(
    "HEV visit checks omit electricity tariff",
    !(await dialog.locator(".visit-brief-preview pre").innerText()).includes(
      "Electricity per kWh",
    ),
  );
  await shot("08b-real-road-map");
  await dialog
    .getByRole("button", { name: "Use my location", exact: true })
    .click();
  await dialog
    .getByText(
      "Location was not available. Select Jabodetabek or Bandung manually.",
      { exact: true },
    )
    .waitFor();
  check(
    "GPS denial has manual recovery",
    (await dialog.getByRole("combobox", { name: /^Area/ }).count()) === 1,
  );
  await dialog.getByRole("combobox", { name: /^Area/ }).selectOption("Bandung");
  await dialog.getByRole("button", { name: /^2 Auto2000 Pasteur/ }).click();
  check(
    "Manual Bandung branch selection",
    (await dialog.locator(".branch-option.selected strong").innerText()) ===
      "Auto2000 Pasteur",
  );
  await dialog
    .getByRole("button", { name: "Generate visit brief", exact: true })
    .click();
  check(
    "Missing preferred date validated",
    (await dialog.getByRole("alert").count()) === 1,
  );
  await dialog.getByLabel("Preferred day", { exact: true }).fill("2099-01-01");
  await dialog
    .getByRole("button", { name: "Generate visit brief", exact: true })
    .click();
  await dialog
    .getByRole("img", {
      name: "QR code opening this saved visit brief",
      exact: true,
    })
    .waitFor();
  check(
    "Actual QR generated",
    (
      (await dialog
        .getByRole("img", {
          name: "QR code opening this saved visit brief",
          exact: true,
        })
        .getAttribute("src")) || ""
    ).startsWith("data:image/png;base64,"),
  );
  const link = await dialog
    .getByLabel("Shareable brief link", { exact: true })
    .inputValue();
  check(
    "Shareable link carries portable saved state",
    link.includes("#visit=") && link.length < 9000,
  );
  await dialog
    .getByRole("button", { name: "Preview WhatsApp handoff", exact: true })
    .click();
  check(
    "WhatsApp preview explains customer-controlled send",
    (await dialog
      .getByText(
        "Draft addressed to official Tasia. Review the message, then send it yourself in WhatsApp.",
        { exact: true },
      )
      .count()) === 1,
  );
  const wa = new URL(
    await dialog
      .getByRole("link", {
        name: "Send Brief to Auto2000 WhatsApp (Tasia)",
        exact: true,
      })
      .getAttribute("href"),
  );
  check(
    "WhatsApp draft targets official Tasia",
    wa.hostname === "wa.me" && wa.pathname === "/6282289802000",
  );
  check(
    "WhatsApp draft carries current branch, finance and saved link",
    wa.searchParams.get("text").includes("Auto2000 Pasteur") &&
      wa.searchParams.get("text").includes("40%") &&
      wa.searchParams.get("text").includes("#visit="),
  );
  check(
    "HEV WhatsApp draft omits electricity tariff",
    !/electricity per kwh|electricity Rp/i.test(wa.searchParams.get("text")),
  );
  const downloadPromise = page.waitForEvent("download");
  await dialog
    .getByRole("button", { name: "Download brief", exact: true })
    .click();
  const download = await downloadPromise;
  const briefPath = path.join(out, "downloaded-visit.txt");
  await download.saveAs(briefPath);
  const brief = await readFile(briefPath, "utf8");
  check(
    "Downloaded brief keeps grade and finance",
    brief.includes("Q HV Modellista") &&
      brief.includes("620.000.000") &&
      brief.includes("40%") &&
      brief.includes("Auto2000 Pasteur"),
  );
  check(
    "HEV downloaded brief omits electricity tariff",
    !/electricity per kwh|electricity Rp/i.test(brief),
  );
  await dialog
    .getByLabel("Include my purchase simulation in the shared brief", {
      exact: true,
    })
    .uncheck();
  await dialog
    .getByRole("button", { name: "Generate visit brief", exact: true })
    .click();
  const privateWa = new URL(
    await dialog
      .getByRole("link", {
        name: "Send Brief to Auto2000 WhatsApp (Tasia)",
        exact: true,
      })
      .getAttribute("href"),
  );
  check(
    "WhatsApp finance opt-out respected",
    !privateWa.searchParams.get("text").includes("Monthly repayment:") &&
      privateWa.searchParams
        .get("text")
        .includes("Finance simulation excluded"),
  );
  await shot("09-visit-brief");
  const sharedPage = await browser.newPage({
    viewport: { width: 1440, height: 1000 },
  });
  sharedPage.on("pageerror", (e) => errors.push(e.message));
  await sharedPage.goto(link);
  const sharedDialog = sharedPage.getByRole("dialog");
  await sharedDialog.waitFor();
  check(
    "Shared link reopens the original vehicle",
    (await sharedDialog
      .getByText("Kijang Innova Zenix", { exact: true })
      .count()) === 1,
  );
  check(
    "Shared link reopens branch and configuration",
    (await sharedDialog
      .locator(".branch-option.selected strong")
      .innerText()) === "Auto2000 Pasteur" &&
      (await sharedDialog.locator(".visit-vehicle").innerText()).includes(
        "Q HV Modellista",
      ),
  );
  await sharedPage.close();
  await dialog
    .getByRole("button", { name: "Close visit brief", exact: true })
    .click();
  check("Dialog closes", (await page.getByRole("dialog").count()) === 0);
  await page
    .getByRole("button", { name: "Interactive showroom", exact: true })
    .click();
  await page.getByRole("button", { name: "Your week", exact: true }).click();
  await page
    .getByRole("spinbutton", { name: "Weekly driving", exact: true })
    .fill("300");
  await page
    .getByRole("button", { name: "Branch & visit", exact: true })
    .click();
  await page.getByText("Review purchase simulation", { exact: true }).click();
  check(
    "Changed driving inputs invalidate old finance summary",
    await page
      .locator(".visit-finance-preview pre")
      .innerText()
      .then((t) => t.includes("not current")),
  );
  await page
    .getByRole("button", { name: "Close visit brief", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Explore all xEV", exact: true })
    .click();
  await page
    .getByRole("button", {
      name: "View Urban Cruiser Battery EV details",
      exact: true,
    })
    .click();
  await page
    .getByRole("button", { name: "Calculate this configuration", exact: true })
    .click();
  check(
    "Catalogue-only selection has its own purchase context",
    (await page.locator(".own-header").innerText()).includes(
      "Urban Cruiser Battery EV",
    ),
  );
  await page.getByRole("button", { name: "Save", exact: true }).click();
  await page.reload();
  await page.locator(".ownership-shell").waitFor({ state: "visible" });
  check(
    "Catalogue-only reload restores ownership instead of mismatched 3D",
    (await page.locator(".ownership-shell").isVisible()) &&
      (await page.locator(".own-header").innerText()).includes(
        "Urban Cruiser Battery EV",
      ),
  );
  await page
    .getByRole("button", { name: "Interactive showroom", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Branch & visit", exact: true })
    .click();
  check(
    "Returning to studio resets visit to actual 3D model",
    (await page.locator(".visit-vehicle").innerText()).includes(
      "Kijang Innova Zenix",
    ) &&
      !(await page.locator(".visit-vehicle").innerText()).includes(
        "Urban Cruiser",
      ),
  );
  await page
    .getByRole("button", { name: "Close visit brief", exact: true })
    .click();
  await page.route("https://tile.openstreetmap.org/**", (route) =>
    route.abort("failed"),
  );
  await page
    .getByRole("button", { name: "Branch & visit", exact: true })
    .click();
  await page.locator(".road-map[data-map-state=failed]").waitFor();
  check(
    "Map outage offers recovery",
    await page
      .getByRole("button", { name: "Retry map", exact: true })
      .isVisible(),
  );
  await page
    .getByRole("button", { name: "Reference map", exact: true })
    .click();
  await page
    .getByRole("button", {
      name: "Select Auto2000 Bekasi Timur on map",
      exact: true,
    })
    .click();
  check(
    "Reference map remains interactive without road tiles",
    (await page.locator(".branch-option.selected strong").innerText()) ===
      "Auto2000 Bekasi Timur",
  );
  await shot("09b-map-fallback");
  await page
    .getByRole("button", { name: "Close visit brief", exact: true })
    .click();
  await page.unroute("https://tile.openstreetmap.org/**");
  await page.setViewportSize({ width: 390, height: 844 });
  await page
    .getByRole("button", { name: "Explore all xEV", exact: true })
    .click();
  check(
    "Mobile catalogue has no page overflow",
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  );
  await shot("10-mobile-catalogue");
  await page
    .getByRole("button", { name: "Purchase & ownership", exact: true })
    .click();
  check(
    "Mobile ownership has no page overflow",
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  );
  await shot("11-mobile-ownership");
  await page
    .getByRole("button", { name: "Prepare a visit brief", exact: true })
    .click();
  check(
    "Mobile modal stays within viewport",
    await page
      .getByRole("dialog")
      .evaluate(
        (el) =>
          el.getBoundingClientRect().width <= innerWidth &&
          el.getBoundingClientRect().height <= innerHeight,
      ),
  );
  await page.getByRole("dialog").evaluate((el) => {
    el.scrollTop = el.scrollHeight;
  });
  check(
    "Mobile Close remains visible after modal scroll",
    await page
      .getByRole("button", { name: "Close visit brief", exact: true })
      .evaluate((el) => {
        const r = el.getBoundingClientRect();
        return r.top >= 0 && r.bottom <= innerHeight;
      }),
  );
  check(
    "Modal locks background scrolling",
    await page.evaluate(
      () => getComputedStyle(document.documentElement).overflow === "hidden",
    ),
  );
  await page.getByLabel("Preferred day", { exact: true }).fill("2099-01-01");
  await page
    .getByRole("button", { name: "Generate visit brief", exact: true })
    .click();
  const mobileTasia = page.getByRole("link", {
    name: "Send Brief to Auto2000 WhatsApp (Tasia)",
    exact: true,
  });
  await mobileTasia.scrollIntoViewIfNeeded();
  check(
    "Mobile Tasia action fits dialog",
    await mobileTasia.evaluate((el) => {
      const r = el.getBoundingClientRect();
      return r.left >= 0 && r.right <= innerWidth && r.height >= 44;
    }),
  );
  await shot("12-mobile-visit");
  await page
    .getByRole("button", { name: "Close visit brief", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Interactive showroom", exact: true })
    .click();
  await page.getByRole("button", { name: "Showroom", exact: true }).click();
  await page.locator("canvas[data-scene-ready=true]").waitFor();
  check(
    "Normal shopping navigation restores 3D without a false failure",
    (await page.locator(".scene-recovery").count()) === 0,
  );
  check(
    "Mobile showroom has no page overflow",
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  );
  await shot("13-mobile-showroom");
  await page.getByRole("button", { name: "2D plan", exact: true }).click();
  check(
    "Interactive 2D alternative",
    (await page
      .getByRole("img", { name: "Overhead vehicle plan", exact: true })
      .count()) === 1,
  );
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.getByRole("button", { name: "3D view", exact: true }).click();
  await page.locator("canvas[data-scene-ready=true]").waitFor();
  check(
    "Reduced motion retains scene",
    (await page.locator("canvas").count()) === 1,
  );
  await page.context().setOffline(true);
  await page.getByRole("button", { name: "Your family", exact: true }).click();
  check(
    "Loaded session core works offline",
    (await page
      .getByRole("heading", {
        name: "Configure seats and luggage",
        exact: true,
      })
      .count()) === 1,
  );
  await page.context().setOffline(false);
  await page
    .locator("canvas")
    .evaluate((el) =>
      el.dispatchEvent(new Event("webglcontextlost", { cancelable: true })),
    );
  await page
    .getByRole("img", { name: "Overhead vehicle plan", exact: true })
    .waitFor();
  check(
    "Context loss gives explicit recovery",
    (await page
      .getByRole("button", { name: "Retry 3D in Lite", exact: true })
      .count()) === 1,
  );
  await page
    .getByRole("button", { name: "Retry 3D in Lite", exact: true })
    .click();
  await page.locator("canvas[data-scene-ready=true]").waitFor();
  check(
    "WebGL retry restores a scene",
    (await page
      .getByRole("combobox", { name: "Graphics quality", exact: true })
      .inputValue()) === "lite",
  );
  check("No uncaught browser errors", errors.length === 0);
  check("No missing assets", requests.length === 0);
} finally {
  await writeFile(
    path.join(out, "browser-results.json"),
    JSON.stringify(
      {
        checks,
        errors,
        requests,
        networkLimitations,
        renderer:
          "Playwright Chromium headless software rendering; not target-device FPS evidence",
      },
      null,
      2,
    ),
  );
  await browser.close();
  await new Promise((r) => server.close(r));
}
console.log(
  JSON.stringify(
    {
      passed: checks.every((c) => c.passed),
      checks: checks.length,
      errors,
      requests,
      networkLimitations,
    },
    null,
    2,
  ),
);

import assert from "node:assert/strict";
import { mkdir, readFile } from "node:fs/promises";
import path from "node:path";
import { chromium, devices, expect } from "@playwright/test";
import { preview } from "vite";
const out = path.resolve(process.env.QA_OUTPUT || "qa-browser-key");
await mkdir(out, { recursive: true });
const server = await preview({
  preview: { host: "127.0.0.1", port: 4817, strictPort: true },
});
const base = "http://127.0.0.1:" + server.httpServer.address().port + "/";
const browser = await chromium.launch({
  executablePath: process.env.PLAYWRIGHT_EXECUTABLE_PATH || undefined,
  args: ["--no-sandbox", "--enable-unsafe-swiftshader"],
});
const external = [],
  errors = [],
  writes = [];
const page = await browser.newPage({
  ...(process.env.QA_MOBILE === "1"
    ? { ...devices["Pixel 7"], viewport: { width: 440, height: 956 } }
    : { viewport: { width: 1440, height: 900 } }),
  acceptDownloads: true,
  reducedMotion: "reduce",
});
page.setDefaultTimeout(12000);
page.on("pageerror", (error) => errors.push(error.message));
await page.route("**/*", (route) => {
  const url = new URL(route.request().url());
  if (route.request().method() !== "GET") writes.push(route.request().method());
  if (url.origin === new URL(base).origin) return route.continue();
  external.push(url.hostname);
  return route.abort();
});
const button = (name) => page.getByRole("button", { name, exact: true });
const heading = (name) => page.getByRole("heading", { name, exact: true });
const press = (name) => button(name).click();
const role = (value) =>
  page.getByRole("combobox", { name: "Switch workspace" }).selectOption(value);
const shot = (name) =>
  page.screenshot({ path: path.join(out, name + ".png"), fullPage: true });
const forbidden =
  /needs validation|illustrative concept|just a prototype|pilot only|subject to validation|proof of concept|masih perlu diuji|perlu divalidasi/i;
async function cleanCopy() {
  assert.doesNotMatch(await page.locator("body").innerText(), forbidden);
}
async function output(buttonName, filename, content) {
  const downloading = page.waitForEvent("download");
  await press(buttonName);
  const download = await downloading;
  assert.match(download.suggestedFilename(), filename);
  const text = await readFile(await download.path(), "utf8");
  assert.doesNotMatch(text, forbidden);
  assert.match(text, content);
}
try {
  await page.goto(base);
  await expect(heading(/Know your fit/)).toBeVisible();
  await expect(page.getByRole("img", { name: /Silver Innova/ })).toBeVisible();
  assert.equal(
    await page
      .getByRole("img", { name: /Silver Innova/ })
      .evaluate((image) => image.complete && image.naturalWidth > 0),
    true,
  );
  await shot("01-home");
  await cleanCopy();
  await press("Open 3D Life Test");
  await expect(page.locator("canvas[data-scene-ready=true]")).toBeVisible({
    timeout: 20000,
  });
  await page.getByRole("button", { name: "Your garage", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: /Check your garage clearance/ }),
  ).toBeVisible();
  await page.getByRole("button", { name: /2D/ }).first().click();
  await expect(
    page.locator("svg[aria-label]").filter({ visible: true }).first(),
  ).toBeVisible();
  await press("Save visit card to KEY");
  await expect(heading("Take your checklist on the road")).toBeVisible();
  await output(
    "Download visit card",
    /Life-Test/,
    /Garage .*check driver door/i,
  );
  await press("Send to sales adviser");
  await expect(heading("Awaiting branch confirmation")).toBeVisible();
  await role("sales");
  await press("Confirm requested drive");
  await expect(heading("Drive confirmed")).toBeVisible();
  await page.getByRole("checkbox", { name: /Licence, coverage/ }).check();
  await press("Record vehicle pickup");
  await role("customer");
  await expect(heading("On the Life Test")).toBeVisible();
  await press("Save household results");
  await role("sales");
  await press("Accept vehicle return");
  await press("Issue dated purchase quote");
  await role("customer");
  await press("Open household buyer view");
  await output("Download buyer copy", /purchase-quote/, /Monthly payment/);
  await press("Accept purchase quote");
  await role("sales");
  await press("Record lender decision");
  await press("Record vehicle order");
  await press("Confirm Toyota delivery");
  await role("customer");
  await expect(heading("Toyota delivered")).toBeVisible();
  await page.reload();
  await expect(heading("Toyota delivered")).toBeVisible();
  await cleanCopy();
  console.log(
    "PASS K: WebGL and 2D studio, exported checklist, adviser calendar, pickup, buyer quote, lender decision, delivery and reload",
  );
  await page.getByRole("link", { name: "Easy Service", exact: true }).click();
  await expect(page.locator('[data-map-source="offline"]')).toBeVisible();
  assert.ok(external.includes("tile.openstreetmap.org"));
  const counts = [
    ["Bandung", "78", "17", "14"],
    ["Surabaya", "59", "10", "6"],
    ["Medan", "78", "3", "0"],
    ["Palembang", "69", "9", "0"],
  ];
  for (const [city, n, before, after] of counts) {
    await press(city);
    await press("Dealer workshops");
    await expect(page.getByTestId("market-gap")).toHaveText(before + " / " + n);
    await press("With eligible OtoXpert");
    await expect(page.getByTestId("market-gap")).toHaveText(after + " / " + n);
  }
  await press("Bandung");
  await expect(page.getByTestId("origin-detail")).toContainText(
    "OtoXpert Bojongsoang",
  );
  await expect(page.locator(".key-map svg path").first()).toBeVisible();
  const marks = await page.locator('.key-map svg path[fill="#128579"]').count();
  await press("Dealer workshops");
  assert.equal(
    marks - (await page.locator('.key-map svg path[fill="#128579"]').count()),
    3,
  );
  await press("With eligible OtoXpert");
  await press("Zoom in");
  await press("List view");
  await expect(page.getByRole("table")).toBeVisible();
  await page.getByRole("table").getByRole("button").first().click();
  await expect(
    page.getByRole("combobox", { name: "Modeled origin" }),
  ).toHaveValue("g00_00");
  await page
    .getByRole("combobox", { name: "Modeled origin" })
    .selectOption("g04_00");
  await press("Show map");
  await expect(page.locator('[data-map-source="offline"]')).toBeVisible();
  await shot("02-bandung-offline");
  await press("Request this service");
  await role("workshop");
  await press("Reserve parts and confirm slot");
  await press("Check in vehicle");
  await press("Issue estimate v2");
  await role("customer");
  await press("Share approval link");
  const oldLink = await page
    .getByRole("textbox", { name: /Scoped approval link/ })
    .inputValue();
  await role("workshop");
  await page
    .getByText("Write additional work estimate", { exact: true })
    .click();
  await page
    .getByRole("spinbutton", { name: /Additional installed price/ })
    .fill("188700");
  await press("Issue estimate v3");
  await page.goto(oldLink);
  await expect(page.getByRole("alert")).toContainText(
    "approval link has expired",
  );
  await press("Open authorized payer view");
  await expect(heading("Additional work estimate · v3")).toBeVisible();
  await press("Approve estimate v3");
  await role("workshop");
  await press("Mark ready for collection");
  await expect(heading("Ready for collection")).toBeVisible();
  await press("Record handover and issue receipt");
  await role("customer");
  await expect(heading("Service completed")).toBeVisible();
  await output(
    "Download service receipt",
    /receipt/,
    /Approved scope version: 3/,
  );
  await cleanCopy();
  console.log(
    "PASS E: blocked tiles, four market denominators and counts, real markers, list, parts, stale quote, payer approval and receipt",
  );
  await page
    .getByRole("link", { name: "Your Next Toyota", exact: true })
    .click();
  await press("Request an inspection");
  await role("upgrade");
  await press("Issue inspected buy offer");
  await page.getByRole("checkbox", { name: /Lender conditions/ }).check();
  await press("Reserve unit and issue upgrade terms");
  await role("customer");
  await expect(heading("Ready for owner acceptance")).toBeVisible();
  await page
    .getByRole("term")
    .filter({ hasText: "Trade-in equity credit" })
    .waitFor();
  await output(
    "Download upgrade terms",
    /upgrade-terms/,
    /71\.500\.000|71,500,000/,
  );
  await press("Accept current upgrade terms");
  await role("upgrade");
  await page
    .getByText("Offer expired or unit unavailable", { exact: true })
    .click();
  await press("Withdraw terms and record refund");
  await expect(page.getByText(/Deposit refund recorded/)).toBeVisible();
  await press("Arrange new terms");
  await press("Issue inspected buy offer");
  await page.getByRole("checkbox", { name: /Lender conditions/ }).check();
  await press("Reserve unit and issue upgrade terms");
  await role("customer");
  await press("Accept current upgrade terms");
  await role("upgrade");
  await press("Record settlement");
  await press("Confirm both handovers");
  await role("customer");
  await expect(heading("Replacement Toyota delivered")).toBeVisible();
  await shot("03-upgrade-delivery");
  await cleanCopy();
  console.log(
    "PASS Y: written inspection offer, equity, lender/unit, accepted terms, recovery/refund, settlement and both handovers",
  );
  await page.getByRole("link", { name: "My requests" }).click();
  await expect(page.getByRole("button", { name: "Open record" })).toHaveCount(
    3,
  );
  await page.getByRole("link", { name: "Vehicle records" }).click();
  await expect(page.getByRole("button", { name: "Open record" })).toHaveCount(
    3,
  );
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole("link", { name: "Overview" }).click();
  await expect(heading(/Know your fit/)).toBeVisible();
  assert.equal(
    await page
      .locator("body")
      .evaluate((body) => body.scrollWidth <= innerWidth),
    true,
  );
  await press("ID");
  await expect(heading(/Kenali kecocokan/)).toBeVisible();
  await cleanCopy();
  await page.getByRole("link", { name: "Servis Mudah", exact: true }).click();
  await expect(heading("Servis selesai")).toBeVisible();
  assert.equal(
    await page
      .locator("body")
      .evaluate((body) => body.scrollWidth <= innerWidth),
    true,
  );
  await shot("04-mobile-service");
  await press("Atur ulang alur demo");
  await page
    .getByRole("dialog")
    .getByRole("button", { name: "Simpan progres" })
    .click();
  await expect(heading("Servis selesai")).toBeVisible();
  await press("Atur ulang alur demo");
  await page
    .getByRole("dialog")
    .getByRole("button", { name: "Atur ulang alur demo" })
    .click();
  await expect(heading(/Kenali kecocokan/)).toBeVisible();
  await page.getByRole("link", { name: "Servis Mudah", exact: true }).click();
  await expect(heading("Bandung")).toBeVisible();
  assert.equal(
    await page
      .locator("body")
      .evaluate((body) => body.scrollWidth <= innerWidth),
    true,
  );
  await shot("05-mobile-map");
  assert.deepEqual(errors, []);
  assert.deepEqual(writes, []);
  assert.deepEqual([...new Set(external)], ["tile.openstreetmap.org"]);
  console.log(
    "PASS shared history, 390 px mobile layout, Indonesian, deliberate reset, zero page errors, no outbound writes",
  );
} finally {
  await browser.close();
  await new Promise((resolve) => server.httpServer.close(resolve));
}

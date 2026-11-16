import assert from "node:assert/strict";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { chromium, devices, expect, firefox, webkit } from "@playwright/test";
import { preview } from "vite";
const engine = process.env.QA_ENGINE || "chromium";
const browser = await { chromium, firefox, webkit }[engine].launch();
const server = await preview({ preview: { host: "127.0.0.1", port: 0 } });
const base = "http://127.0.0.1:" + server.httpServer.address().port + "/";
const routes = {
  "#home": ".key-hero h1",
  "#k": ".key-visit-card h2",
  "#e": ".key-service-offers h2",
  "#y": ".key-split h2",
  "#requests": ".key-main h1",
  "#records": ".key-main h1",
  "#sales": ".key-queue",
  "#workshop": ".key-queue",
  "#upgrade": ".key-queue",
  "#studio": ".task-panel h1",
  "#studio/garage": ".task-panel h1",
  "#studio/ownership": ".own-header h2",
};
const out = process.env.QA_OUTPUT;
const touch = { ...devices[engine === "webkit" ? "iPhone 15" : "Pixel 7"] };
if (engine === "firefox") delete touch.isMobile;
const screenSizes = [
  [320, 670],
  [360, 800],
  [390, 844],
  [430, 932],
  [431, 932],
  [440, 956],
  [480, 850],
  [540, 850],
  [600, 850],
  [601, 850],
  [760, 850],
  [761, 850],
  [768, 1024],
  [844, 390],
  [1024, 768],
  [1280, 720],
  [1920, 1080],
];
const errors = [];
function watch(page) {
  page.on("pageerror", (error) => errors.push(error.message));
  return page.route("https://tile.openstreetmap.org/**", (route) =>
    route.abort(),
  );
}
async function fit(page, name, elements = []) {
  await page.evaluate(() => document.fonts.ready.then(() => true));
  const dimensions = await page.evaluate(() => ({
    width: document.documentElement.clientWidth,
    content: document.documentElement.scrollWidth,
  }));
  assert.ok(
    dimensions.content <= dimensions.width + 1,
    `${name} overflows: ${dimensions.content} > ${dimensions.width}`,
  );
  for (const locator of elements) {
    await expect(locator).toBeVisible();
    const box = await locator.boundingBox();
    assert.ok(
      box.x >= -1 && box.x + box.width <= dimensions.width + 1,
      `${name}: ${locator} extends outside the viewport`,
    );
  }
}
async function visit(page, route, selector) {
  await page.goto(base + route, { waitUntil: "domcontentloaded" });
  await expect(page.locator(selector).first()).toBeVisible();
}
try {
  const page = await browser.newPage({ reducedMotion: "reduce" });
  await watch(page);
  for (const [width, height] of screenSizes) {
    await page.setViewportSize({ width, height });
    for (const [route, selector] of Object.entries(routes)) {
      await visit(page, route, selector);
      await fit(page, `${width}×${height} ${route}`, [
        page.locator(
          route.startsWith("#studio") ? ".save-button" : ".key-role",
        ),
      ]);
    }
  }
  await page.close();
  const mobile = await browser.newPage({
    ...touch,
    viewport: { width: 320, height: 668 },
    reducedMotion: "reduce",
  });
  await watch(mobile);
  await mobile.addInitScript(() => {
    const getContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (type, ...args) {
      return /webgl/i.test(type) ? null : getContext.call(this, type, ...args);
    };
  });
  await visit(mobile, "#home", ".key-hero h1");
  await mobile.getByRole("button", { name: "ID", exact: true }).tap();
  await fit(mobile, "Bahasa phone header", [
    mobile.getByRole("combobox", { name: "Ganti ruang kerja" }),
  ]);
  await mobile.getByRole("button", { name: "EN", exact: true }).tap();
  await mobile
    .getByRole("combobox", { name: "Switch workspace" })
    .selectOption("workshop");
  await expect(
    mobile.getByText("No service requests yet").first(),
  ).toBeVisible();
  await mobile
    .getByRole("combobox", { name: "Switch workspace" })
    .selectOption("customer");
  await mobile.getByRole("button", { name: "Jump to service offers" }).tap();
  await expect(mobile.locator(".key-service-offers")).toBeFocused();
  await expect(
    mobile.getByRole("combobox", { name: "Workshop job" }),
  ).toBeInViewport();
  await fit(mobile, "mobile service offers");
  await visit(mobile, "#studio/garage", ".task-panel h1");
  await expect(mobile.locator(".plan-view")).toBeVisible();
  await mobile.getByRole("button", { name: "Your family", exact: true }).tap();
  await expect(
    mobile.getByRole("heading", { name: /Configure seats/ }),
  ).toBeVisible();
  const branch = mobile.getByRole("button", {
    name: "Branch & visit",
    exact: true,
  });
  await fit(mobile, "mobile showroom", [branch]);
  await branch.tap();
  const modal = mobile.getByRole("dialog");
  await expect(modal).toBeVisible();
  await fit(mobile, "mobile branch visit", [
    modal,
    modal.getByRole("button", { name: "Close visit brief" }),
  ]);
  assert.ok(
    await modal.evaluate(
      (element) => element.scrollWidth <= element.clientWidth + 1,
    ),
    "visit dialog has horizontal overflow",
  );
  await modal.getByRole("button", { name: "Close visit brief" }).tap();
  await expect(modal).not.toBeVisible();
  await mobile
    .getByRole("button", { name: "Explore all xEV", exact: true })
    .tap();
  await expect(mobile.locator(".catalogue-page")).toBeVisible();
  await mobile
    .getByRole("button", { name: /View .* details/ })
    .first()
    .tap();
  await fit(mobile, "mobile vehicle details");
  await mobile
    .getByRole("button", { name: "Purchase & ownership", exact: true })
    .tap();
  await expect(mobile.locator(".own-header h2")).toBeVisible();
  await fit(
    mobile,
    "mobile purchase and ownership",
    await mobile.locator(".own-tabs button").all(),
  );
  await mobile
    .getByRole("button", { name: "Service & benefits", exact: true })
    .tap();
  await fit(mobile, "mobile service benefits");
  if (out) {
    await mkdir(out, { recursive: true });
    await mobile.setViewportSize({ width: 440, height: 956 });
    await visit(mobile, "#home", ".key-hero h1");
    await mobile.screenshot({ path: path.join(out, `${engine}-440-home.png`) });
  }
  assert.deepEqual(errors, []);
  console.log(
    `PASS ${engine}: ${screenSizes.length} viewport sizes × ${Object.keys(routes).length} routes, plus touch navigation, language, service jump, 2D fallback, visit dialog, catalogue and ownership`,
  );
} finally {
  await browser.close();
  await new Promise((resolve) => server.httpServer.close(resolve));
}

const fs = require("fs");
const path = require("path");
const { expect } = require("@playwright/test");

const smokeDataPath = path.resolve(__dirname, "../../../addons/.playwright-smoke-data.json");

function readSmokeData() {
  return JSON.parse(fs.readFileSync(smokeDataPath, "utf8"));
}

async function login(page, credentials) {
  await page.goto("/web/login", { waitUntil: "domcontentloaded" });
  await page.locator('input[name="login"]').fill(credentials.login);
  await page.locator('input[name="password"]').fill(credentials.password);
  await Promise.all([
    page.waitForURL(/\/odoo|\/web/, { timeout: 15000 }),
    page.getByRole("button", { name: /log in/i }).click(),
  ]);
  await expect(page.locator(".o_web_client, .o_main_navbar, .o_action_manager").first()).toBeVisible();
  await page.waitForTimeout(1500);
}

function actionUrl(baseURL, { action, recordId }) {
  return `${baseURL}/odoo/action-${action}${recordId ? `/${recordId}` : ""}`;
}

async function openAction(page, options) {
  const data = readSmokeData();
  await page.goto(actionUrl(data.base_url, options), { waitUntil: "domcontentloaded" });
  await expect(page.locator(".o_web_client, .o_action_manager, .o_content").first()).toBeVisible();
  await page.waitForTimeout(2000);
}

async function maybeDismissDialog(page) {
  const okButton = page.getByRole("button", { name: /^ok$/i });
  if (await okButton.isVisible().catch(() => false)) {
    await okButton.click();
  }
}

async function expectNotification(page, text) {
  await expect(page.getByText(text, { exact: false })).toBeVisible();
}

async function openHtmlReportFromButton(page, buttonLabel) {
  const popupPromise = page.waitForEvent("popup", { timeout: 5000 }).catch(() => null);
  const samePageReportPromise = page.waitForURL(/\/report\/html\//, { timeout: 5000 }).catch(
    () => null
  );
  await page.getByRole("button", { name: buttonLabel }).click();
  const popup = await popupPromise;
  if (popup) {
    await popup.waitForLoadState("domcontentloaded");
    return popup;
  }
  await samePageReportPromise;
  return page;
}

module.exports = {
  expect,
  expectNotification,
  login,
  maybeDismissDialog,
  openAction,
  openHtmlReportFromButton,
  readSmokeData,
};

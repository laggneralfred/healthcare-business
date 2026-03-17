const { defineConfig } = require("@playwright/test");

const browserName = process.env.PLAYWRIGHT_BROWSER || "firefox";

const use = {
  baseURL: process.env.PLAYWRIGHT_BASE_URL || "http://127.0.0.1:8069",
  browserName,
  headless: true,
  trace: "on-first-retry",
  screenshot: "only-on-failure",
  video: "off",
};

if (browserName === "chromium") {
  use.channel = "chromium";
  use.chromiumSandbox = false;
  use.launchOptions = {
    args: [
      "--disable-crash-reporter",
      "--disable-crashpad",
      "--no-crash-upload",
    ],
  };
}

module.exports = defineConfig({
  testDir: "./tests/playwright",
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR || "/tmp/playwright-results",
  timeout: 60_000,
  expect: {
    timeout: 10_000,
  },
  fullyParallel: false,
  retries: 0,
  workers: 1,
  reporter: [["list"]],
  use,
});

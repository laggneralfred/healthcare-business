const { test } = require("@playwright/test");
const {
  expect,
  expectNotification,
  login,
  maybeDismissDialog,
  openAction,
  openHtmlReportFromButton,
  readSmokeData,
} = require("./helpers/odoo");

test.describe("Sprint 18 pilot smoke", () => {
  test("role-based access stays within the frozen clinic baseline", async ({ browser }) => {
    const data = readSmokeData();

    const ownerContext = await browser.newContext();
    const ownerPage = await ownerContext.newPage();
    await login(ownerPage, data.users.owner);
    await openAction(ownerPage, {
      action: data.actions.service_fees,
    });
    await expect(ownerPage.getByText(data.expected.service_fee_name, { exact: false })).toBeVisible();
    await ownerContext.close();

    const providerContext = await browser.newContext();
    const providerPage = await providerContext.newPage();
    await login(providerPage, data.users.provider);
    await openAction(providerPage, {
      action: data.actions.appointments,
      recordId: data.records.appointment_id,
    });
    await expect(providerPage.getByRole("button", { name: "Start Checkout" })).toHaveCount(0);
    await providerContext.close();
  });

  test("front desk can move one checkout from payment_due to paid and clear the unpaid summary", async ({
    page,
  }) => {
    const data = readSmokeData();

    await login(page, data.users.front_desk);
    await openAction(page, {
      action: data.actions.appointments,
      recordId: data.records.appointment_id,
    });

    await expect(page.getByText(data.expected.appointment_name, { exact: false })).toBeVisible();
    await expect(page.getByRole("button", { name: "Start Checkout" })).toBeVisible();
    await page.getByRole("button", { name: "Start Checkout" }).click();

    await expect(page.getByRole("cell", { name: data.expected.service_fee_name }).first()).toBeVisible();
    await expect(page.getByText(data.expected.checkout_total, { exact: false }).first()).toBeVisible();
    await expect(page.getByRole("button", { name: "Mark Payment Due" })).toBeVisible();

    const checkoutName = data.expected.checkout_name;

    await page.getByRole("button", { name: "Mark Payment Due" }).click();
    await expect(page.getByRole("button", { name: "Collect Cash Payment" })).toBeVisible();

    await openAction(page, {
      action: data.actions.patients,
      recordId: data.records.patient_id,
    });
    await expect(page.getByRole("button", { name: "Print Patient Statement" })).toBeVisible();

    const statementPage = await openHtmlReportFromButton(page, "Print Patient Statement");
    const statementContent =
      statementPage === page ? page.frameLocator("iframe") : statementPage;
    await expect(statementContent.getByText("Patient Statement", { exact: false })).toBeVisible();
    await expect(statementContent.getByText(data.expected.patient_name, { exact: true })).toBeVisible();
    await expect(statementContent.getByText(checkoutName, { exact: false })).toBeVisible();

    if (statementPage !== page) {
      await statementPage.close();
    }

    await openAction(page, {
      action: data.actions.checkout,
    });
    await page.getByText(checkoutName, { exact: false }).click();
    await page.waitForLoadState("networkidle");

    await expect(page.getByRole("button", { name: "Collect Cash Payment" })).toBeVisible();
    await page.getByRole("button", { name: "Collect Cash Payment" }).click();
    await expect(page.getByRole("button", { name: "Collect Cash Payment" })).toHaveCount(0);

    await openAction(page, {
      action: data.actions.patients,
      recordId: data.records.patient_id,
    });
    await page.getByRole("button", { name: "Print Patient Statement" }).click();
    await expectNotification(
      page,
      "Patient statement is only available when unpaid checkout sessions exist."
    );
    await maybeDismissDialog(page);
  });
});

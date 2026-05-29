/**
 * Google Sheets Automation Demo — Order Tracker
 * ==============================================
 * Two automations on one sheet:
 *
 *  1. onEdit trigger: when someone sets a row's Status to "Done", it
 *     auto-stamps the completion time and emails a confirmation to the
 *     customer — instantly, hands-free.
 *
 *  2. sendDailySummary(): a scheduled (time-driven) function that emails
 *     the owner a daily roll-up of pending vs. completed orders.
 *
 * Expected sheet columns (row 1 = headers):
 *   A: Order ID | B: Customer | C: Email | D: Amount | E: Status | F: Completed At
 *
 * Status values: "Pending" / "Done"
 *
 * --- SETUP ---
 *  • Extensions > Apps Script, paste this file.
 *  • Set OWNER_EMAIL below.
 *  • onEdit works automatically (simple trigger).
 *  • For the daily summary: run createDailyTrigger() ONCE to schedule it.
 */

const OWNER_EMAIL = "you@example.com"; // <-- change this
const SHEET_NAME = "Orders";

// Column indexes (1-based, matching A=1, B=2, ...)
const COL = { ORDER_ID: 1, CUSTOMER: 2, EMAIL: 3, AMOUNT: 4, STATUS: 5, COMPLETED_AT: 6 };

/**
 * Simple trigger: fires on every edit. We only act when the Status column
 * of a data row is changed to "Done".
 */
function onEdit(e) {
  const range = e.range;
  const sheet = range.getSheet();

  if (sheet.getName() !== SHEET_NAME) return;
  if (range.getColumn() !== COL.STATUS) return;
  if (range.getRow() === 1) return; // header

  const newValue = String(e.value || "").trim().toLowerCase();
  if (newValue !== "done") return;

  const row = range.getRow();
  const rowValues = sheet.getRange(row, 1, 1, COL.COMPLETED_AT).getValues()[0];

  const orderId = rowValues[COL.ORDER_ID - 1];
  const customer = rowValues[COL.CUSTOMER - 1];
  const email = rowValues[COL.EMAIL - 1];
  const amount = rowValues[COL.AMOUNT - 1];

  // 1. Stamp completion time
  sheet.getRange(row, COL.COMPLETED_AT).setValue(new Date());

  // 2. Email the customer (skip if no address)
  if (email && /\S+@\S+\.\S+/.test(email)) {
    const subject = `Your order ${orderId} is complete ✅`;
    const body =
      `Hi ${customer},\n\n` +
      `Good news — your order ${orderId} (amount: ${amount}) has been completed.\n\n` +
      `Thank you for your business!\n\n` +
      `— The Team`;
    MailApp.sendEmail(email, subject, body);
    sheet.getRange(row, COL.STATUS).setNote("Confirmation email sent " + new Date());
  }
}

/**
 * Time-driven: emails the OWNER a summary of pending vs. completed orders.
 * Schedule it with createDailyTrigger().
 */
function sendDailySummary() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  if (!sheet) return;

  const lastRow = sheet.getLastRow();
  if (lastRow < 2) return;

  const data = sheet.getRange(2, 1, lastRow - 1, COL.COMPLETED_AT).getValues();

  let pending = 0;
  let done = 0;
  let pendingTotal = 0;

  data.forEach(function (r) {
    const status = String(r[COL.STATUS - 1]).trim().toLowerCase();
    const amount = Number(r[COL.AMOUNT - 1]) || 0;
    if (status === "done") {
      done++;
    } else {
      pending++;
      pendingTotal += amount;
    }
  });

  const subject = `Daily Order Summary — ${pending} pending, ${done} done`;
  const body =
    `Daily summary:\n\n` +
    `• Pending orders: ${pending} (total amount: ${pendingTotal})\n` +
    `• Completed orders: ${done}\n\n` +
    `Generated automatically by your Sheet.`;

  MailApp.sendEmail(OWNER_EMAIL, subject, body);
}

/**
 * Run ONCE to schedule sendDailySummary every morning at ~8am.
 * Safe to re-run: it clears any previous copy of the same trigger first.
 */
function createDailyTrigger() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === "sendDailySummary") {
      ScriptApp.deleteTrigger(t);
    }
  });

  ScriptApp.newTrigger("sendDailySummary")
    .timeBased()
    .atHour(8)
    .everyDays(1)
    .create();

  SpreadsheetApp.getActiveSpreadsheet().toast("Daily summary scheduled for 8am.");
}

/**
 * Optional: adds a custom menu so non-technical users can trigger actions
 * from the toolbar instead of the Apps Script editor.
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("⚙️ Automation")
    .addItem("Send daily summary now", "sendDailySummary")
    .addItem("Schedule daily summary (8am)", "createDailyTrigger")
    .addToUi();
}

// Bấm icon extension → mở tab bảng điều khiển
chrome.action.onClicked.addListener(() => {
  chrome.tabs.create({ url: chrome.runtime.getURL("panel.html") });
});

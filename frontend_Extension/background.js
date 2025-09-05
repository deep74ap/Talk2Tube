chrome.runtime.onInstalled.addListener(() => {
  // When user clicks the toolbar icon, open the side panel
  chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
});

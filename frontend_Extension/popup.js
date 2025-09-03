document.getElementById("useCurrent").addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  document.getElementById("ytLink").value = tab.url;
});

document.getElementById("send").addEventListener("click", async () => {
  const videoUrl = document.getElementById("ytLink").value;
  const question = document.getElementById("userInput").value;
  if (!videoUrl || !question) return;

  addMessage("You", question);

  try {
    const response = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ videoUrl, question })
    });

    const data = await response.json();
    addMessage("AI", data.answer);
  } catch (e) {
    addMessage("Error", "Could not reach backend. Is it running?");
  }
});

function addMessage(sender, text) {
  const msgBox = document.getElementById("messages");
  msgBox.innerHTML += `<p><b>${sender}:</b> ${text}</p>`;
  msgBox.scrollTop = msgBox.scrollHeight;
}

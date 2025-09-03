// document.getElementById("useCurrent").addEventListener("click", async () => {
//   let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
//   document.getElementById("ytLink").value = tab.url;
// });


document.getElementById("send").addEventListener("click", async () => {
  const videoUrl = document.getElementById("ytLink").value.trim();
  const question = document.getElementById("userInput").value.trim();
  if (!videoUrl || !question) return;

  addMessage("You", question);

  try {
    const response = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ videoUrl, question })
    });

    if (!response.ok) {
      addMessage("Error", `Backend error: ${response.status}`);
      return;
    }

    const data = await response.json();
    if (data.answer) {
      addMessage("AI", data.answer, true); // Typing effect for AI
    } else if (data.error) {
      addMessage("Error", data.error);
    }
  } catch (e) {
    addMessage("Error", "Could not reach backend. Is it running?");
  }
});


// Typing queue for AI messages
let typingQueue = [];
let typingActive = false;

async function addMessage(sender, text, isTyping = false) {
  const msgBox = document.getElementById("messages");
  // User or error messages: render instantly
  if (sender !== "AI" || !isTyping) {
    const p = document.createElement("p");
    p.className = sender === "You" ? "user" : sender === "AI" ? "ai" : "error";
    p.innerHTML = `<b>${sender}:</b> ${text}`;
    msgBox.appendChild(p);
    msgBox.scrollTop = msgBox.scrollHeight;
    return;
  }
  // AI message with typing effect: queue
  typingQueue.push({ sender, text });
  if (!typingActive) processTypingQueue();
}

async function processTypingQueue() {
  typingActive = true;
  const msgBox = document.getElementById("messages");
  while (typingQueue.length > 0) {
    const { sender, text } = typingQueue.shift();
    const p = document.createElement("p");
    p.className = "ai";
    p.innerHTML = `<b>${sender}:</b> `;
    msgBox.appendChild(p);
    let i = 0;
    while (i < text.length) {
      p.innerHTML = `<b>${sender}:</b> ` + text.slice(0, i + 1);
      msgBox.scrollTop = msgBox.scrollHeight;
      await new Promise(res => setTimeout(res, 35 + Math.random() * 15));
      i++;
    }
    // Ensure fully visible after typing
    msgBox.scrollTop = msgBox.scrollHeight;
    await new Promise(res => setTimeout(res, 100));
  }
  typingActive = false;
}

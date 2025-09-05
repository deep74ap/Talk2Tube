document.addEventListener("DOMContentLoaded", () => {


  if (typeof chrome === "undefined" || !chrome.storage) {
    console.error("❌ Not running inside Chrome extension context.");
    return;
  }

  const ytLinkInput = document.getElementById("ytLink");
  const userInput = document.getElementById("userInput");
  const messagesBox = document.getElementById("messages");
  const sendBtn = document.getElementById("send");
  const useCurrentBtn = document.getElementById("useCurrent");


  function getVideoId(url) {
    const match = url.match(/[?&]v=([^&]+)/);
    return match ? match[1] : url;
  }
  
  // 🔹 Restore saved state
  chrome.storage.local.get(["ytLink", "messages"], (data) => {
    if (data.ytLink) ytLinkInput.value = data.ytLink;
    if (data.messages) {
      messagesBox.innerHTML = data.messages;
      messagesBox.scrollTop = messagesBox.scrollHeight;
    }
  });

  // 🔹 Save link immediately when user pastes/changes it
  ytLinkInput.addEventListener("input", () => {
    chrome.storage.local.set({ ytLink: ytLinkInput.value });
  });

  // ✅ Use current tab as video
  useCurrentBtn.addEventListener("click", async () => {
    try {
      console.log("📺 Getting current tab...");
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      console.log("🔍 Tab found:", tab);
      if (tab && tab.url) {
        ytLinkInput.value = tab.url;
        chrome.storage.local.set({ ytLink: tab.url });
      }
       else {
      addMessage("Error", "No active tab URL found.");
    }
    } catch (err) {
      addMessage("Error", "Could not read current tab URL.");
    }
  });


  // ✅ Send question
  sendBtn.addEventListener("click", async (event) => {
    event.preventDefault();
    console.log("📩 Send button clicked"); // 🔍 Debug log
    const videoUrl = ytLinkInput.value.trim();
    const question = userInput.value.trim();
    if (!videoUrl || !question) return;
    sendBtn.disabled = true;
    addMessage("You", question);
    userInput.value = "";

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ videoUrl, question }),
      });

      if (!response.ok) {
        addMessage("Error", `Backend error: ${response.status}`);
        return;
      }

      const data = await response.json();
      if (data.answer) {
        addMessage("AI", data.answer, true);
      } else if (data.error) {
        addMessage("Error", data.error);
      }
    } catch (e) {
      addMessage("Error", "Could not reach backend. Is it running?");
    }
    finally{
      sendBtn.disabled = false;
    }
  });

  // Typing queue
  let typingQueue = [];
  let typingActive = false;

  function persistMessages() {
    chrome.storage.local.set({ messages: messagesBox.innerHTML });
  }

  async function addMessage(sender, text, isTyping = false) {
    if (sender !== "AI" || !isTyping) {
      const p = document.createElement("p");
      p.className = sender === "You" ? "user" : sender === "AI" ? "ai" : "error";
      p.innerHTML = `<b>${sender}:</b> ${text}`;
      messagesBox.appendChild(p);
      messagesBox.scrollTop = messagesBox.scrollHeight;
      persistMessages();
      return;
    }

    typingQueue.push({ sender, text });
    if (!typingActive) processTypingQueue();
  }

  async function processTypingQueue() {
    typingActive = true;

    while (typingQueue.length > 0) {
      const { sender, text } = typingQueue.shift();
      const p = document.createElement("p");
      p.className = "ai";
      p.innerHTML = `<b>${sender}:</b> `;
      messagesBox.appendChild(p);

      let i = 0;
      while (i < text.length) {
        p.innerHTML = `<b>${sender}:</b> ` + text.slice(0, i + 1);
        messagesBox.scrollTop = messagesBox.scrollHeight;
        await new Promise((res) => setTimeout(res, 25 + Math.random() * 20));
        i++;
      }
      persistMessages();
      messagesBox.scrollTop = messagesBox.scrollHeight;
      await new Promise((res) => setTimeout(res, 80));
    }
    typingActive = false;
  }
});

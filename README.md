# 🎥 Talk2Tube – YouTube Q&A Assistant 🤖  

Talk2Tube is a **Chrome Extension** that lets you ask natural language questions about any YouTube video and get **AI-powered answers**.  
It combines the power of **Retrieval-Augmented Generation (RAG)** with a seamless frontend extension for a smooth user experience.  

---

## ✨ Features  

✅ Paste or capture the **current YouTube video link**  
✅ Ask **questions in plain English** about the video  
✅ Get **AI-powered answers** using RAG (Retrieval Augmented Generation)  
✅ **Chat history persistence** with local storage  
✅ Clean, simple **side panel UI** integrated into Chrome  

---

## 🛠️ Tech Stack  

**Frontend (Chrome Extension):**  
- HTML, CSS, JavaScript  
- Chrome Extension APIs (Side Panel, Tabs, Storage)  

**Backend:**  
- Python (FastAPI)  
- LangChain for RAG  
- ChromaDB for vector storage & retrieval  

**RAG Pipeline:**  
- `ragIndexing.py` → Index YouTube transcripts into ChromaDB  
- `ragGeneration.py` → Generate answers with context retrieval  
- `ragAugmentation.py` → Handle augmentation & embedding logic  

---

## 📂 Project Structure  

```
Talk2Tube/
│── backendRag/
│   ├── ragIndexing.py
│   ├── ragGeneration.py
│   ├── ragAugmentation.py
│   ├── requirements.txt
│
│── extension/
│   ├── manifest.json
│   ├── background.js
│   ├── sidebar.html
│   ├── sidebar.js
│   ├── styles.css
│   ├── icon.png
│
│── chroma_db/   # (Generated locally, not included in repo)
│── README.md
```

---

## 🚀 Installation  

### 1. Clone the Repository  
```bash
git clone https://github.com/deep74ap/Talk2Tube.git
cd Talk2Tube
```

### 2. Backend Setup  
```bash
cd backendRag
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

This will start the FastAPI backend at `http://127.0.0.1:8000`.

### 3. Extension Setup  
1. Open **Google Chrome** → Go to `chrome://extensions/`  
2. Enable **Developer Mode** (top-right)  
3. Click **Load unpacked** → Select the `extension/` folder  
4. The extension will appear in your toolbar.  

---

## 🎯 Usage  

1. Open any YouTube video  
2. Open the Talk2Tube side panel from the extension  
3. Paste the video link or click **“Use Current Video”**  
4. Ask your question in plain English  
5. Get AI-powered answers in real-time ✨  

---

## 📸 Demo  
<img width="1903" height="1007" alt="image" src="https://github.com/user-attachments/assets/1ea921eb-2970-4674-9795-ad06d7f41572" />

<img width="1918" height="1022" alt="image" src="https://github.com/user-attachments/assets/f2691b24-f4fc-4cd1-9fe0-2b1d1e1c915f" />


---

## 🤝 Contributing  

Contributions, issues, and feature requests are welcome!  
Feel free to open an issue or submit a pull request.  


---

## 🔗 Links  

📂 **GitHub Repo:** [Talk2Tube](https://github.com/deep74ap/Talk2Tube)  
📺 **Demo Video:** [Talk2Tube ](https://www.linkedin.com/posts/deepak0901_ai-machinelearning-langchain-activity-7370166669396291584-KALa?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAEGGdQwBpHgyGSCn7rLtEmecr5b2lmei3nc)

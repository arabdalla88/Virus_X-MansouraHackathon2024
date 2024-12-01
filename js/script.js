// إعداد السيرفر
function setupServer() {
    const cpu = document.getElementById("cpu").value;
    const ram = document.getElementById("ram").value;
    const storage = document.getElementById("storage").value;
  
    if (cpu && ram && storage) {
      addToChatLog(`Server setup with ${cpu} CPU cores, ${ram}GB RAM, and ${storage}GB storage.`);
    } else {
      alert("Please fill in all fields!");
    }
  }
  
  // إرسال الرسائل للمساعد الذكي
  function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    if (userInput) {
      addToChatLog(`User: ${userInput}`);
      getAssistantResponse(userInput);
      document.getElementById("user-input").value = ""; // تفريغ المدخل
    }
  }
  
  // ردود المساعد الذكي الذكية
  function getAssistantResponse(message) {
    let response;
  
    // تحليل الرسالة للعثور على ردود محددة
    if (message.toLowerCase().includes("recommend")) {
      response = "For optimal performance, consider using at least 4 CPU cores and 16GB RAM.";
    } else if (message.toLowerCase().includes("storage")) {
      response = "If you need more storage, consider increasing to 500GB or more.";
    } else if (message.toLowerCase().includes("security")) {
      response = "For enhanced security, enable two-factor authentication and use strong passwords.";
    } else if (message.toLowerCase().includes("hello") || message.toLowerCase().includes("hi")) {
      response = "Hello! How can I assist you with your server setup?";
    } else {
      response = "I'm here to help! Ask me anything about server setup or optimization.";
    }
  
    addToChatLog(`AI Assistant: ${response}`);
  }
  
  // إضافة الرسائل إلى نافذة المحادثة
  function addToChatLog(message) {
    const chatLog = document.getElementById("chat-log");
    const messageElement = document.createElement("div");
    messageElement.textContent = message;
    chatLog.appendChild(messageElement);
    chatLog.scrollTop = chatLog.scrollHeight;
  }
  
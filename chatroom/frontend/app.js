let ws = null;
let username = localStorage.getItem("username") || "";

function joinChat() {
    const nameInput = document.getElementById("username");
    const inputName = nameInput.value.trim();
    if (inputName) {
        username = inputName;
    }

    if (!username) {
        alert("请输入名字");
        return;
    }

    localStorage.setItem("username", username);

    document.getElementById("login").style.display = "none";
    document.getElementById("chat").style.display = "block";
    document.getElementById("current-user").innerText = "当前用户：" + username;

    if (ws) {
        ws.close();
    }

    ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onopen = function () {
        console.log("已连接到聊天室");
    };

    ws.onmessage = function (event) {
        const data = JSON.parse(event.data);
        addMessage(data.sender, data.content, data.timestamp);
    };

    ws.onclose = function () {
        console.log("连接已断开");
    };
}

function sendMessage() {
    const input = document.getElementById("messageInput");
    const content = input.value.trim();

    if (!content) return;

    const data = {
        sender: username,
        content: content,
        timestamp: new Date().toLocaleString()
    };

    ws.send(JSON.stringify(data));
    input.value = "";
}

function addMessage(sender, content, timestamp) {
    const messagesDiv = document.getElementById("messages");
    const msgDiv = document.createElement("div");
    msgDiv.className = "message";

    msgDiv.innerHTML = `
        <span class="name">${sender}</span>
        <span class="time">${timestamp}</span>
        <div class="content">${content}</div>
    `;

    messagesDiv.appendChild(msgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("messageInput");
    if (input) {
        input.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                sendMessage();
            }
        });
    }

    if (username) {
        joinChat();
    }
});
function logout(){
    if (ws) {
        ws.close();
    }
    localStorage.removeItem("username");
    location.reload();

}
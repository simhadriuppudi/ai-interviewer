const voiceHandler = new VoiceHandler();
const chatBox = document.getElementById('chatBox');
const micBtn = document.getElementById('micBtn');
const statusMsg = document.getElementById('statusMsg');

let isProcessing = false;
let conversationHistory = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem('token')) {
        window.location.href = 'login.html';
    }

    // Create initial context
    conversationHistory.push({ role: "system", content: "Interview started." });
});

function appendMessage(text, isUser) {
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${isUser ? 'user' : 'ai'}`;
    bubble.innerHTML = `<p>${text}</p>`;
    chatBox.appendChild(bubble);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Animate
    bubble.style.opacity = '0';
    bubble.style.transform = 'translateY(10px)';
    setTimeout(() => {
        bubble.style.transition = 'all 0.3s ease';
        bubble.style.opacity = '1';
        bubble.style.transform = 'translateY(0)';
    }, 10);

    // Track history
    conversationHistory.push({
        role: isUser ? "user" : "assistant",
        content: text
    });
}

micBtn.addEventListener('click', () => {
    if (isProcessing) return;

    if (!voiceHandler.isListening) {
        voiceHandler.startListening(
            (transcript) => {
                handleUserInput(transcript);
            },
            () => {
                updateMicUI(false);
            }
        );
        updateMicUI(true);
        statusMsg.textContent = "Listening...";
    } else {
        voiceHandler.stopListening();
        updateMicUI(false);
        statusMsg.textContent = "Processing...";
    }
});

function updateMicUI(listening) {
    if (listening) {
        micBtn.classList.add('listening');
        micBtn.innerHTML = '<i class="fa-solid fa-microphone-lines"></i>';
    } else {
        micBtn.classList.remove('listening');
        micBtn.innerHTML = '<i class="fa-solid fa-microphone"></i>';
    }
}

async function handleUserInput(text) {
    voiceHandler.stopListening();
    updateMicUI(false);

    if (!text || text.trim() === "") return;

    appendMessage(text, true);
    isProcessing = true;
    statusMsg.textContent = "AI is thinking...";
    micBtn.disabled = true;

    try {
        const response = await apiRequest('/interview/chat', 'POST', { message: text });

        if (response && response.response) {
            const aiText = response.response;
            appendMessage(aiText, false);

            statusMsg.textContent = "Speaking...";
            micBtn.classList.add('speaking');

            voiceHandler.speaking(aiText, () => {
                micBtn.classList.remove('speaking');
                statusMsg.textContent = "Your turn";
                micBtn.disabled = false;
                isProcessing = false;
            });
        }
    } catch (error) {
        console.error(error);
        statusMsg.textContent = "Error occurred";
        micBtn.disabled = false;
        isProcessing = false;
    }
}

// End Interview Handler
function endInterview() {
    localStorage.setItem("interviewHistory", JSON.stringify(conversationHistory));
    window.location.href = "report.html";
}

// Bind End Interview Button (assuming it's the one in nav)
document.querySelector('.btn-secondary').onclick = endInterview;

VoiceHandler.prototype.speaking = function (text, onEnd) {
    this.speak(text, onEnd);
}

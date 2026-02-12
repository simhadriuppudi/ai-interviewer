// Interview Page - Voice-Enabled Interview Logic

const API_BASE = 'http://localhost:8000/api/v1';
let interviewId = null;
let questionCount = 0;
let recognition = null;
let isListening = false;
let startTime = null;
let timerInterval = null;

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const micButton = document.getElementById('micButton');
const voiceStatus = document.getElementById('voiceStatus');
const listeningIndicator = document.getElementById('listeningIndicator');
const speakingIndicator = document.getElementById('speakingIndicator');
const questionCountEl = document.getElementById('questionCount');
const interviewTypeEl = document.getElementById('interviewType');
const timerEl = document.getElementById('timer');
const endInterviewBtn = document.getElementById('endInterviewBtn');
const ttsAudio = document.getElementById('ttsAudio');
const answerInput = document.getElementById('answerInput');
const submitAnswerBtn = document.getElementById('submitAnswerBtn');

// Initialize Speech Recognition
function initSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = true;  // Changed to true for continuous listening
        recognition.interimResults = true;  // Changed to true to show interim results
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            isListening = true;
            micButton.classList.add('listening');
            listeningIndicator.style.display = 'block';
            voiceStatus.textContent = 'Listening... Speak your answer';
        };

        recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            // Process all results
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }

            // Update the answer input with the transcript
            const currentAnswer = answerInput.value;
            if (finalTranscript) {
                answerInput.value = currentAnswer + finalTranscript;
            }

            // Show interim results in status
            if (interimTranscript) {
                voiceStatus.textContent = 'Recognizing: ' + interimTranscript;
            }

            console.log('Final:', finalTranscript, 'Interim:', interimTranscript);
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            voiceStatus.textContent = 'Error: ' + event.error;
            stopListening();
        };

        recognition.onend = () => {
            stopListening();
        };
    } else {
        alert('Speech recognition is not supported in your browser. Please use Chrome or Edge.');
    }
}

// Start listening
function startListening() {
    if (recognition && !isListening) {
        recognition.start();
    }
}

// Stop listening
function stopListening() {
    if (recognition && isListening) {
        recognition.stop();
    }
    isListening = false;
    micButton.classList.remove('listening');
    listeningIndicator.style.display = 'none';
    voiceStatus.textContent = 'Click microphone to speak';
}

// Toggle listening (start/stop)
function toggleListening() {
    if (isListening) {
        stopListening();
    } else {
        startListening();
    }
}

// Add message to chat
function addMessage(text, sender) {
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${sender}`;
    bubble.innerHTML = `<p>${text}</p>`;
    chatMessages.appendChild(bubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Play TTS audio
function playTTS(base64Audio) {
    if (!base64Audio) return;

    speakingIndicator.style.display = 'block';

    const audioData = `data:audio/mp3;base64,${base64Audio}`;
    ttsAudio.src = audioData;

    ttsAudio.onended = () => {
        speakingIndicator.style.display = 'none';
        voiceStatus.textContent = 'Click microphone to answer';
    };

    ttsAudio.play().catch(err => {
        console.error('Error playing audio:', err);
        speakingIndicator.style.display = 'none';
    });
}

// Submit answer manually
function submitAnswerManually() {
    const answer = answerInput.value.trim();
    if (!answer) {
        alert('Please provide an answer before submitting.');
        return;
    }

    // Display user's answer in chat
    addMessage(answer, 'user');

    // Submit to backend
    submitAnswer(answer);

    // Clear the input
    answerInput.value = '';

    // Stop listening if active
    if (isListening) {
        stopListening();
    }
}

// Start interview
async function startInterview() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    // Get interview ID from URL or session storage
    const urlParams = new URLSearchParams(window.location.search);
    interviewId = urlParams.get('id') || sessionStorage.getItem('interviewId');

    if (!interviewId) {
        alert('No interview ID found. Please set up an interview first.');
        window.location.href = 'dashboard.html';
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/interview/start?interview_id=${interviewId}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to start interview');
        }

        const data = await response.json();

        // Display first question
        addMessage(data.first_question, 'ai');

        // Play TTS if available
        if (data.audio_base64) {
            playTTS(data.audio_base64);
        }

        // Update UI
        questionCount = 1;
        updateQuestionCount();

        // Start timer
        startTimer();

    } catch (error) {
        console.error('Error starting interview:', error);
        alert('Failed to start interview. Please try again.');
    }
}

// Submit answer
async function submitAnswer(answerText) {
    const token = localStorage.getItem('token');

    try {
        voiceStatus.textContent = 'Processing your answer...';

        const response = await fetch(`${API_BASE}/interview/answer`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                interview_id: interviewId,
                answer: answerText
            })
        });

        if (!response.ok) {
            throw new Error('Failed to submit answer');
        }

        const data = await response.json();

        if (data.is_complete) {
            // Interview is complete
            endInterview();
        } else {
            // Display next question
            addMessage(data.next_question, 'ai');

            // Play TTS
            if (data.audio_base64) {
                playTTS(data.audio_base64);
            }

            // Update question count
            questionCount++;
            updateQuestionCount();

            voiceStatus.textContent = 'Click microphone to answer';
        }

    } catch (error) {
        console.error('Error submitting answer:', error);
        voiceStatus.textContent = 'Error submitting answer. Please try again.';
    }
}

// End interview
async function endInterview() {
    const token = localStorage.getItem('token');

    try {
        const response = await fetch(`${API_BASE}/interview/end?interview_id=${interviewId}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to end interview');
        }

        const data = await response.json();

        // Store report data
        sessionStorage.setItem('performanceReport', JSON.stringify(data.performance_report));
        sessionStorage.setItem('interviewId', interviewId);

        // Redirect to report page
        window.location.href = `report.html?id=${interviewId}`;

    } catch (error) {
        console.error('Error ending interview:', error);
        alert('Failed to end interview. Please try again.');
    }
}

// Update question count display
function updateQuestionCount() {
    questionCountEl.textContent = `${questionCount}`;
}

// Start timer
function startTimer() {
    startTime = Date.now();
    timerInterval = setInterval(() => {
        const elapsed = Date.now() - startTime;
        const minutes = Math.floor(elapsed / 60000);
        const seconds = Math.floor((elapsed % 60000) / 1000);
        timerEl.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }, 1000);
}

// Event Listeners
micButton.addEventListener('click', toggleListening);

submitAnswerBtn.addEventListener('click', submitAnswerManually);

// Allow Enter key to submit (Ctrl+Enter for new line)
answerInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.ctrlKey && !e.shiftKey) {
        e.preventDefault();
        submitAnswerManually();
    }
});

endInterviewBtn.addEventListener('click', endInterview);

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initSpeechRecognition();
    startInterview();

    // Get interview type from session storage
    const interviewType = sessionStorage.getItem('interviewType') || 'General';
    interviewTypeEl.textContent = interviewType;
});

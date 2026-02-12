class VoiceHandler {
    constructor() {
        this.synth = window.speechSynthesis;
        this.recognition = null;
        this.isListening = false;

        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.lang = 'en-US';
            this.recognition.interimResults = false;
        } else {
            alert("Speech Recognition not supported in this browser. Please use Chrome.");
        }
    }

    speak(text, onEndCallback) {
        if (this.synth.speaking) {
            console.error('speechSynthesis.speaking');
            return;
        }

        // Strip markdown-ish characters for cleaner speech
        const cleanText = text.replace(/[*_#]/g, '');

        const utterThis = new SpeechSynthesisUtterance(cleanText);

        // Select a good voice if available
        const voices = this.synth.getVoices();
        const preferredVoice = voices.find(v => v.name.includes('Google US English') || v.name.includes('Samantha'));
        if (preferredVoice) utterThis.voice = preferredVoice;

        utterThis.onend = () => {
            if (onEndCallback) onEndCallback();
        };

        utterThis.onerror = (e) => {
            console.error('Speech synthesis error', e);
        };

        this.synth.speak(utterThis);
    }

    startListening(onResultCallback, onEndCallback) {
        if (!this.recognition) return;

        if (this.isListening) {
            this.recognition.stop();
            return;
        }

        this.recognition.onstart = () => {
            this.isListening = true;
        };

        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            onResultCallback(transcript);
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            this.isListening = false;
        };

        this.recognition.onend = () => {
            this.isListening = false;
            if (onEndCallback) onEndCallback();
        };

        this.recognition.start();
    }

    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
    }
}

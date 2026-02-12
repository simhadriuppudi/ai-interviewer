// Main Frontend Logic
console.log("AI Interviewer Loaded");

// Animation for chat bubbles
document.addEventListener('DOMContentLoaded', () => {
    const bubbles = document.querySelectorAll('.chat-bubble');
    bubbles.forEach((bubble, index) => {
        bubble.style.opacity = '0';
        bubble.style.transform = 'translateY(20px)';
        setTimeout(() => {
            bubble.style.transition = 'all 0.5s ease';
            bubble.style.opacity = '1';
            bubble.style.transform = 'translateY(0)';
        }, 300 * (index + 1));
    });
});

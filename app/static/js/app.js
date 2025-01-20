// JavaScript functionality for the chat interface

document.addEventListener('DOMContentLoaded', function () {
  const createContentButton = document.getElementById('create-content');
  const refineIdeaButton = document.getElementById('refine-idea');
  const chatWindow = document.getElementById('chat-window');
  const inputField = document.getElementById('message-input');
  const sendButton = document.getElementById('send-button');

  function addMessage(content, isUser = true) {
    const messageBubble = document.createElement('div');
    messageBubble.className = isUser ? 'user-message message-bubble' : 'ai-response message-bubble';
    messageBubble.textContent = content;
    chatWindow.appendChild(messageBubble);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  function showTypingAnimation() {
    const typingBubble = document.createElement('div');
    typingBubble.className = 'ai-response message-bubble';
    typingBubble.textContent = '...';
    chatWindow.appendChild(typingBubble);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return typingBubble;
  }

  function removeTypingAnimation(typingBubble) {
    chatWindow.removeChild(typingBubble);
  }

  createContentButton.addEventListener('click', function () {
    addMessage("Let's brainstorm content ideas!", false);
  });

  refineIdeaButton.addEventListener('click', function () {
    addMessage("Tell me your content idea, and I’ll help improve it.", false);
  });

  sendButton.addEventListener('click', function () {
    const userMessage = inputField.value.trim();
    if (userMessage) {
      addMessage(userMessage);
      inputField.value = '';

      const typingBubble = showTypingAnimation();

      // Simulate AI response
      setTimeout(() => {
        removeTypingAnimation(typingBubble);
        addMessage("This is a simulated AI response.", false);
      }, 2000);
    }
  });
});

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');

    function formatAIResponse(text) {
        // Remove any extra ** symbols
        text = text.replace(/\*\*/g, '');
        
        // Split into paragraphs
        const paragraphs = text.split('\n\n').filter(p => p.trim());
        
        const formattedDiv = document.createElement('div');
        formattedDiv.className = 'space-y-4';
        
        paragraphs.forEach(paragraph => {
            // Check if paragraph is a list
            if (paragraph.includes('\n-') || paragraph.includes('\n•')) {
                // Create list container
                const listContainer = document.createElement('div');
                listContainer.className = 'space-y-2';
                
                // Split into list items
                const items = paragraph.split('\n').filter(item => item.trim());
                
                items.forEach(item => {
                    if (item.startsWith('- ') || item.startsWith('• ')) {
                        // This is a list item
                        const listItem = document.createElement('div');
                        listItem.className = 'flex items-start';
                        
                        const bullet = document.createElement('span');
                        bullet.className = 'mr-2';
                        bullet.textContent = '•';
                        
                        const content = document.createElement('span');
                        content.textContent = item.replace(/^[-•]\s*/, '');
                        
                        listItem.appendChild(bullet);
                        listItem.appendChild(content);
                        listContainer.appendChild(listItem);
                    } else {
                        // This is a header or normal text
                        const text = document.createElement('div');
                        text.className = 'font-medium';
                        text.textContent = item;
                        listContainer.appendChild(text);
                    }
                });
                
                formattedDiv.appendChild(listContainer);
            } else {
                // Regular paragraph
                const p = document.createElement('div');
                p.textContent = paragraph;
                formattedDiv.appendChild(p);
            }
        });
        
        return formattedDiv;
    }

    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `p-4 rounded-lg ${isUser ? 'bg-blue-100 ml-12' : 'bg-gray-100 mr-12'} mb-4`;
        
        const roleSpan = document.createElement('div');
        roleSpan.className = 'font-semibold mb-2 text-sm text-gray-600';
        roleSpan.textContent = isUser ? 'You' : 'ContentCoach';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'text-gray-800';
        
        if (isUser) {
            contentDiv.textContent = content;
        } else {
            contentDiv.appendChild(formatAIResponse(content));
        }
        
        messageDiv.appendChild(roleSpan);
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage(message, true);
        messageInput.value = '';

        try {
            console.log('Sending message:', message);
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'message': message
                })
            });

            console.log('Response status:', response.status);
            const data = await response.json();
            console.log('Response data:', data);
            
            if (data.error) {
                console.error('Server error:', data.error);
                addMessage(`Error: ${data.error}`);
            } else if (data.response) {
                console.log('Received response:', data.response);
                addMessage(data.response);
            } else {
                console.error('Unexpected response format:', data);
                addMessage('Received an unexpected response format from the server.');
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your request. Please try again.');
        }
    });
});

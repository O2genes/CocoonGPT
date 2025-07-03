// CocoonGPT - Hyperbaric Oxygen Therapy Assistant
// Main JavaScript functionality

class CocoonGPT {
    constructor() {
        this.apiUrl = '/chat';  // Use local Flask backend
        this.userRole = null;
        this.sessionId = this.generateSessionId();
        this.isInitialized = false;
        

        
        this.init();
    }

    // Initialize the application
    init() {
        this.initializeDOM();
        this.setupEventListeners();
        this.startLoadingSequence();
        this.initializeOxygenEffect();
        this.displayInitialTimestamp();
    }

    // Initialize DOM elements and references
    initializeDOM() {
        this.elements = {
            loadingOverlay: document.getElementById('loadingOverlay'),
            chatMessages: document.getElementById('chatMessages'),
            messageInput: document.getElementById('messageInput'),
            sendButton: document.getElementById('sendButton'),
            inputStatus: document.getElementById('inputStatus'),
            clearChatBtn: document.getElementById('clearChat'),
            exportChatBtn: document.getElementById('exportChat'),
            toastContainer: document.getElementById('toastContainer')
        };
    }

    // Setup all event listeners
    setupEventListeners() {
        // Role selection buttons
        document.querySelectorAll('.role-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.selectRole(e.target.dataset.role));
        });

        // Send message functionality
        this.elements.sendButton.addEventListener('click', () => this.sendMessage());
        this.elements.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        this.elements.messageInput.addEventListener('input', this.autoResizeTextarea);

        // Chat controls
        this.elements.clearChatBtn.addEventListener('click', () => this.clearChat());
        this.elements.exportChatBtn.addEventListener('click', () => this.exportChat());

        // Window resize handler
        window.addEventListener('resize', this.handleResize.bind(this));
    }

    // Generate a unique session ID
    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }

    // Role selection handler
    selectRole(role) {
        this.userRole = role;
        
        // Update visual feedback
        document.querySelectorAll('.role-btn').forEach(btn => {
            btn.classList.remove('selected');
        });
        document.querySelector(`[data-role="${role}"]`).classList.add('selected');

        // Enable chat input
        this.elements.messageInput.disabled = false;
        this.elements.sendButton.disabled = false;
        this.elements.inputStatus.textContent = `Selected role: ${role.charAt(0).toUpperCase() + role.slice(1)}`;

        // Add role confirmation message
        this.addMessage('assistant', `Thank you for selecting your role as ${role}. I'm CocoonGPT, your professional HBOT assistant. How can I help you today?`);

        // Focus on input
        this.elements.messageInput.focus();

        this.showToast(`Role selected: ${role.charAt(0).toUpperCase() + role.slice(1)}`);
    }

    // Send message to OpenAI API
    async sendMessage() {
        const message = this.elements.messageInput.value.trim();
        if (!message || !this.userRole) return;

        // Disable input while processing
        this.setInputState(false);

        // Add user message to chat
        this.addMessage('user', message);
        
        // Clear input
        this.elements.messageInput.value = '';
        this.autoResizeTextarea();

        try {
            // Show typing indicator
            this.showTypingIndicator();

            // Call Flask backend API
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    user_role: this.userRole,
                    session_id: this.sessionId
                })
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
            
            if (data.status === 'error') {
                throw new Error(data.error || 'Unknown error occurred');
            }

            const assistantMessage = data.response;

            // Remove typing indicator
            this.hideTypingIndicator();

            // Add assistant response
            this.addMessage('assistant', assistantMessage);

        } catch (error) {
            console.error('Error calling OpenAI API:', error);
            
            // Remove typing indicator
            this.hideTypingIndicator();
            
            // Show error message
            this.addMessage('assistant', 'I apologize, but I\'m having trouble connecting right now. Please try again in a moment. If you have an emergency, please use the emergency stop button or contact support immediately.');
            
            this.showToast('Connection error. Please try again.', 'error');
        } finally {
            // Re-enable input
            this.setInputState(true);
        }
    }

    // Add message to chat interface
    addMessage(sender, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message fade-in`;

        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = sender === 'user' ? 
            (this.userRole === 'user' ? '<i class="fas fa-user"></i>' : 
             this.userRole === 'clinic staff' ? '<i class="fas fa-user-md"></i>' : 
             '<i class="fas fa-cogs"></i>') : 
            '<i class="fas fa-robot"></i>';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.innerHTML = this.formatMessage(content);

        const timestampDiv = document.createElement('div');
        timestampDiv.className = 'message-timestamp';
        timestampDiv.textContent = new Date().toLocaleTimeString();

        contentDiv.appendChild(textDiv);
        contentDiv.appendChild(timestampDiv);
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);

        this.elements.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    // Format message content (handle line breaks, etc.)
    formatMessage(content) {
        return content
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }

    // Show typing indicator
    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant-message typing-indicator';
        typingDiv.id = 'typing-indicator';

        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = '<i class="fas fa-robot"></i>';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = `
            <div class="message-text">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;

        typingDiv.appendChild(avatarDiv);
        typingDiv.appendChild(contentDiv);
        this.elements.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();

        // Add typing animation CSS if not already present
        if (!document.querySelector('#typing-animation-css')) {
            const style = document.createElement('style');
            style.id = 'typing-animation-css';
            style.textContent = `
                .typing-dots {
                    display: flex;
                    gap: 4px;
                    align-items: center;
                }
                .typing-dots span {
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background-color: var(--primary-green);
                    animation: typing 1.4s infinite ease-in-out both;
                }
                .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
                .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
                @keyframes typing {
                    0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
                    40% { transform: scale(1); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }
    }

    // Hide typing indicator
    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    // Control input state
    setInputState(enabled) {
        this.elements.messageInput.disabled = !enabled;
        this.elements.sendButton.disabled = !enabled;
        
        if (enabled) {
            this.elements.inputStatus.textContent = `Selected role: ${this.userRole.charAt(0).toUpperCase() + this.userRole.slice(1)}`;
            this.elements.messageInput.focus();
        } else {
            this.elements.inputStatus.textContent = 'CocoonGPT is thinking...';
        }
    }

    // Auto-resize textarea
    autoResizeTextarea() {
        const textarea = document.getElementById('messageInput');
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 100) + 'px';
    }

    // Clear chat history
    async clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            try {
                // Call backend to reset conversation
                const response = await fetch('/reset', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        session_id: this.sessionId
                    })
                });

                if (response.ok) {
                    this.elements.chatMessages.innerHTML = '';
                    
                    // Re-add initial message
                    this.addMessage('assistant', `Welcome to CocoonGPT - Your Professional Hyperbaric Oxygen Therapy Assistant.

Before we begin, please tell me: **What's your role?**

<div class="role-buttons">
    <button class="role-btn" data-role="user">
        <i class="fas fa-user"></i>
        User/Patient
    </button>
    <button class="role-btn" data-role="clinic staff">
        <i class="fas fa-user-md"></i>
        Clinic Staff
    </button>
    <button class="role-btn" data-role="operator">
        <i class="fas fa-cogs"></i>
        Operator
    </button>
</div>`);

                    // Reset role selection
                    this.userRole = null;
                    this.elements.messageInput.disabled = true;
                    this.elements.sendButton.disabled = true;
                    this.elements.inputStatus.textContent = 'Please select your role first';

                    // Re-setup role button listeners
                    document.querySelectorAll('.role-btn').forEach(btn => {
                        btn.addEventListener('click', (e) => this.selectRole(e.target.dataset.role));
                    });

                    this.showToast('Chat cleared');
                } else {
                    throw new Error('Failed to reset conversation');
                }
            } catch (error) {
                console.error('Error clearing chat:', error);
                this.showToast('Error clearing chat history', 'error');
            }
        }
    }

    // Export chat history
    exportChat() {
        // Get all chat messages from the DOM
        const messages = Array.from(this.elements.chatMessages.querySelectorAll('.message')).map(msg => {
            const isUser = msg.classList.contains('user-message');
            const content = msg.querySelector('.message-text').textContent;
            const timestamp = msg.querySelector('.message-timestamp').textContent;
            return {
                role: isUser ? 'user' : 'assistant',
                content: content,
                timestamp: timestamp
            };
        });

        const chatData = {
            timestamp: new Date().toISOString(),
            userRole: this.userRole,
            sessionId: this.sessionId,
            messages: messages
        };

        const dataStr = JSON.stringify(chatData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `cocoongpt-chat-${new Date().toISOString().split('T')[0]}.json`;
        link.click();

        this.showToast('Chat exported successfully');
    }

    // Scroll chat to bottom
    scrollToBottom() {
        this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
    }

    // Loading sequence
    startLoadingSequence() {
        setTimeout(() => {
            if (this.elements.loadingOverlay) {
                this.elements.loadingOverlay.style.opacity = '0';
                setTimeout(() => {
                    this.elements.loadingOverlay.style.display = 'none';
                    this.isInitialized = true;
                }, 1000);
            }
        }, 2000);
    }

    // Initialize oxygen bubble effect
    initializeOxygenEffect() {
        const createOxygenBackground = () => {
            let oxygenBg = document.querySelector('.oxygen-bg');
            if (!oxygenBg) {
                oxygenBg = document.createElement('div');
                oxygenBg.className = 'oxygen-bg';
                document.body.appendChild(oxygenBg);
            }
            return oxygenBg;
        };

        const generateBubbles = () => {
            const oxygenBg = createOxygenBackground();
            
            // Clear existing bubbles periodically to prevent memory issues
            if (oxygenBg.children.length > 50) {
                Array.from(oxygenBg.children).slice(0, 25).forEach(child => child.remove());
            }

            // Create bubbles
            for (let i = 0; i < 8; i++) {
                const bubble = document.createElement('div');
                bubble.className = 'bubble';
                
                const size = Math.random() * 60 + 20;
                const left = Math.random() * 100;
                const duration = Math.random() * 8 + 12;
                const delay = Math.random() * 10;
                
                bubble.style.width = `${size}px`;
                bubble.style.height = `${size}px`;
                bubble.style.left = `${left}%`;
                bubble.style.animationDuration = `${duration}s`;
                bubble.style.animationDelay = `${delay}s`;
                
                oxygenBg.appendChild(bubble);
                
                // Remove bubble after animation
                setTimeout(() => {
                    if (bubble.parentNode) {
                        bubble.remove();
                    }
                }, (duration + delay) * 1000);
            }

            // Create particles
            for (let i = 0; i < 15; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                
                const size = Math.random() * 8 + 3;
                const startX = Math.random() * 100;
                const startY = Math.random() * 100;
                const xMove = (Math.random() - 0.5) * 200;
                const yMove = (Math.random() - 0.5) * 200;
                const duration = Math.random() * 8 + 8;
                const delay = Math.random() * 5;
                
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                particle.style.left = `${startX}%`;
                particle.style.top = `${startY}%`;
                particle.style.setProperty('--x', `${xMove}px`);
                particle.style.setProperty('--y', `${yMove}px`);
                particle.style.animationDuration = `${duration}s`;
                particle.style.animationDelay = `${delay}s`;
                
                oxygenBg.appendChild(particle);
                
                // Remove particle after animation
                setTimeout(() => {
                    if (particle.parentNode) {
                        particle.remove();
                    }
                }, (duration + delay) * 1000);
            }
        };

        // Generate initial bubbles
        generateBubbles();
        
        // Continue generating bubbles
        setInterval(generateBubbles, 8000);
    }



    // Display initial timestamp
    displayInitialTimestamp() {
        const timestampElement = document.getElementById('initialTimestamp');
        if (timestampElement) {
            timestampElement.textContent = new Date().toLocaleTimeString();
        }
    }

    // Show toast notification
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        this.elements.toastContainer.appendChild(toast);
        
        setTimeout(() => {
            if (this.elements.toastContainer.contains(toast)) {
                this.elements.toastContainer.removeChild(toast);
            }
        }, 3000);
    }

    // Handle window resize
    handleResize() {
        // Adjust chat height on mobile
        if (window.innerWidth <= 768) {
            const vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', `${vh}px`);
        }
    }


}

// Initialize CocoonGPT when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the main application
    window.cocoonGPT = new CocoonGPT();
    


    // Add mobile viewport height fix
    const setVH = () => {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    };
    
    setVH();
    window.addEventListener('resize', setVH);
    window.addEventListener('orientationchange', setVH);

    // Add performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log(`CocoonGPT loaded in ${Math.round(perfData.loadEventEnd - perfData.loadEventStart)}ms`);
            }, 0);
        });
    }

    // Service worker registration for offline functionality (if available)
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').catch(err => {
            console.log('Service worker registration failed:', err);
        });
    }
});

// Export for global access
window.CocoonGPT = CocoonGPT;
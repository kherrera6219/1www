$(document).ready(function() {
    const chatContainer = $('#chat-container');
    const chatForm = $('#chat-form');
    const userInput = $('#user-input');
    const feedbackBtn = $('#feedback-btn');
    const clearChatBtn = $('#clear-chat');
    const themeToggleBtn = $('#theme-toggle');
    const charCount = $('#char-count');
    const maxChars = 500;

    function addMessage(message, isUser = false, extras = {}) {
        const messageClass = isUser ? 'user-message' : 'bot-message';
        const avatar = isUser ? '👤' : '🤖';
        const timestamp = new Date().toLocaleTimeString();
        let messageHtml = `
            <div class="d-flex ${messageClass} message">
                <div class="avatar">${avatar}</div>
                <div>
                    <div class="message-content">${message}</div>
                    <div class="timestamp">${timestamp}</div>
        `;

        if (!isUser && extras) {
            messageHtml += '<div class="extras">';
            if (extras.intent) {
                messageHtml += `<div><strong>Intent:</strong> ${extras.intent}</div>`;
            }
            if (extras.entities && extras.entities.length > 0) {
                messageHtml += `<div><strong>Entities:</strong> ${extras.entities.map(e => e.text).join(', ')}</div>`;
            }
            if (extras.noun_phrases && extras.noun_phrases.length > 0) {
                messageHtml += `<div><strong>Noun Phrases:</strong> ${extras.noun_phrases.map(np => np.text).join(', ')}</div>`;
            }
            if (extras.sentiment) {
                messageHtml += `<div><strong>Sentiment:</strong> Polarity: ${extras.sentiment.polarity.toFixed(2)}, Subjectivity: ${extras.sentiment.subjectivity.toFixed(2)}</div>`;
            }
            messageHtml += '</div>';
        }

        messageHtml += `
                </div>
            </div>
        `;
        chatContainer.append(messageHtml);
        scrollToBottom();
    }

    function scrollToBottom() {
        chatContainer.animate({ scrollTop: chatContainer[0].scrollHeight }, 300);
    }

    function showTypingIndicator() {
        chatContainer.append(`
            <div class="bot-message message typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        $('.typing-indicator').remove();
    }

    chatForm.on('submit', function(e) {
        e.preventDefault();
        const message = userInput.val().trim();
        if (message) {
            addMessage(message, true);
            userInput.val('');
            updateCharCount();

            showTypingIndicator();

            $.ajax({
                url: '/get_response',
                method: 'POST',
                data: { message: message },
                timeout: 60000, // Increase timeout to 60 seconds
                success: function(data) {
                    removeTypingIndicator();
                    addMessage(data.response, false, {
                        intent: data.intent,
                        entities: data.entities,
                        noun_phrases: data.noun_phrases,
                        sentiment: data.sentiment
                    });
                },
                error: function(xhr, status, error) {
                    removeTypingIndicator();
                    console.error("Error:", error);
                    let errorMessage = "Sorry, there was an error processing your request. Please try again later.";
                    if (status === "timeout") {
                        errorMessage = "The request is taking longer than expected. Please try again or rephrase your question.";
                    }
                    addMessage(errorMessage, false);
                }
            });
        }
    });

    feedbackBtn.on('click', function() {
        const feedbackMessage = prompt("Please provide your feedback or report an issue:");
        if (feedbackMessage) {
            alert("Thank you for your feedback! We'll review it to improve our chatbot.");
            // Here you can implement sending the feedback to a server endpoint if needed
        }
    });

    clearChatBtn.on('click', function() {
        chatContainer.empty();
    });

    themeToggleBtn.on('click', function() {
        $('html').attr('data-bs-theme', function(i, val) {
            return val === 'dark' ? 'light' : 'dark';
        });
    });

    userInput.on('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        updateCharCount();
    });

    function updateCharCount() {
        const currentChars = userInput.val().length;
        charCount.text(`${currentChars}/${maxChars}`);
        if (currentChars > maxChars) {
            charCount.addClass('text-danger');
        } else {
            charCount.removeClass('text-danger');
        }
    }

    // Initialize
    updateCharCount();
});

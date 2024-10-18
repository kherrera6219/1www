$(document).ready(function() {
    const chatContainer = $('#chat-container');
    const chatForm = $('#chat-form');
    const userInput = $('#user-input');
    const feedbackBtn = $('#feedback-btn');

    function addMessage(message, isUser = false) {
        const messageClass = isUser ? 'justify-content-end' : 'justify-content-start';
        const messageBg = isUser ? 'bg-primary' : 'bg-secondary';
        chatContainer.append(`
            <div class="d-flex ${messageClass} mb-2">
                <div class="d-inline-block ${messageBg} rounded p-2 text-break" style="max-width: 75%;">
                    ${message}
                </div>
            </div>
        `);
        chatContainer.scrollTop(chatContainer[0].scrollHeight);
    }

    chatForm.on('submit', function(e) {
        e.preventDefault();
        const message = userInput.val().trim();
        if (message) {
            addMessage(message, true);
            userInput.val('');

            $.ajax({
                url: '/get_response',
                method: 'POST',
                data: { message: message },
                success: function(data) {
                    addMessage(data.response);
                },
                error: function(xhr, status, error) {
                    console.error("Error:", error);
                    addMessage("Sorry, there was an error processing your request. Please try again later.");
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
});

$(document).ready(function() {
    const chatContainer = $('#chat-container');
    const chatForm = $('#chat-form');
    const userInput = $('#user-input');

    function addMessage(message, isUser = false) {
        const messageClass = isUser ? 'text-end' : 'text-start';
        const messageBg = isUser ? 'bg-primary' : 'bg-secondary';
        chatContainer.append(`
            <div class="${messageClass} mb-2">
                <span class="d-inline-block ${messageBg} rounded p-2">
                    ${message}
                </span>
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
                error: function() {
                    addMessage("Sorry, there was an error processing your request.");
                }
            });
        }
    });
});

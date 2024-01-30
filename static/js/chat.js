// document.getElementById('getAnimeDetailsButton').addEventListener('click', function() {
//     // Handle "Get Anime Details" button click
//     // Redirect to the appropriate page
//     window.location.href = 'recommend_anime.html';
// });

// document.getElementById('animeRecommendationsButton').addEventListener('click', function() {
//     // Handle "Anime Recommendations" button click
//     // Redirect to the appropriate page
//     window.location.href = 'recommend_tags.html';
// });

document.getElementById('exitButton').addEventListener('click', function() {
    // Handle "Exit" button click
    // Redirect to the main page
    window.location.href = '/';
});

// Add event listeners for other buttons as needed
document.getElementById('sendButton').addEventListener('click', function() {
    var userInput = document.getElementById('userInput').value;

    // Display the user's message
    var userMessageElement = document.createElement('div');
    userMessageElement.className = 'user-message';
    userMessageElement.innerHTML = 'User: ' + userInput;
    document.getElementById('chatbox').appendChild(userMessageElement);

    // Send the user's message to the server
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'user_input': userInput }),
    })
    .then(response => response.json())
    .then(data => {
        // Display the chatbot's response
        var response = data.response;
        var lines = response.split('\n'); // Split the response into lines
        var output = '';
        lines.forEach(line => {
            if (line.trim() !== '') { // Skip empty lines
                var parts = line.split(': '); // Split each line into key-value pairs
                if (parts[0] === 'Picture') {
                    // Display the picture
                    var imageUrl = parts[1].replace(/[\[\]']+/g, '');
                    output += '<img src="' + imageUrl + '" alt="Anime Image"><br>';
                } else if (parts[0] === 'Primary Source') {
                    // Display the primary source link
                    var sourceUrl = parts[1].replace(/[\[\]']+/g, ''); // Remove square brackets
                    output += 'Primary Source: <a href="' + sourceUrl.trim() + '">Link</a><br>';
                } else {
                    output += line + '<br>';
                }
            }
        });
        var chatbotMessageElement = document.createElement('div');
        chatbotMessageElement.className = 'chatbot-message';
        chatbotMessageElement.innerHTML = output;
        document.getElementById('chatbox').appendChild(chatbotMessageElement);

        // Clear the user's input
        document.getElementById('userInput').value = '';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Make the send button work when the enter key is pressed
document.getElementById('userInput').addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        document.getElementById('sendButton').click();
    }
});
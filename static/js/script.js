document.getElementById('getAnimeDetailsButton').addEventListener('click', function() {
    // Handle "Get Anime Details" button click
    // Redirect to the appropriate page
    window.location.href = 'recommend_anime.html';
});

document.getElementById('animeRecommendationsButton').addEventListener('click', function() {
    // Handle "Anime Recommendations" button click
    // Redirect to the appropriate page
    window.location.href = 'recommend_tags.html';
});

document.getElementById('exitButton').addEventListener('click', function() {
    // Handle "Exit" button click
    // Redirect to the main page
    window.location.href = 'index.html';
});

// Add event listeners for other buttons as needed

document.getElementById('sendButton').addEventListener('click', function() {
    var userInput = document.getElementById('userInput').value;

    // Display the user's message
    document.getElementById('chatbox').innerHTML += 'User: ' + userInput + '<br>';

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
        var details = response.split(', ');
        var output = '';
        for (var i = 0; i < details.length; i++) {
            if (details[i].startsWith('Picture:')) {
                var pictureUrl = details[i].slice(10, -2);  // Correctly extract the URL from the string
                output += '<img src="' + pictureUrl + '"><br>';
            } else if (details[i].startsWith('Primary Source:')) {
                var sourceUrl = details[i].slice(16, -2);  // Correctly extract the URL from the string
                output += 'Primary Source: <a href="' + sourceUrl + '">Link</a><br>';
            } else {
                output += details[i] + '<br>';
            }
        }
        document.getElementById('chatbox').innerHTML += 'Chatbot: <br>' + output;
    });

    // Clear the user's input
    document.getElementById('userInput').value = '';
});

// Function to handle getting anime recommendations
function getAnimeRecommendations() {
    var animeTitleInput = document.getElementById('animeTitle');
    var animeTitle = animeTitleInput.value;

    // Send a POST request to the server
    fetch('/api/recommend/anime', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'anime_title': animeTitle }),
    })
    .then(response => response.json())
    .then(data => {
        // Display the recommendations
        var recommendations = data.recommendations; // Assuming this is an array of recommendations

        // Clear any existing recommendations
        var recommendationsContainer = document.getElementById('recommendationsContainer');
        recommendationsContainer.innerHTML = '';

        recommendations.forEach(recommendation => {
            // Create a new div for the recommendation
            var recommendationElement = document.createElement('div');
            recommendationElement.className = 'recommendation';

            // Split the details string into individual properties
            var details = recommendation.details.split('\n').filter(detail => detail.trim() !== '');

            // Add the recommendation title to the div
            var titleElement = document.createElement('h2');
            titleElement.textContent = recommendation.title;
            recommendationElement.appendChild(titleElement);

            // Add details line by line
            details.forEach(detail => {
                var detailElement = document.createElement('p');
                if (detail.includes('[') && detail.includes(']')) {
                    // If detail contains square brackets, extract URL and create link
                    var url = detail.match(/\[(.*?)\]/)[1];
                    var text = detail.replace(/\[(.*?)\]/, ''); // Remove brackets from text
                    // Remove additional quotes around the URL if any
                    url = url.replace(/['"]/g, '');
                    detailElement.innerHTML = `<a href="${url}">${text}</a>`;
                } else {
                    detailElement.textContent = detail;
                }
                recommendationElement.appendChild(detailElement);
            });

            // Add the div to the recommendations container
            recommendationsContainer.appendChild(recommendationElement);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });

    // Clear the input field
    animeTitleInput.value = '';
}

// Add event listener for the button
document.getElementById('getRecommendationsButton').addEventListener('click', getAnimeRecommendations);
document.getElementById('exitButton').addEventListener('click', function() {
    // Handle "Exit" button click
    // Redirect to the main page
    window.location.href = '/';
});
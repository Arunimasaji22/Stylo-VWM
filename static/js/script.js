document.getElementById("user-input").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent default behavior of Enter key (e.g., form submission)
        sendMessage(); // Call the sendMessage function
    } else {
        updateStatusImage("{% static 'js/default.png'}"); // Update to default image while user types
    }
});

function sendMessage() {
    var userInput = document.getElementById("user-input");
    var message = userInput.value.trim();
    var loadingGif = document.getElementById("loading-gif");

    if (message !== "") {
        var chatBody = document.getElementById("chat-body");

        // Display the user's message
        var newMessage = document.createElement("div");
        newMessage.className = "message";
        newMessage.innerHTML = "<p class='user-message'>" + message + "</p>";
        chatBody.appendChild(newMessage);

        // Show the loading GIF
        loadingGif.style.display = "inline";

        // Update to 'speaking' image while waiting for bot response
        updateStatusImage("speak.gif");

        // Send the message to the server
        fetch("", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            },
            body: new URLSearchParams({
                msg: message,
            }),
        })
        .then(response => response.json())
        .then(data => {
            // Hide the loading GIF
            loadingGif.style.display = "none";

            // Display the bot's response
            var botMessage = document.createElement("div");
            botMessage.className = "message";
            botMessage.innerHTML = "<p class='bot-message'>" + data.response + "</p>";
            chatBody.appendChild(botMessage);
            chatBody.scrollTop = chatBody.scrollHeight; // Auto-scroll to the latest message

            // Revert back to default image after bot message is displayed
            updateStatusImage("default.png");
        })
        .catch(error => {
            console.error("Error:", error);
            loadingGif.style.display = "none"; // Hide the GIF in case of an error
            updateStatusImage("default.png"); // Revert to default image if there is an error
        });

        // Clear the input field
        userInput.value = "";
    }
}

function updateStatusImage(imagePath) {
    var statusImage = document.getElementById("status-image");
    statusImage.src = imagePath;
}
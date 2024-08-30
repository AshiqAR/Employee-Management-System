document.addEventListener("DOMContentLoaded", function() {
    const popupMessage = document.getElementById("pop-up-message-div");

    // Check if popupMessage exists and has children (messages)
    if (popupMessage && popupMessage.children.length > 0) {
        // Show the popup
        popupMessage.classList.add("show");

        // Hide the popup after 5 seconds
        setTimeout(function() {
            popupMessage.classList.remove("show");
        }, 3000); // Adjust this value if you want it to stay longer
    }
});

document.addEventListener("DOMContentLoaded", function() {
    const messagePopup = document.getElementById('pop-up-message-div');
    console.log("inside message_popup.js");
    if (messagePopup) {
        messagePopup.classList.add('show');
        setTimeout(function() {
            messagePopup.classList.remove('show');
        }, 5000); 
    }
});

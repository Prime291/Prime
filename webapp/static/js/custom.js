// custom.js
function buyNow(flowerId, isLoggedIn) {
    if (!isLoggedIn) {
        $('#loginModal').modal('show'); // Show login dialog
    } else {
        $('#shopNowForm_' + flowerId).submit(); // Submit the form if the user is authenticated
        $('#loginModal').modal('hide'); // Hide the modal after submitting the form
    }
}

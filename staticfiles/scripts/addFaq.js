$(document).ready(function () {
$("#faqItemsFormAdd").submit(function (e) {
    e.preventDefault(); // Prevent the default form submission

    // Add loading spinner to the button
    $("#faqItemsFormAdd button").html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Adding Faqs..');

    $.ajax({
        type: "POST",
        url: $(this).attr('action'), // Use the form's action attribute as the URL
        data: $(this).serialize(), // Serialize the form data
        dataType: 'json', // Specify that the expected response is JSON
        success: function (response) {
            if (response.success) {
                // Display success message or handle accordingly
                $("#responseFaqMsg").html('<div class="alert alert-success">' + response.message + '</div>');
            } else {
                // Display error message
                $("#responseFaqMsg").html('<div class="alert alert-danger">' + response.message + '</div>');
            }
        },
        error: function (error) {
            // Handle the error (e.g., show an error message)
            console.log(error.responseText);
        },
        complete: function () {
            // Remove loading spinner from the button
            $("#faqItemsFormAdd button").html('Add New Faq');
        },
    });
});
});
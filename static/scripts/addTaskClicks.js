$(document).ready(function () {
    $("#taskAddForm").submit(function (e) {
        e.preventDefault(); // Prevent the default form submission

        // Add loading spinner to the button
        $("#taskAddForm button").html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Adding new task..');

        var formData = new FormData(this); // Create FormData object from the form

        $.ajax({
            type: "POST",
            url: $(this).attr('action'), // Use the form's action attribute as the URL
            data: formData, // Use FormData object for data
            processData: false, // Prevent jQuery from processing the data
            contentType: false, // Prevent jQuery from setting content type
            dataType: 'json', // Specify that the expected response is JSON
            success: function (response) {
                if (response.success) {
                    // Display success message or handle accordingly
                    $("#responseTaskMsg").html('<div class="alert alert-success">' + response.message + '</div>');
                } else {
                    // Display error message
                    $("#responseTaskMsg").html('<div class="alert alert-danger">' + response.message + '</div>');
                }
            },
            error: function (error) {
                // Handle the error (e.g., show an error message)
                console.log(error.responseText);
            },
            complete: function () {
                // Remove loading spinner from the button
                $("#taskAddForm button").html('Add New Task');
            },
        });
    });
});


$(document).ready(function () {
$("#clickForm").submit(function (e) {
    e.preventDefault(); // Prevent the default form submission

    // Add loading spinner to the button
    $("#clickForm button").html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Adding Click..');

    $.ajax({
        type: "POST",
        url: $(this).attr('action'), // Use the form's action attribute as the URL
        data: $(this).serialize(), // Serialize the form data
        dataType: 'json', // Specify that the expected response is JSON
        success: function (response) {
            if (response.success) {
                // Display success message or handle accordingly
                $("#responseClickMsg").html('<div class="alert alert-success">' + response.message + '</div>');
            } else {
                // Display error message
                $("#responseClickMsg").html('<div class="alert alert-danger">' + response.message + '</div>');
            }
        },
        error: function (error) {
            // Handle the error (e.g., show an error message)
            console.log(error.responseText);
        },
        complete: function () {
            // Remove loading spinner from the button
            $("#clickForm button").html('Add New Click');
        },
    });
});
});
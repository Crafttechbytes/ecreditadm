//  $(document).ready(function() {
//        $('#loginForm').submit(function(e) {
//            e.preventDefault();
//
//            // Get form data
//            var formData = new FormData(this);
//
//            // Perform basic form validation
//            var username = formData.get('username');
//            var password = formData.get('password');
//
//            if (!username || !password) {
//                $('#error-message').html('<p style="color: red;">All fields are required.</p>');
//                return;
//            }
//
//            // Disable the submit button and set loading text
//            var submitBtn = $('#submitBtn');
//            submitBtn.prop('disabled', true);
//            submitBtn.text('Signing in...');
//
//            $.ajax({
//                type: 'POST',
//                url: $(this).attr('action'), // Use the form's action attribute as the URL
//                data: formData,
//                dataType: 'json',
//                contentType: false,
//                processData: false,
//                success: function(response) {
//                    $('#error-message').html(response.message);
//
//                    // Check if there's a 'redirect' property in the response
//                    if (response.redirect) {
//                        // Redirect to the specified URL
//                        window.location.href = response.redirect;
//                    }
//
//                },
//                error: function(error) {
//                    $('#error-message').html('<p style="color: red;">Wrong username or password.</p>');
//                    console.log(error);
//                },
//                complete: function() {
//                    // Enable the submit button and revert the text
//                    submitBtn.prop('disabled', false);
//                    submitBtn.text('Submit');
//                }
//            });
//        });
//    });

    $(document).ready(function () {
        $("#loginForm").submit(function (e) {
            e.preventDefault(); // Prevent the default form submission

            // Add loading spinner to the button
            $("#loginForm button").html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Signing in..');

            $.ajax({
                type: "POST",
                url: $(this).attr('action'), // Use the form's action attribute as the URL
                data: $(this).serialize(), // Serialize the form data
                dataType: 'json', // Specify that the expected response is JSON
                success: function (response) {
                    if (response.success) {
                        // Display success message or handle accordingly
                        $("#success-message").html('<div class="alert alert-success">' + response.message + '</div>');
                        window.location.href = response.redirect;

                    } else {
                        // Display error message
                        $("#error-message").html('<div class="alert alert-danger">' + response.message + '</div>');
                    }
                },
                error: function (error) {
                    // Handle the error (e.g., show an error message)
                    console.log(error.responseText);
                },
                complete: function () {
                    // Remove loading spinner from the button
                    $("#loginForm button").html('Sign in');
                },
            });
        });
    });

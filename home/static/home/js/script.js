$('.plus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function (data) {
            console.log("data = ", data);
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        },
        error: function (xhr, status, error) {
            console.error("Error:", error);
            // Handle the error, such as displaying an error message to the user
        }
    })
})

$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function (data) {
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        },
        error: function (xhr, status, error) {
            console.error("Error:", error);
            // Handle the error, such as displaying an error message to the user
        }
    })
})

$('.remove-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function (data) {
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        },
        error: function (xhr, status, error) {
            console.error("Error:", error);
            // Handle the error, such as displaying an error message to the user
        }
    })
})



// Wait for the document to be fully loaded
$(document).ready(function () {
    // Add event listener to show the toast when the form is submitted
    $('#add-to-cart-form').on('submit', function (event) {
        // Prevent the default form submission
        event.preventDefault();

        // Perform an AJAX request to add the product to the cart
        $.ajax({
            type: 'GET',
            url: '/add-to-cart',
            data: $(this).serialize(), // Serialize the form data
            success: function () {
                // If the request is successful, display the toast message
                console.log('Before toast initialization');
                var toast = new bootstrap.Toast(document.getElementById('toastMessage'));
                toast.show();
                console.log('After toast initialization');
            },
            error: function () {
                // If there's an error, log it to the console
                console.error('Error adding item to cart.');
            }
        });
    });
});
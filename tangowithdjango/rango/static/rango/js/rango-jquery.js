$(document).ready(function () {
    console.log("this is a test log for js import")

    $('#about-btn').click(function (event) {
        alert('Your clicked button using jQuery')
    });

    $("p").hover(function () {
            $(this).css('color', 'red');
        },
        function () {
            $(this).css('color', 'blue');
        });
    $("#about-btn").addClass('btn btn-primary');
})
$("#like").click(function () {
    var cat_id = $(this).attr("data_catid");
    $.get('/rango/like_category/', {category_id: cat_id}, function (data) {
        $("#like_count").html(data);
        $("#like").hide();
    });
});

$("#suggestion").keyup(function () {
    $.get('/rango/suggest_category/', {starts_with: $(this).val()}, function (data) {
        $("#cats").html(data)
    })
})
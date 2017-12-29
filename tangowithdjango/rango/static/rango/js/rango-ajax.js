$("#like").click(function () {
    var cat_id = $(this).attr("data_catid");
    $.get('/rango/like_category/', {category_id: cat_id}, function (data) {
        $("#like_count").html(data);
        $("#like").hide();
    })
})
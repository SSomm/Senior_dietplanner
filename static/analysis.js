$(document).ready(function(){
    $(".suggest").on("click", function(){
        $(".modal_back").show();
    });
    $(".close_pill").on("click", function(){
        $(".modal_back").hide();
    });

    $(".review").on("click", function(){
        $(".modal_back_review").show();
    });

    $(".close_pill_review").on("click", function(){
        $(".modal_back_review").hide();
    });
});
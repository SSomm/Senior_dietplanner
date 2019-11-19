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

//    $("").on("mouseover", function(){
////        $(this).css("scale", )
//    });
    // 평가 창 열기
    $(".eval").on("click", function(){
        $(".review_back").show();
    });
   //수정 창 열기
    $(".modify").on("click", function(){
        $(".review_back").show();
    });
    $(".review_close").on("click", function(){
        $(".review_back").hide();
    });
//    평가하기
    $(".review_com").on("click", function(){
        var evaluate=$("input:radio[name=satisfy]:checked").val();
        $(".fa-thumbs-up").remove();
        var eval_html=``;
        for (var i=0; i<evaluate;i++){
            eval_html+=`<i class="far fa-thumbs-up">&nbsp;</i>`;
        }
        $(".thumbsup").append(eval_html);
        $(".default_guide").text("평가가 완료되었습니다.");
        $(".review_back").hide();
    });
    //평가 취소하기
    $(".review_cancel").on("click", function(){
        $(".review_back").hide();
    });

    $(".circle1").on("mouseover", function(){
        $(".r_pointa").text("89점");
    });
     $(".circle1").on("mouseleave", function(){
        $(".r_pointa").text("");
    });

    $(".circle2").on("mouseover", function(){
        $(".r_pointb").text("89점");
    });
     $(".circle2").on("mouseleave", function(){
        $(".r_pointb").text("");
    });

     $(".circle3").on("mouseover", function(){
        $(".r_pointc").text("89점");
    });
     $(".circle3").on("mouseleave", function(){
        $(".r_pointc").text("");
    });



});

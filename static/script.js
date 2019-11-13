//(function ($) {
//    $.fakeLoader = function(options) {
//
//        var settings = $.extend({
//            targetClass:'fakeLoader',
//            timeToHide:1200,
//            bgColor: '#2ecc71',
//            spinner:'spinner2'
//        }, options);
//
//        var spinner01 = '<div class="fl fl-spinner spinner1"><div class="double-bounce1"></div><div class="double-bounce2"></div></div>';
//        var spinner02 = '<div class="fl fl-spinner spinner2"><div class="spinner-container container1"><div class="circle1"></div><div class="circle2"></div><div class="circle3"></div><div class="circle4"></div></div><div class="spinner-container container2"><div class="circle1"></div><div class="circle2"></div><div class="circle3"></div><div class="circle4"></div></div><div class="spinner-container container3"><div class="circle1"></div><div class="circle2"></div><div class="circle3"></div><div class="circle4"></div></div></div>';
//        var spinner03 = '<div class="fl fl-spinner spinner3"><div class="dot1"></div><div class="dot2"></div></div>';
//        var spinner04 = '<div class="fl fl-spinner spinner4"></div>';
//        var spinner05 = '<div class="fl fl-spinner spinner5"><div class="cube1"></div><div class="cube2"></div></div>';
//        var spinner06 = '<div class="fl fl-spinner spinner6"><div class="rect1"></div><div class="rect2"></div><div class="rect3"></div><div class="rect4"></div><div class="rect5"></div></div>';
//        var spinner07 = '<div class="fl fl-spinner spinner7"><div class="circ1"></div><div class="circ2"></div><div class="circ3"></div><div class="circ4"></div></div>';
//
//        var el = $('body').find('.' + settings.targetClass);
//
//        el.each(function() {
//            var a = settings.spinner;
//
//                switch (a) {
//                    case 'spinner1':
//                            el.html(spinner01);
//                        break;
//                    case 'spinner2':
//                            el.html(spinner02);
//                        break;
//                    case 'spinner3':
//                            el.html(spinner03);
//                        break;
//                    case 'spinner4':
//                            el.html(spinner04);
//                        break;
//                    case 'spinner5':
//                            el.html(spinner05);
//                        break;
//                    case 'spinner6':
//                            el.html(spinner06);
//                        break;
//                    case 'spinner7':
//                            el.html(spinner07);
//                        break;
//                    default:
//                        el.html(spinner01);
//                    }
//        });
//
//        el.css({
//            'backgroundColor':settings.bgColor
//        });
//
//        setTimeout(function () {
//            $(el).fadeOut();
//        }, settings.timeToHide);
//    };
//}(jQuery));
$(document).ready(function(){

    $('.check_btn').on('click', function(){
//        var gender=$('.rdgen').prop('checked').val();
//        alert(gender);
//        var age=;
//        var height=;
//        var weight=;
//        var activelevel=;
//        var check_disease=;
//        var etc_disease=;
//        location.href='result/diet_result.html';

    });
    r=$('.re_table').css('margin-left');

    //식단메뉴 슬라이딩 인터벌
    var click_index=0;
    playAlert = setInterval(function() {
       if(click_index == 0){
            $(".re_table").stop().animate({marginLeft:-778} ,10);
            click_index = 1
       }else if(click_index == 1){
            $(".re_table").stop().animate({marginLeft:-1556} ,10);
            click_index = 2;
       }else{
            $(".re_table").stop().animate({marginLeft:0} ,10);
            click_index = 0;
       }
    }, 5000);

    //아침밥 클릭시 이벤트
    $(".bre").on("click",function(){
            playAlert = setInterval(function() {
               if(click_index == 0){
                    $(".re_table").stop().animate({marginLeft:-778} ,10);
                    click_index = 1
               }else if(click_index == 1){
                    $(".re_table").stop().animate({marginLeft:-1556} ,10);
                    click_index = 2;
               }else{
                    $(".re_table").stop().animate({marginLeft:0} ,10);
                    click_index = 0;
               }
            }, 5000);
        $(".re_table").stop().animate({marginLeft:0} ,10);
        click_index=0;
    })

    //점심밥 클릭시 이벤트
    $(".lun").on("click",function(){
        playAlert = setInterval(function() {
               if(click_index == 0){
                    $(".re_table").stop().animate({marginLeft:-778} ,10);
                    click_index = 1
               }else if(click_index == 1){
                    $(".re_table").stop().animate({marginLeft:-1556} ,10);
                    click_index = 2;
               }else{
                    $(".re_table").stop().animate({marginLeft:0} ,10);
                    click_index = 0;
               }
            }, 5000);
       $(".re_table").stop().animate({marginLeft:-778} ,10);
        click_index=1;
    });
    $(".din").on("click",function(){
    //    alert("a");
        $(".re_table").stop().animate({marginLeft:-1556} ,10);
        click_index=2;
    });

//오른쪽 화살표 클릭 이벤트(슬라이딩)
    $('.right_btn').on('click', function(){
    clearInterval(playAlert);
    if(click_index == 0){
//         $(".re_table").css("margin-left","-540px");
            playAlert = setInterval(function() {
               if(click_index == 0){
                    $(".re_table").stop().animate({marginLeft:-778} ,10);
                    click_index = 1
               }else if(click_index == 1){
                    $(".re_table").stop().animate({marginLeft:-1556} ,10);
                    click_index = 2;
               }else{
                    $(".re_table").stop().animate({marginLeft:0} ,10);
                    click_index = 0;
               }
            }, 5000);
            $(".re_table").stop().animate({marginLeft:-778} ,10);
            click_index=1;
    }else if(click_index == 1){
            playAlert = setInterval(function() {
               if(click_index == 0){
                    $(".re_table").stop().animate({marginLeft:-778} ,10);
                    click_index = 1
               }else if(click_index == 1){
                    $(".re_table").stop().animate({marginLeft:-1556} ,10);
                    click_index = 2;
               }else{
                    $(".re_table").stop().animate({marginLeft:0} ,10);
                    click_index = 0;
               }
            }, 5000);
        $(".re_table").stop().animate({marginLeft:-1556} ,10);
            click_index=2;
    }

    });
    //왼쪽 화살표 버튼 클릭 이벤트
    $(".left_btn").on("click",function(){
        if(click_index == 2){
            playAlert = setInterval(function() {
               if(click_index == 0){
                    $(".re_table").stop().animate({marginLeft:-778} ,10);
                    click_index = 1
               }else if(click_index == 1){
                    $(".re_table").stop().animate({marginLeft:-1556} ,10);
                    click_index = 2;
               }else{
                    $(".re_table").stop().animate({marginLeft:0} ,10);
                    click_index = 0;
               }
            }, 5000);
            $(".re_table").stop().animate({marginLeft:-778} ,10);
            click_index=1;
        }else if(click_index == 1){
            playAlert = setInterval(function() {
               if(click_index == 0){
                    $(".re_table").stop().animate({marginLeft:-778} ,10);
                    click_index = 1
               }else if(click_index == 1){
                    $(".re_table").stop().animate({marginLeft:-1556} ,10);
                    click_index = 2;
               }else{
                    $(".re_table").stop().animate({marginLeft:0} ,10);
                    click_index = 0;
               }
            }, 5000);
            $(".re_table").stop().animate({marginLeft:0} ,10);
            click_index=0;
        }
    });

    $('.slide_btn').off('hover');

//식단분석표 클릭시
function redirectPost(url, data) {
    var form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'post';
    form.action = url;
    for (var name in data) {
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = name;
        input.value = data[name];
        form.appendChild(input);
    }
    form.submit();
}
    $(".analysis_diet").on("click", function(){
        location.href="/analysis";

    });

    //요일 바뀔 때의 변화
    $(".hover_spann").on("click", function(){
        var days=$(this).text();
        var week=$(this).data("week");
        var check=$(this).data("check");
        if(days=="월"){
            days=0;
        }else if(days=="화"){
            days=1;
        }else if(days=="수"){
            days=2;
        }else if(days=='목'){
            days=3;
        }else if(days=='금'){
            days=4;
        }else if(days=='토'){
            days=5;
        }else{
            days=6
        }
       location.href='/result'+'?days='+days+'&check='+check+"&week="+week;

    });

    $(".week_change").on("click", function(){
        var days=$(this).data("days");
        var check=$(this).data("check");
        var week=$(this).data("week");
        if(days=="월"){
            days=0;
        }else if(days=="화"){
            days=1;
        }else if(days=="수"){
            days=2;
        }else if(days=='목'){
            days=3;
        }else if(days=='금'){
            days=4;
        }else if(days=='토'){
            days=5;
        }else{
            days=6
        }
       location.href='/result'+'?days='+days+'&check='+check+'&week='+week;

    });


    var week =$(".hidden_week").text();
//        alert(week);
    if(week=='preweek'){
        $(".prev_week").hide();
        $(".this_week").show();
        $(".nxt_week").show();
    }else if(week=="nextweek"){
//     alert(week);
        $(".prev_week").show();
        $(".this_week").show();
        $(".this_week").css("margin-right","0");
        $(".nxt_week").hide();
    }else{
//     alert(week);
        $(".prev_week").show();
        $(".this_week").hide();
        $(".nxt_week").show();
    }



});

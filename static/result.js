$(document).ready(function(){
    var bre_cal=parseFloat($(".bre_cal").text());
    var lun_cal=parseFloat($(".lun_cal").text());
    var din_cal=parseFloat($(".din_cal").text());

    $(".bre_cal").text("총 칼로리: "+bre_cal.toFixed(0));
    $(".lun_cal").text("총 칼로리: "+lun_cal.toFixed(0));
    $(".din_cal").text("총 칼로리: "+din_cal.toFixed(0));

    var carbo=parseFloat($(".carbo").text());
    var protein=parseFloat($(".protein").text());
    var fat=parseFloat($(".fat").text());

    $(".carbo").text("탄수화물: "+carbo.toFixed(0)+"g ");
    $(".protein").text("단백질: "+protein.toFixed(0)+"g ");
    $(".fat").text("지방: "+fat.toFixed(0)+"g ");

    var carbo_l=parseFloat($(".carbo_l").text());
    var protein_l=parseFloat($(".protein_l").text());
    var fat_l=parseFloat($(".fat_l").text());

    $(".carbo_l").text("탄수화물: "+carbo_l.toFixed(0)+"g ");
    $(".protein_l").text("단백질: "+protein_l.toFixed(0)+"g ");
    $(".fat_l").text("지방: "+fat_l.toFixed(0)+"g ");

    var carbo_d=parseFloat($(".carbo_d").text());
    var protein_d=parseFloat($(".protein_d").text());
    var fat_d=parseFloat($(".fat_d").text());

    $(".carbo_d").text("탄수화물: "+carbo_d.toFixed(0)+"g ");
    $(".protein_d").text("단백질: "+protein_d.toFixed(0)+"g ");
    $(".fat_d").text("지방: "+fat_d.toFixed(0)+"g ");



});
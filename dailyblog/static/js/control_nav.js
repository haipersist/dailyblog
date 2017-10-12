/**
 * Created by wanghb311 on 2016/6/28.
 */


$(function(){

    $("li.usercontrol ul").hide();
    $("li.usercontrol > a").click(function(){
        $(this).next().toggle();
        return false;
    });
})
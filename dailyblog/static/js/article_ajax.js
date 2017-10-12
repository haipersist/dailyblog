/**
 * Created by haibo on 17-3-17.
 */





$(function() {
    function index_form(e) {
        $.getJSON('/dashboard/certainarticle/',
            function(result) {
                var sidercatstr= "";
                var navcat="";
                var hotcat="";
                var latcat="";
                var mydairy="";
                var mydjango="";
                var myweb="";
                var jingstr="";
                var youstr="";
                var mingstr="";
                var category = result.categories;
                var hottest = result.hottest_articles;
                var latest = result.latest_articles;
                var dairies = result.mydairy;
                var djangos = result.mydjango;
                var webs = result.myweb;
                var jingdian = result.jingdian;
                var youxiu = result.youxiu;
                var mingren = result.mingren;
                for (i=0;i<category.length;i++) {
                    if (category[i].id != 0) {
                        sidercatstr += '<li class="list-group-item"><a href=' +
                        '"/category/' + category[i].alias + '">'+ category[i].name + '</a>' +
                        '<span class="badge badge-inverse" style="background-color: rgba(110, 121, 89, 0.8)">' + category[i].id + '</span></li>';
                        navcat += '<li><a href=' +
                                 '"/category/' + category[i].alias + '">'+ category[i].name + '</a>';
                    }
                }
                for (i=0;i<hottest.length;i++) {
                    hotcat += '<li class="list-group-item"><a href=' +
                        '"/article/' + hottest[i].alias + '.html">'+ hottest[i].title + '</a>' +
                        '<span class="hotspna">' + hottest[i].read_times + '</span></li>';
                }
                for (i=0;i<latest.length;i++) {
                    latcat += '<li class="list-group-item"><a href=' +
                        '"/article/' + latest[i].alias + '.html">'+ latest[i].title + '</a>';
                }
                for (i=0;i<dairies.length;i++) {
                    mydairy += '<li class="list-group-item"><a href=' +
                        '"/article/' + dairies[i].alias + '.html">'+ dairies[i].title + '</a>';
                }
                for (i=0;i<djangos.length;i++) {
                    mydjango += '<li class="list-group-item"><a href=' +
                        '"/article/' + djangos[i].alias + '.html">'+ djangos[i].title + '</a>';
                }
                for (i=0;i<webs.length;i++) {
                    myweb += '<li class="list-group-item"><a href=' +
                        '"/article/' + webs[i].alias + '.html">'+ webs[i].title + '</a>';
                }
                for (i=0;i<jingdian.length;i++) {
                    jingstr += '<li class="list-group-item"><a href=' +
                        '"/article/' + jingdian[i].alias + '.html">'+ jingdian[i].title + '</a>';
                }
                for (i=0;i<youxiu.length;i++) {
                    youstr += '<li class="list-group-item"><a href=' +
                        '"/article/' + youxiu[i].alias + '.html">'+ youxiu[i].title + '</a>';
                }
                 for (i=0;i<mingren.length;i++) {
                    mingstr += '<li class="list-group-item"><a href=' +
                        '"/article/' + mingren[i].alias + '.html">'+ mingren[i].title + '</a>';
                }
                $("#categories_info_list").html(sidercatstr);
                $("#dailycategory").html(navcat);
                $("#dailycategory2").html(navcat);
                $("#hottest-article-list").html(hotcat);
                $("#latest-article-list").html(latcat);
                $("#mydairy_info_list").html(mydairy);
                $("#mydjango_info_list").html(mydjango);
                $("#myweb_info_list").html(myweb);
                $("#jingdian_info_list").html(jingstr);
                $("#mingren_info_list").html(mingstr);
                $("#youxiu_info_list").html(youstr);
                //$("#latest-comment-list").html(mydjango);
            });
    }
    index_form();
// 绑定click事件
//$('#display').bind('click', submit_form);
});


$(function() {
    function initdata(e) {
       $('#datatable').DataTable({
            "language": {
                "sProcessing": "处理中...",
                "sLengthMenu": "显示 _MENU_ 项结果",
                "sZeroRecords": "没有匹配结果",
                "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
                "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
                "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
                "sInfoPostFix": "",
                "sSearch": "搜索:",
                "sUrl": "",
                "sEmptyTable": "表中数据为空",
                "sLoadingRecords": "载入中...",
                "sInfoThousands": ",",
                "oPaginate": {
                    "sFirst": "首页",
                    "sPrevious": "上页",
                    "sNext": "下页",
                    "sLast": "末页"
                },
                "oAria": {
                    "sSortAscending": ": 以升序排列此列",
                    "sSortDescending": ": 以降序排列此列"
                }
            },
            "ajax": {
                "url":'/dashboard/articlelist',
                "type":'GET',
                "data":function() {return {"name":$("#ttest").val()}}
            },
            "columns": [
                {"data": "title"},
                {"data": "author"},
                {"data": "pub_time"},
                {"data": "read_times"}
            ]
        });
    }
    function reinit(e){
        var table=$("#datatable").DataTable();
        // 重新载入table数据
        table.ajax.reload();
    }
    initdata();
    $("#tablebut").bind('click',reinit);
} );



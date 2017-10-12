/**
 * Created by haibo on 17-3-17.
 */







//for displaying job information
$(function() {
    function load_job_form(e) {
        $.getJSON('/job/display/',{"start":$("#graghstartday").val(),"end":$("#graghendday").val()},
        function(result) {
			$('#jobcontainer').highcharts({
                title: {
                    text: '工作统计',
                    x: -20 //center
                },
                subtitle: {
                    text: '统计日发布职位数',
                    x: -20
                },
                xAxis: {
                    categories: result.months
                },
                yAxis: {
                    title: {
                        text: '个'
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'
                    }]
                },
                tooltip: {
                    valueSuffix: '个'
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle',
                    borderWidth: 0
                },
                series: [{
                    name: '职位数',
                    data: result.count
                }
                ]
            });
        });

    }
	load_job_form();
    // 绑定click事件
    $('#job-graph-button').bind('click', load_job_form);
});

$(function() {
    function initjob(e) {
       $('#jobtable').DataTable({
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
            "aaSorting":[[5,'desc']],
            "ajax": {
                "url":'/job/list/',
                "type":'GET',
                "data":function() {return {"start":$("#startday").val(),"end":$("#endday").val()}}
            },
            "columns": [
                {"data": "title"},
                {"data": "company"},
                {"data": "salary"},
                {"data": "website"},
                {"data": "pub_time"},
                {"data": "link"}
            ]
        });
    }
    function reinitjob(e){
        var table=$("#jobtable").DataTable();
        // 重新载入table数据
        table.ajax.reload();
    }
    initjob();
    $("#job-table-button").bind('click',reinitjob);
} );
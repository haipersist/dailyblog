/**
 * Created by haibo on 17-3-17.
 */







//for displaying job information
$(function() {
    function load_comment_form(e) {
        $.getJSON('/api/comments/?format=json',
        function(result) {
            var comstr = "";
            var commentlist = result.results;
            var len = commentlist.length;
            var end = 0;
            if (len<5) {
                end = len;
            }
            else {
                end=len;
            }
            for(i=0;i<end;i++) {
                comstr += '<li class="list-group-item">' +
                    '<strong style="font-weight:bolder">'+commentlist[i].author.name +'</strong>'+ '在' +
                    '<a href=' + '"/article/' + commentlist[i].article.alias + '.html">'+
                    commentlist[i].article.title + '</a>发表了评论:'+
                '<span style="color:#b18012">'+commentlist[i].content+'</span>';
            }
			$('#latest-comment-list').html(comstr);
        });
    }

	load_comment_form();
    // 绑定click事件
    //$('#job-graph-button').bind('click', load_job_form);
});


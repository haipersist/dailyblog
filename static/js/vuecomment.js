/**
 * Created by haibo on 17-6-15.
 */



Vue.config.delimiters = ['${', '}}'];
Vue.http.options.emulateJSON = true;
var vm = new Vue({
  el: '#vcomments',
  //delimiters: ['${', '}}'],
  data: {
    comment: {
        content:'',
        commentid:0,
        toid:0,
        username:'',
        useremail:'',
        reply:0,
        csrftoken:''
    },
    title: '留下评论',
    no_comments: true,
   // comments: ''
    articleid:0
    //csrftoken:''


  },
  http:{
      headers:{'X-CSRFToken':this.comment.csrftoken}
  },

  methods:{
    createcomment: function () {
        if(this.comment.content==''){
            $.scojs_message('请输入评论内容', $.scojs_message.TYPE_ERROR);
            return 1;
        } else {
        this.$http.post('/comment/article/'+this.articleid+'/create/',this.comment,
            {'headers':{'X-CSRFToken':this.comment.csrftoken}}
        ).then(function(response) {
                if(response.data.msg=='success') {
                    $.scojs_message('评论提交成功！', $.scojs_message.TYPE_OK);
                    this.getcommentlist();
                    this.clearcomment();
                } else if(response.data.msg=='emailempty') {
                    $.scojs_message('邮箱是必填项，方便作者与您深入交流啊！', $.scojs_message.TYPE_ERROR);
                } else if(response.data.msg=='emailformat') {
                    $.scojs_message('邮箱格式错误，请正确填写邮箱！', $.scojs_message.TYPE_ERROR);
                } else if(response.data.msg=='tokenexpire') {
                    $.scojs_message('token过期了，您注册一下用户吧，让我们更好交流！', $.scojs_message.TYPE_ERROR);
                } else {
                    $.scojs_message('提交失败，请稍后再试，或者给作者发邮件留言', $.scojs_message.TYPE_ERROR);
                    this.clearcomment();
                }
            });
        }
    },
    testcreate: function () {
        this.clearcomment();
        $.scojs_message('请输入评论内容', $.scojs_message.TYPE_ERROR);
    },
    replycomment: function (commentid,toid,name) {
        this.comment.commentid = commentid;
        this.comment.toid = toid;
        this.comment.reply = 1;
        this.title = '@'+name+':';
    },
    clearcomment: function() {
        this.comment.content='';
        this.comment.commentid=0;
        this.comment.toid=0;
        this.comment.reply=0;
        this.title = '留下评论';

    },
    getcommentlist: function () {
        this.$http.get('/comment/article/'+this.articleid+'/list/', function (data) {
                    this.$set('comments', data.comments);
                    if(data.comments.length != 0){
                        this.no_comments = false;
                    }
            });
    }
  },
  ready: function () {
      this.getcommentlist();
  }
});


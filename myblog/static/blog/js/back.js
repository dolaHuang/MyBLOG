$(function () {
    // 显示分页器
    var page_num=$('ul.pagination').children().length;
    if(page_num>3){
        $('.home_site_paginator').show()
    }
    // {#删除获取数据#}
    $('.delete-button').click(function () {
            // {#当前按钮标签的href#}
            var id = $(this).attr('id');
            var tag = $('#myModal');
            $(this).parent().parent().append(tag);
            // {#获取该行数据的name字段的值#}
            article_name = $(this).parent().siblings().first().text();
            console.log(article_name);
            // {#模态框的删除按钮#}
            btn = $(this).parent().siblings('div').find('a');
            // {#设置btn的href#}
            btn.attr("href", '/article/' + id + '/delete');
            $('div.modal-body').text('确定要删除 <' + article_name + '> 吗？删除后将无法恢复！！！');
        });
    // 添加新标签和分类
    $('span.add').click(function () {
        var title=$(this).prev().val().trim();
        if(title){
            $.ajax({
                url:'/add_new_condition/',
                type:'post',
                data:{
                    'title':title,
                    'conditon':$(this).attr('add'),
                    csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()
                },
                success:function (response) {
                    condition=response.conditon;
                    console.log(condition);
                    $('.add_'+condition).val('');
                    tag=`<option value="${title}">${title}</option>`;
                    if(response.state){
                        $('#'+condition).append(tag);
                        $('.selectpicker').selectpicker('refresh');
                        $('.add_error').html('已成功添加');
                        setTimeout(function () {
                            $('.add_error').html('')
                        },1000)

                    }else{
                        $('.add_error').html(response.msg);
                        setTimeout(function () {
                            $('.add_error').html('')
                        },1000)
                    }
                    // 添加到选择器中

                }
            })
        }
        else if(title===''){
            $('.add_error').html('字段不能为空！');
            setTimeout(function () {
                 $('.add_error').html('')
            },1000)
        }
    });
    // 添加新文章
    $('.publish_article').click(function () {
        var title=$('#article-title').val();
        html = editor.html();
        editor.sync();
        var content=editor.html();
        var web_site_category=$('#web_site_category').val();
        var category=$('#category').val();
        var tag=$('#tag').val();
        $.ajax({
            url:'',
            type:'post',
            data:{
                'title':title,
                'content':content,
                'web_site_category':web_site_category,
                'category':category,
                'tag':tag,
                 csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()
            },
            traditional:true,
            success:function (response) {
                if(response.state){
                    window.location.href='/back_stage/'
                }else {
                    if(content===''|| title===''){
                        $('.add_error').html('发布失败！内容或者标题不能为空');
                    }else if(title.length>32){
                        $('.add_error').html('发布失败！标题不得大于32个字符  ');
                    }
                    $.each(response.msg,function (name,error_info) {
                        $('.error_'+name).html(error_info);
                    });
                    setTimeout(function () {
                        $('.error_content').html('');
                        $('.error_title').html('');
                        $('.add_error').html('');
                    },2000)
                }
            }
        })
    })
});



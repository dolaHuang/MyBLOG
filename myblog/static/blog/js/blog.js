$(function () {
    // {#刷新验证码#}
    $('#valid_code_img').click(function () {
    $(this)[0].src+='?'
});
    // {#登陆验证#}
    $('#login-btn').click(function () {
    $.ajax({
        url:'',
        type:'post',
        data:{
            user:$('#login-username-input').val(),
            pwd:$('#login-pwd-input').val(),
            valid_code:$('#login-valid-input').val(),
            csrfmiddlewaretoken:$('[name=csrfmiddlewaretoken]').val()
        },
        success:function (data) {
            $('#login-username').text('');
            $('#login-password').text('');
            $('#login-valid').text('');
            if(data.user){
                location.href='/index/'
            }else {
                $.each(data.msg,function (name,error_info) {
                    $('#login-'+name).text(error_info)

                });
                setTimeout(function () {
                    $('#login-username').text('');
                    $('#login-password').text('');
                    $('#login-valid').text('');

                },1000)
            }
        }

    })
});
    // 头像预览
    $('#avator').change(function () {
        console.log(123);
        // 获取用户选中的文件对象
        var file_obj=$(this)[0].files[0];
        // 获取选中图片路径
        var reader=new FileReader();
        reader.readAsDataURL(file_obj);
        // 修改img的src的属性,覆盖原图片
        reader.onload=function () {
            $('#avator_img').attr('src',reader.result)
        };
    });
         // 基于Ajax提交注册数据
    $('#reg-button').click(function () {
        var form_data=new FormData();
        var requset_data=$('#form').serializeArray();
        $.each(requset_data,function (index,data) {
            form_data.append(data.name,data.value)
        });
        // 当数据多的时候，用上面的方法
        // form_data.append('username',$('#id_username').val());
        // form_data.append('password',$('#id_password').val());
        // form_data.append('password_r',$('#id_password_r').val());
        // form_data.append('email',$('#id_email').val());
        // form_data.append('csrfmiddlewaretoken',$("[name='csrfmiddlewaretoken']").val());
        form_data.append('avator',$('#avator')[0].files[0]);

        $.ajax({
            url:'',
            type:'post',
            // 编码类型两个参数
            contentType:false,
            processData:false,
            data:form_data,
            success:function (data) {
                // 清空错误状态
                $('span.reg-error').text('');
                $('.form-group').removeClass('has-error');
                // 判断验证是否通过
                if(data.user){
                    setTimeout(function () {
                        $('.success_reg_info').css('display','block');
                    },1000);
                    // 直接跳转到登陆页面
                    location.href='/login/';
                    setTimeout(function () {
                        $('.success_reg_info').hide();
                    },1000)
                }else {
                    console.log(data.msg);
                    $.each(data.msg,function (name,error_info) {
                        // 全局错误信息的展示
                        if(name==='__all__'){
                            $('#id_password_r').next().text(error_info[0]).parent().addClass('has-error')
                        }

                        $('#id_'+name).next().text(error_info[0]);
                        $('#id_'+name).parent().addClass('has-error');

                        setTimeout(function () {
                            $('span.reg-error').text('');
                            $('.form-group').removeClass('has-error');
                        },2000)
                    })
                }
            }
        })
    })




});
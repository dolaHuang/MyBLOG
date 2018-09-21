$(function () {
    $('.set_pwd').click(function () {
        var old_password=$('#old_password').val();
        var new_password=$('#new_password').val();
        var repeat_password=$('#repeat_password').val();
        $.ajax({
            url:'',
            type:'post',
            data:{
                'old_password':old_password,
                'new_password':new_password,
                'new_password_r':repeat_password,
                'csrfmiddlewaretoken':$('[name="csrfmiddlewaretoken"]').val(),
            },
            success:function (response) {
                console.log(response);
                if(response.state){
                    $('.success_set').show();
                    setTimeout(function () {
                        window.location.href='/login/'
                    },1000);

                }else{
                    $.each(response.msg,function (name,error_info) {
                        $('#re_'+name).text(error_info);
                        if(name==="__all__"){
                            $('#re_new_password').text(error_info)
                        }
                    });
                    setTimeout(function () {
                        $('#re_new_password').text('');
                        $('#re_old_password').text('');
                        $('#re_new_password_r').text('');

                    },3000)
                }

            }
        })
    })
});
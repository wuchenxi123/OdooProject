/**
 * Created by pengyb on 16/4/2.
 */



$(function () {
    $('#soup_id').on('change', function() {
        var soup_id = $(this).attr("value")
        var url = "/get_soup/"+$("#soup_id").val()
        $.get(url,function(data,status){
            if (status == 'success'){
                var soup = JSON.parse(data);
                if (soup != 0){
                    $('#price').val(soup.price)
                    $('#tax').val(soup.price*0.17)
                    $('#payment').val(soup.price)
                    $('#calc_price').text('应付:'+soup.price+'元(其中包括税:'+$('#tax').val()+'元)')
                }else{
                    alter('亲,老板娘还未准备好咧!\n等会再来吧!');
                }
            }
        });
    });

});

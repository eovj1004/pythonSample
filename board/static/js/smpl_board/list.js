$(function(){
	$('#btn_regist').click(function(){
		location.href = '/smplBoard/registForm';
	});
});


function checkPassword(board_id){
	var input_pw = prompt('パスワードを入力してください。');
	if(input_pw == ''){
		return;
	}
	$.ajax({
        url:'/smplBoard/checkPassword',
        type:'POST',
        dataType : 'json',
        data : { 'board_id': board_id, 
        		 'input_pw': input_pw, 
        		 'csrfmiddlewaretoken': csrftoken 
        },
        success:function(data){
            if(data.result == -1){
            	alert("パスワードが一致してません。");
            }
            else if(data.result == 1000){
            	location.href = '/smplBoard/view?board_id=' + board_id + '&password=' + input_pw;
            }
        },
        error:function(request,status,error){
			alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
			}
    });
}
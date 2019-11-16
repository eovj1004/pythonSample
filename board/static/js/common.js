var csrftoken = getCookie('csrftoken');

$(function(){

	$('#login_id').keydown(function(){
		if (event.keyCode === 13) {
			clickLogin();
		}
	});
	$('#login_pw').keydown(function(){
		if (event.keyCode === 13) {
			clickLogin();
		}
	});

	// Login ボタンクリックイベント
	$('#btn_com_login').click(function(){
		var id = $('#login_id').val();
		var pw = $('#login_pw').val();
		
		if(id == '' || id.length < 5){
			alert('idを入力してください。');
			return;
		}
		if(pw == ''){
			alert('passwordを入力してください。');
			return;
		}

		$.ajax({
            url:'/user/loginProcess',
            type:'POST',
            dataType : 'json',
            data : { 'id': id, 'pw': pw, 'csrfmiddlewaretoken': csrftoken },
            success:function(data){
                if(data.result == -1){
                	alert("ID及びパスワードを確認してください。");
                }
                else if(data.result == 1000){
                	location.reload();
                }
            },
            error:function(request,status,error){
				alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
   			}
        });
	});

	//Join ボタンクリックイベント
	$('#btn_com_join').click(function(){
		$('#loginForm').hide();
		$('#joinForm').show();
		layer_popup('#layer2');
	});

	//Regist 画面でcancelボタンクリックイベント 
	$('#btn_com_cancel').click(function(){
		$('#loginForm').show();
		$('#joinForm').hide();
		layer_popup('#layer2');
	});

	//Regist ボタンクリックイベント
	$('#btn_com_regist').click(function(){
		var id = $('#id').val();
		var pw = $('#pw').val();
		var pw2 = $('#pw2').val();
		var picture = $('#picture').val();

		if(id == ''){
			alert('idを入力してください。');
			$('#id').focus();
			return;
		}
		if(pw == '' || pw < 4){
			alert('4文字以上のPasswordを入力してください。');
			$('#pw').focus();
			return;	
		}
		if(pw2 == ''){
			alert('Verify Passwordを入力してください。');
			$('#pw2').focus();
			return;	
		}
		if(pw != pw2){
			alert('PasswordとVerify Passwordが一致してません。ご確認してください。');
			$('#pw').focus();
			return;
		}
		if(picture == ''){
			alert('Pictureを登録してください。');
			$('#Picture').focus();
			return;
		}

		var frm = document.getElementById('registForm');
	 	var fileData = new FormData(frm);

		$.ajax({
            url:'/user/regist',
            type:'POST',
	        data:fileData,
	        async:false,
	        cache:false,
	        contentType:false,
	        processData:false,
            success:function(data){
                if(data.result == -1){
                	alert("エラー発生");
                }
                else if(data.result == -1000){
                	alert("登録されてるID");
                }
                else if(data.result == 1000){
                	alert("登録完了");
                	location.reload();
                }
            },
            error:function(request,status,error){
				alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
   			}
        });
	});

	// index pageメール発送イベント
	$('#btn_mail_send').click(function(){
		var email = $('#email').val();
		if(!checkEmail(email)){
			alert("入力したメールアドレスを確認してください。");
			return false;
		}
		
		$.ajax({
			url:'/sendMail',
            type:'POST',
            dataType : 'json',
            data : { 'email': email, 'csrfmiddlewaretoken': csrftoken },
            success:function(data){
                if(data.result == -1){
                	alert("メール発送失敗");
                }
                else if(data.result == 1000){
                	alert("メール発送が完了されました。");
                }
            },
            error:function(request,status,error){
				alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
   			}
        });
	});

	$("#email").keydown(function(e){
		
		//enter ボタン押した場合
		if(e.keyCode == 13){
			e.preventDefault();
			$('#btn_mail_send').click();
		}

	});
});

//メールを有効性を確認する
function checkEmail(email){
	var regExp = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;

	if(regExp.test(email)){
		//正しいメール
		return true;
	}
	else{
		return false;
	}
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue =   decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function clickLogin(){
	$('#btn_com_login').trigger('click');
}
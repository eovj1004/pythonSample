$(function(){
	$('#edit').froalaEditor({
        //言語設定
        language: 'ko',

        //height
        height: 300,

        // イメージをアップロードするときのparameter name
        imageUploadParam: 'file',

        // イメージアップロードURL Path
        imageUploadURL: '/image/upload',

        // Request method
        imageUploadMethod: 'POST',

        // イメージサイズ : 5MB
        imageMaxSize: 5 * 1024 * 1024,

        // アップロードできる画像のタイプ
        imageAllowedTypes: ['jpeg', 'jpg', 'png']
    })
    //editorからイメージか削除された場合サーバーに保存されてるイメージも削除
	.on('froalaEditor.image.removed', function (e, editor, $img) {
        $.ajax({
          	// Request method
          	method: "POST",

          	// イメージ削除URL Path
          	url: "/image/delete",

          	// Request params
          	data: {
            src: $img.attr('src')
      		}
	    })
	    .done (function (data) {
	        console.log ('イメージ削除完了');
	    })
	    .fail (function () {
	    	console.log ('イメージ削除失敗');
	    })
    })
    .on('froalaEditor.image.error', function (e, editor, error, response) {
      	alert('イメージアップロードに失敗しました。');
        console.log ('イメージ削除失敗');
    });



	$('#btn_regist').click(function(){
        if(checkForm()){
            var smpl_form = $('#smpl_form');
            smpl_form.attr('method', 'POST');
            smpl_form.attr('action', '/smplBoard/insert');
            smpl_form.submit();
        }

	});

    $('#btn_cancel').click(function(){
        location.href = '/smplBoard/list';
    });

    $('input[name=is_secret]').change(function(){
        if(this.value == 0){
            $('#pw_area').hide();
        }
        else if(this.value == 1){
            $('#pw_area').show();
        }
    });

    $('#btn_modify').click(function(){
        if(checkForm()){
            var smpl_form = $('#smpl_form');
            smpl_form.attr('method', 'POST');
            smpl_form.attr('action', '/smplBoard/update');
            smpl_form.submit();
        }
    });
});

function checkForm(){
    var title = $('#title').val();
    var is_secret = $(":input:radio[name=is_secret]:checked").val();
    var password = $('#password').val();
    var content = $('#edit').froalaEditor('html.get');

    if(title == '' || title.length > 100){
        alert('1～100文字のタイトルを入力してください。');
        $('#title').focus();
        return false;
    }

    if(is_secret == 1){
        if(password == '' || password.length < 4){
            alert('4文字以上のパスワードを入力してください。');
            $('#password').focus();
            return false;
        }
    }

    if(content == ''){
        alert('内容を入力してください。');
        return false;
    }
    else{
        $('#content').val(content);
    }

    return true;
}
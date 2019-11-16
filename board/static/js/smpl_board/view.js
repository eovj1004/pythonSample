$(function() {
    $('#btn_move_list').click(function() {
        location.href = '/smplBoard/list';
    });

    $('#btn_modify').click(function() {
        location.href = '/smplBoard/registForm?board_id=' + $('#board_id').val();
    });
});

var active_row = -1;

function setReply(parent_id, row_index, req_type) {
    $('#parent_id').val(parent_id);
    if (active_row >= 0) {
        $(".comment_area li:eq(" + active_row + ")").remove();
        $('#close' + (active_row - 1)).hide();
        $('#reply' + (active_row - 1)).show();
        $('#modify' + (active_row - 1)).show();
    }
    var text_area = '';
    var html_btn = '';
    if (req_type == 'c') {
        text_area = '<textarea class="comment" id="reply" name="reply"></textarea>';
        html_btn = '<span onclick="addComment($(\'#reply\').val())" class="btn_cmt_regist pointer">' +
            '    <label class="pointer">登録</label>' +
            '</span>';
    }
    if (req_type == 'u') {
        comment = $('#comment' + row_index).html().trim();
        text_area = '<textarea class="comment" id="reply" name="reply">' + comment + '</textarea>';
        html_btn = '<span onclick="modifyComment(' + parent_id + ')" class="btn_cmt_regist pointer">' +
            '    <label class="pointer">修正</label>' +
            '</span>';
    }

    var html = '<li class="parent">' +
        '    <table class="w_full">' +
        '        <colgroup>' +
        '            <col style="width: 90%;">' +
        '            <col style="width: *;">' +
        '        </colgroup>' +
        '        <tbody>' +
        '            <tr>' +
        '                <td>' +
        text_area +
        '                </td>' +
        '                <td>' +
        html_btn +
        '                </td>' +
        '            </tr>' +
        '        </tbody>' +
        '    </table>' +
        '</li>';

    $(".comment_area li:eq(" + row_index + ")").after($(html));

    $('#close' + row_index).show();
    $('#reply' + row_index).hide();
    $('#modify' + row_index).hide();

    active_row = row_index + 1;
}

function addComment(content) {
    var comment = content;
    var board_id = $('#board_id').val();
    var parent_id = $('#parent_id').val();

    if (comment == '') {
        alert('コメントを入力してください。');
        return;
    }

    $.ajax({
        url: '/smplBoard/insertComment',
        type: 'POST',
        dataType: 'json',
        data: {
            'comment': comment,
            'board_id': board_id,
            'parent_id': parent_id,
            'csrfmiddlewaretoken': csrftoken
        },
        success: function(data) {
            if (data.result == -1) {
                alert("コメント登録失敗");
            } else if (data.result == 1000) {
                location.reload();
            }
        },
        error: function(request, status, error) {
            alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        }
    });
}

function cancelReply(row_index) {
    $(".comment_area li:eq(" + active_row + ")").remove();
    active_row = -1;

    $('#close' + row_index).hide();
    $('#reply' + row_index).show();
    $('#modify' + row_index).show();
}

function removeReply(comment_id) {
    if (confirm('確認ボタンを押すとコメントが削除されます。\n本当に削除しますか？')) {
        $.ajax({
            url: '/smplBoard/removeComment',
            type: 'POST',
            dataType: 'json',
            data: {
                'comment_id': comment_id,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(data) {
                if (data.result == -1) {
                    alert("コメント削除失敗");
                } else if (data.result == 1000) {
                    location.reload();
                }
            },
            error: function(request, status, error) {
                alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            }
        });
    }
}

function modifyComment(comment_id) {
	var reply = $('#reply').val();

	if(reply == ''){
        alert('コメントを入力してください。');
		return;
	}

    $.ajax({
        url: '/smplBoard/modifyComment',
        type: 'POST',
        dataType: 'json',
        data: {
            'comment_id': comment_id,
            'comment': reply,
            'csrfmiddlewaretoken': csrftoken
        },
        success: function(data) {
            if (data.result == -1) {
                alert("コメント修正失敗");
            } else if (data.result == 1000) {
                location.reload();
            }
        },
        error: function(request, status, error) {
            alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        }
    });
}
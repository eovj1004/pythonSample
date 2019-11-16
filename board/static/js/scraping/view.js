var href = '';
$(function() {
	$('h1').css('color','black')
	href = $(".tpcNews_detailLink>a").attr('href');
	$(".tpcNews_detailLink>a").attr('href', '#');

	$('.paragraph').css('border-bottom', '1px solid black');
	$('.paragraph').css('margin', '50px 0px');

	$(".tpcNews_detailLink>a").click(function(){
		location.href = '/scraping/detail?url=' + escape(href);
	});

	$("#btn_move_list").click(function(){
		location.href = '/scraping/yahoo';
	});
});
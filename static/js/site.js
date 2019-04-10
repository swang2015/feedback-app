$('#radioBtn label').on('click', function(){
	labelID = $(this).attr('for');
	$('#'+labelID).attr('checked', true);
	$("#answerform").submit();
})

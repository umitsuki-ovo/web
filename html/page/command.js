// accordion
$('.title').on('click', function() {
	$('.box').slideUp(500);
    
	var findElm = $(this).next(".box");
    
	if($(this).hasClass('close')){
		$(this).removeClass('close');   
	}
	else{
		$('.close').removeClass('close'); 
		$(this).addClass('close');
		$(findElm).slideDown(500);
	}
});

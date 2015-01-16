function showSimple()
{
    $('#advanced-search').hide();
    $('#simple-search').show();
	return false;
}

function showAdvanced()
{
    $('#simple-search').hide();
    $('#advanced-search').show();
	return false;
}


$(function(){
	$('h3.clickable').click(
		function(){
			$('#advanced-search #'+$(this).attr('name')).focus();
		}
	);
})

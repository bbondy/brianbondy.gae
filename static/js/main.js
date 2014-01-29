$(document.body).load(function () {
    $(".comments").slideUp();
});

function styleCode()
{
	$("pre code").parent().each(
		function()
		{
			if(!$(this).hasClass("prettyprint"))
			{
				$(this).addClass("prettyprint");
				prettyPrint();
			}
		}
	);
}

function toggleAddComment(newsID)
{
	$("#AddComment-" + newsID).slideToggle();
	$("#Comments-" + newsID).slideUp();
}

function toggleComments(newsID)
{
	$("#Comments-" + newsID).slideToggle();
	$("#AddComment-" + newsID).slideUp();
}

function toggleTags()
{
	$("#sidebar3").slideToggle();
        if($("#tag-label").text().indexOf(">>") != -1)
		$("#tag-label").text($("#tag-label").text().replace(">>", "<<"));
	else
		$("#tag-label").text($("#tag-label").text().replace("<<", ">>"));
}

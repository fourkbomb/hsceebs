$(document).ready(function() {
    $('.subj-sel-check').prop('checked', 0);
    $('.subj-sel-check').change(function(sender) {
		$('.subject-select').removeClass('selected');
        $(sender.target.parentElement).addClass('selected');
    });
	$('#launch-countdown').click(function(sender) {
		var sel = $('input[name=bob]:checked', '#setup-modal-inner');
		if (sel.length == 0) {
			$('#pls-select-exam').addClass('plsguys');
			return false;
		} else {
			console.log(sel.val());
			window.location = window.location.toString() + sel.val();
		}
	});
});

$(document).ready(function() {
    $('.subj-sel-check').prop('checked', 0);
    $('.subj-sel-check').change(function(sender) {
        $(sender.target.parentElement, 'label').toggleClass('selected');
        console.log($(sender.target.parentElement, 'label'));
    });
});

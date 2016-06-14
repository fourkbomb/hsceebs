$(document).ready(function() {
	console.log(subjdata);
	// looks like the parser screwed up (some) dates.
	var d = new Date(subjdata['times'][1]);
	if (d.getHours() > 17 || (d.getHours() == 17 && d.getMinutes() > 0) || d.getHours() < 11) {
		// some dates are 12 hours off for some reason.
		// all HSC exams finish between 11AM and 5PM, so we can work around this
		subjdata['times'][1] -= 12 * 3600 * 1000;
	}
	$('#countdown-label').html(new Date(subjdata['times'][1]));
	updateCountdown();
	setInterval(updateCountdown, 1000);
});

function pad(number, size) {
	var n = ''+number;
	if (n.length < size) {
		n = '0' * (size - n.length) + n;
	}
	return n;
}

function fmtSeconds(sec) {
	var ms, secs, min, hrs, days, res, showMS = false;
	ms = sec % 1000;
	sec = Math.floor(sec / 1000);
	secs = sec % 60;
	sec = Math.floor(sec/60);
	min = sec % 60;
	sec = Math.floor(sec/60);
	hrs = sec % 24;
	sec = Math.floor(sec/24);
	days = sec;

	res = "";
	secs = pad(secs, 2);
	min = pad(min, 2);
	if (hrs > 0 || days > 0) {
		hrs = pad(hrs, 2);
		if (days > 0) {
			res = days + "d ";
		} else {
			showMS = true;
		}
		res += hrs + "h ";
	}
	res += min + "m " + secs + "s";
	if (showMS) res += " " + ms + "ms";
	return res;

}

function updateCountdown() {
	var gap, str;
	gap = subjdata['times'][1] - Date.now();
	str = fmtSeconds(gap);
	$('#countdown-label').html(str);
}


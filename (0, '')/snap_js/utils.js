$(document).ready(function() {
	// contact us button
	$("input.contact-button").button();
	// create crontab button
	$("a.create-crontab").button();
	$('a.tooltip-500').aToolTip({
		fixed: true,
		xOffset: -280, // centered
		yOffset: 5,
		toolTipClass: 'aToolTip-500',
	}); 
});

// track ajax links with Google Analytics
function gaTrack(url) {
	if (typeof pageTracker=='object') {
		pageTracker._trackPageview(url);
	}
}

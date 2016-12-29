(function( $ ){

	// Append the actual Tooltip elements to the BODY
	$('body').prepend('<div class="lpTooltipWrap"><div class="lpTooltipText"><span></span></div></div>');

	var text = '';
	var cWidth = 0;
	var cHeight = 0;
	var tWidth = 0;
	var tHeight = 0;
	var offsetWidth = 0;
	var pos = 0;
	var posTop = 0;
	var posLeft = 0;

	$(document).on('mouseenter', '.lpTooltip', function () {

		var $that = $(this);

		text = $(this).attr('data-tooltip-text');
		pos = $(this).offset();
		posTop = pos.top;
		posLeft = pos.left;
		cWidth = $(this).outerWidth();
		cHeight = $(this).outerHeight();

		if(text !== ''){
			
			$('.lpTooltipText span').text(text);

			$('.lpTooltipWrap').css({
				'top': posTop,
				'left': posLeft,
				'width': cWidth
			}).show();

			tWidth = $('.lpTooltipText').outerWidth();
			tHeight = $('.lpTooltipText').outerHeight() + 10;
			offsetWidth = tWidth - cWidth;
			offsetWidth = offsetWidth / 2;

			if(tWidth > cWidth){
				$('.lpTooltipText').css('marginLeft', - offsetWidth);
			}

			$('.lpTooltipWrap').removeClass('lpBottom').removeClass('lpLeft').removeClass('lpRight').css('marginTop', - tHeight);

			if($(this).hasClass('lpBottom')){
				$('.lpTooltipWrap').addClass('lpBottom').css('marginTop', cHeight + 10);
			}

			if($(this).hasClass('lpLeft')){
				var diffHeight = tHeight - 10;
				diffHeight = diffHeight / 2;

				$('.lpTooltipWrap').addClass('lpLeft').css({
					'marginTop': cHeight / 2 - diffHeight,
					'left': posLeft - cWidth
				});

				console.log(cWidth);
			}

			if($(this).hasClass('lpRight')){
				var diffHeight = tHeight - 10;
				diffHeight = diffHeight / 2;

				$('.lpTooltipWrap').addClass('lpRight').css({
					'marginTop': cHeight / 2 - diffHeight,
					'left': posLeft + cWidth
				});

				console.log(diffHeight);
			}

		}

	});

	$(document).on('mouseleave', '.lpTooltip', function() {
		$('.lpTooltipText span').text('');
		$('.lpTooltipText').css('marginLeft', '0');
		$('.lpTooltipWrap').hide();
	});

	$(document).on('click', function() {
		$('.lpTooltipText span').text('');
		$('.lpTooltipText').css('marginLeft', '0');
		$('.lpTooltipWrap').hide();
	});

})( jQuery );

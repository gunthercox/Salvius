(function($) {
 	$.fn.spinner = function(settings) {
 		
 		settings = $.extend({
 			sqr: undefined,
 			framerate : 10,
 			spokeCount : 16,
 			rotation : 0,
 			spokeOffset : {
 				inner : undefined,
 				outer : undefined
 			},
 			spokeWidth : undefined,
 			colour : '000,000,000',
 			backup : 'images/spinner.gif',
 			centered : true
 		}, settings || {});
 
 		return this.each(function () {
 
 			var $this = $(this),
 				width = $this.width(),
 				height = $this.height(),
 				ctx,
 				hsqr,
 				$wrap,
 				$canv;
 						
 			settings.sqr = Math.round(width >= height ? height : width);
 			hsqr = settings.sqr/2;
 			// convert from deg to rad
 			settings.rotation = settings.rotation/180 * Math.PI
			settings.spokeOffset.inner = settings.spokeOffset.inner || hsqr * 0.3;
			settings.spokeOffset.outer = settings.spokeOffset.outer || hsqr * 0.6;	
 			
 			$wrap = $('<div id="spinner-' + $.fn.spinner.count + '" class="spinner" />')
 			if (settings.centered) {
 				$wrap.css({'position' : 'absolute', 'z-index' : 999, 'left' : '50%', 'top' : '50%', 'margin' : hsqr * -1 + 'px 0 0 ' + hsqr * -1 + 'px', 'width' : settings.sqr, 'height' : settings.sqr })
 			}
 		    $canv = $('<canvas />').attr({ 'width' : settings.sqr, 'height' : settings.sqr });
 			
 			if ( $this.css('position') === 'static' && settings.centered ) {
 				$this.css({ 'position' : 'relative' });
 			}
 			
 			$canv.appendTo($wrap);
 			$wrap.appendTo($this);
 			 		
			if ( $canv[0].getContext ){  
				ctx = $canv[0].getContext('2d');
				ctx.translate(hsqr, hsqr);
				ctx.lineWidth = settings.spokeWidth || Math.ceil(settings.sqr * 0.025);
				ctx.lineCap = 'round'
				this.loop = setInterval(drawSpinner, 1000/ settings.framerate);
			} else {
				// show a backup image...
				$canv.remove();
				$wrap.css({ 'background-image' : 'url(' + settings.backup + ')', 'background-position' : 'center center', 'background-repeat' : 'none'})
			}

			function drawSpinner () {
				ctx.clearRect(hsqr * -1, hsqr * -1, settings.sqr, settings.sqr);
				ctx.rotate(Math.PI * 2 / settings.spokeCount + settings.rotation );
				for (var i = 0; i < settings.spokeCount; i++) {
					ctx.rotate(Math.PI * 2 / settings.spokeCount);
					ctx.strokeStyle = 'rgba(' + settings.colour + ','+ i / settings.spokeCount +')';
					ctx.beginPath();
					ctx.moveTo(0, settings.spokeOffset.inner);
					ctx.lineTo(0, settings.spokeOffset.outer);
					ctx.stroke();
				}
			}  
 			$.fn.spinner.count++;
 		});
 	};
 	$.fn.spinner.count = 0;
 	$.fn.spinner.loop;
 
 	$.fn.clearSpinner = function() {
 		return this.each(function () {
	 		clearTimeout($.fn.spinner.loop);
	 		$(this).find('div.spinner').fadeOut().remove().end();
 		});
 	}
})(window.jQuery);

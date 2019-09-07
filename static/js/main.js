'use strict';


$(window).on('load', function () {
	/*------------------
		Preloder
	--------------------*/
	$(".loader").fadeOut();
	$("#preloder").delay(400).fadeOut("slow");


	/*------------------
		Product filter
	--------------------*/
	if ($('#product-filter').length > 0) {
		var containerEl = document.querySelector('#product-filter');
		var mixer = mixitup(containerEl);
	}

});

(function ($) {
	/*------------------
		Navigation
	--------------------*/
	$('.nav-switch').on('click', function (event) {
		$('.main-menu').slideToggle(400);
		event.preventDefault();
	});


	/*------------------
		Background Set
	--------------------*/
	$('.set-bg').each(function () {
		var bg = $(this).data('setbg');
		$(this).css('background-image', 'url(' + bg + ')');
	});


	/*------------------
		Hero Slider
	--------------------*/
	$('.hero-slider').owlCarousel({
		loop: true,
		nav: true,
		navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
		dots: true,
		mouseDrag: false,
		animateOut: 'fadeOut',
		animateIn: 'fadeIn',
		items: 1,
		autoplay: true
	});


	/*------------------
		Intro Slider
	--------------------*/
	if ($('.intro-slider').length > 0) {
		var $scrollbar = $('.scrollbar');
		var $frame = $('.intro-slider');
		var sly = new Sly($frame, {
			horizontal: 1,
			itemNav: 'forceCentered',
			activateMiddle: 1,
			smart: 1,
			activateOn: 'click',
			//mouseDragging: 1,
			touchDragging: 1,
			releaseSwing: 1,
			startAt: 10,
			scrollBar: $scrollbar,
			//scrollBy: 1,
			activatePageOn: 'click',
			speed: 200,
			moveBy: 600,
			elasticBounds: 1,
			dragHandle: 1,
			dynamicHandle: 1,
			clickBar: 1,
		}).init();
	}



	/*------------------
		ScrollBar
	--------------------*/
	$(".cart-table, .product-thumbs").niceScroll({
		cursorborder: "",
		cursorcolor: "#afafaf",
		boxzoom: false
	});



	/*------------------
		Single Product
	--------------------*/
	$('.product-thumbs-track > .pt').on('click', function () {
		var imgurl = $(this).data('imgbigurl');
		var bigImg = $('.product-big-img').attr('src');
		if (imgurl != bigImg) {
			$('.product-big-img').attr({
				src: imgurl
			});
		}
	})

})(jQuery);
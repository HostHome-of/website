isTouchDevice = ->
  prefixes = ' -webkit- -moz- -o- -ms- '.split(' ')

  mq = (query) ->
    window.matchMedia(query).matches

  if 'ontouchstart' of window or window.DocumentTouch and document instanceof DocumentTouch
    return true
  query = [
    '('
    prefixes.join('touch-enabled),(')
    'heartz'
    ')'
  ].join('')
  mq query

do ->
  svg4everybody()
  return
if isTouchDevice()
  $('body').addClass 'touch-device'
do ->
  header = $('.js-header')
  burger = header.find('.js-header-burger')
  wrapper = header.find('.js-header-wrapper')
  html = $('html')
  body = $('body')
  burger.on 'click', ->
    burger.toggleClass 'active'
    wrapper.toggleClass 'visible'
    html.toggleClass 'no-scroll'
    body.toggleClass 'no-scroll'
    return
  return
navArrows = [
  '\n    <span><svg class="icon icon-arrow-prev">\n        <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/src/web/static/images/sprite.svg#icon-arrow-prev"></use>\n    </svg></span>'
  '<span><svg class="icon icon-arrow-next">\n        <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/src/web/static/images/sprite.svg#icon-arrow-next"></use>\n    </svg></span>'
]
$(document).ready ->
  slider = $('.js-slider-details')
  slider.owlCarousel
    items: 3
    nav: true
    navElement: 'button'
    navText: navArrows
    dots: false
    loop: true
    smartSpeed: 700
    responsive:
      320: items: 1
      768: items: 2
      1024: items: 3
  # slider.on('changed.owl.carousel', function(event) {
  #     const items = slider.find('.owl-item');
  #     items.removeClass('left');
  #     items.eq(event.item.index).prevAll().addClass('left');
  # });
  # $(document).on('click', '.owl-item', function(){
  #     itemsIndex = $(this).index();
  #     slider.trigger('to.owl.carousel', itemsIndex);
  # });
  $('.js-slider-review').owlCarousel
    items: 1
    nav: true
    navElement: 'button'
    navText: navArrows
    dots: false
    loop: true
    smartSpeed: 700
    autoplay: true
    autoplayTimeout: 5000
    responsive:
      320:
        nav: false
        dots: true
      768:
        nav: true
        dots: false
  $('.js-slider-cases').owlCarousel
    items: 2
    nav: true
    navElement: 'button'
    navText: navArrows
    dots: false
    loop: true
    smartSpeed: 700
    responsive:
      320:
        nav: false
        dots: true
        items: 1
      768:
        nav: true
        dots: false
        items: 2
  return
do ->
  slider = $('.js-owl')

  owlMobileAlbum = (obj, itemsMobileAlbum, itemsMobilePortrait) ->
    `var mobilePoint`
    optionLoop = true
    if obj.is('[data-no-loop]')
      optionLoop = false
    optionAutoHeight = false
    if obj.is('[data-autoheight]')
      optionAutoHeight = true
    fullWidth = window.innerWidth
    if navigator.platform.indexOf('Win') > -1
      mobilePoint = 766
    else
      mobilePoint = 767
    # console.log(mobilePoint); 
    if fullWidth <= mobilePoint
      if !obj.hasClass('owl-carousel')
        obj.addClass 'owl-carousel'
        obj.owlCarousel
          items: itemsMobileAlbum
          nav: false
          dots: true
          loop: optionLoop
          smartSpeed: 600
          autoHeight: optionAutoHeight
          responsive:
            0: items: itemsMobilePortrait
            480: items: itemsMobileAlbum
    else
      obj.removeClass 'owl-carousel'
      obj.trigger 'destroy.owl.carousel'
    return

  owlMobilePortrait = (obj, itemsMobilePortrait) ->
    optionLoop = true
    if obj.is('[data-no-loop]')
      optionLoop = false
    optionAutoHeight = false
    if obj.is('[data-autoheight]')
      optionAutoHeight = true
    windowWidth = $(window).width()
    if windowWidth <= 479
      if !obj.hasClass('owl-carousel')
        obj.addClass 'owl-carousel'
        obj.owlCarousel
          items: itemsMobilePortrait
          nav: false
          dots: true
          smartSpeed: 600
          loop: optionLoop
          autoHeight: optionAutoHeight
    else
      obj.removeClass 'owl-carousel'
      obj.trigger 'destroy.owl.carousel'
    return

  if slider.length
    slider.each ->
      _this = $(this)
      itemsMobileAlbum = _this.data('items-mobile-album')
      itemsMobilePortrait = _this.data('items-mobile-portrait')
      console.log itemsMobileAlbum
      if itemsMobileAlbum and itemsMobilePortrait
        owlMobileAlbum _this, itemsMobileAlbum, itemsMobilePortrait
        $(window).resize ->
          owlMobileAlbum _this, itemsMobileAlbum, itemsMobilePortrait
          return
      if !itemsMobileAlbum and itemsMobilePortrait
        owlMobilePortrait _this, itemsMobilePortrait
        $(window).resize ->
          owlMobilePortrait _this, itemsMobilePortrait
          return
      return
  return
AOS.init()
do ->
  parallax = $('.js-parallax')
  if parallax.length
    parallax.each ->
      _this = $(this)
      scale = _this.data('scale')
      orientation = _this.data('orientation')
      new simpleParallax(_this[0],
        scale: scale
        orientation: orientation
        delay: .5
        overflow: true
        transition: 'cubic-bezier(0,0,0,1)')
      return
  return
do ->
  btn = $('.js-scroll')
  btn.click ->
    $('html, body').animate { scrollTop: $($(this).attr('href')).offset().top + 'px' }, duration: 1000
    false
  return

(function(){
  $(window).scroll(function () {
      var top = $(document).scrollTop();
      $('.corporate-jumbo').css({
        'background-position': '0px -'+(top/3).toFixed(2)+'px'
      });
      if(top > 50)
      {
        $('.navbar').addClass('navbar-inverse');
        $('.navbar').removeClass('navbar-transparent');
      }

      else
      {
      $('.navbar').addClass('navbar-default');
      $('.navbar').removeClass('navbar-inverse');
      }
  }).trigger('scroll');
})();

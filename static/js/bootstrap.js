$(function() {
  $(window).load(function() {
    if ($('#top-bar')) {
      $('#top-bar li a').each(function(index, element) {
        var classes = $(element).attr('class').split(' ');
        for (var key in classes) {
          if ($('body').hasClass(classes[key])) {
            $(element).parent().addClass('active');
            break;
          }
        }
      });
    }
    $('.nav .dropdown, .btn-group').mouseenter(function(){ if (!$(this).hasClass('open')) { $('> a.dropdown-toggle', this).click(); }});
    $('.tooltip').tooltip();
    $('.popover').popover();
    $("*[rel=popover]").popover();
  });
});

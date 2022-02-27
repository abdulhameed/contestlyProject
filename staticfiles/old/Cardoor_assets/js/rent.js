
$(function () {

  $(".js-create-rent").click(function() {
    $.ajax({
//      url: '/car/rent/create/',
       url: {% url 'rent_create' %},
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-rent").modal("show");
      },
      success: function (data) {
        $("#modal-rent .modal-content").html(data.html_form);
      }
    });
  });

});
$("form[name=adddata").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/alldata",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      console.log(resp);
      // window.location.href = "/dashboard/";
    },
    error: function(resp) {
      console.log(resp);
    }
  });

  e.preventDefault();
});


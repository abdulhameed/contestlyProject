    <!-- Paystack starts here -->
    <script src="https://js.paystack.co/v1/inline.js"></script>
    <script>
      //Custom script goes here
      $(document).ready(function () {
        //Trigger submit when make payment button is been clicked
        $("#purchasebtn").click(function (e) {
          e.preventDefault();
          //Submit details for payment
          var email = $("#email").val();
          var name = $("#name").val();
          var amount = $("#amount").val();
          //Check if email is empty
          if (email == "") {
            alert("Enter your email"); //display notification
            return; //i.e stop running query
          } else if (name == "") {
            alert("Enter your name"); //i.e display notification
            return; //i.e stop running query
          } else if (amount == "") {
            alert("Enter your amount"); //i.e display notification
            return; //i.e stop running query
          }
          //Run paystack query
          var handler = PaystackPop.setup({
            key: "{{pk_public}}",
            email: email,
            amount: amount + "00",
            currency: "NGN",
            ref: "" + Math.floor(Math.random() * 1000000000 + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
            metadata: {
              custom_fields: [
                {
                  display_name: name,
                  variable_name: name
                }
              ]
            },
            callback: function (response) {
              //   if transaction successful do this

                 alert('success. transaction ref is ' + response.reference);
              var referenceid = response.reference;
              //Make an http request to cart process
              $.ajax({
                type: "GET", //Send in POST Method
                url: "/verify/" + referenceid, //Endpoint for the ajax
                beforeSend: function () {
                  console.log("Sending request");
                  $(".alert").text("Sending request");
                },
                success: function (response) {
                  if (response[3].status == "success") {
                    //Once transaction completed redirect to complete page
                    $(".alert").removeClass("alert-warning");
                    $(".alert").addClass("alert-success");
                    $(".alert").text("Transaction verified");
                    console.log("Transaction verified");
                    $("form").trigger("reset");
                  } else {
                    $(".alert").text("Transaction reference not found");
                  }
                }
              });
            },
            onClose: function () {
              //Do stuff
            }
          });
          handler.openIframe();
        });
      });
    </script>
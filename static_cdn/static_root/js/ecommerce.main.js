$(document).ready(function(){

var stripeFormModule = $(".stripe-payment-form")

var stripeModuleToken = stripeFormModule.attr("data-token")

var stripeModuleNextUrl = stripeFormModule.attr("data-next-url")


var stripeTemplate = $.templates("#stripeTemplate")

var stripeTemplateDataContext = {
  publish_key: stripeModuleToken,
  next_url: stripeModuleNextUrl
}

var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)

stripeFormModule.html(stripeTemplateHtml)


var paymentForm = $(".payment-form")
if (paymentForm.length > 1){
	alert("Only one payment form is allowed per page")
	paymentForm.css('display', 'none')
}
else if (paymentForm.length == 1){

var pubKey = paymentForm.attr('data-token')

var nextUrl = paymentForm.attr('data-next-url')

var stripe = Stripe(pubKey);

	// A reference to Stripe.js

// var stripe = Stripe('pk_test_sDSJuqfqmePoOVohfLp65WoD00BzaBm3pW');

var elements = stripe.elements();

var style = {
  base: {
    color: "#32325d",
  }
};

var card = elements.create("card", { style: style });
card.mount("#card-element");

card.addEventListener('change', ({error}) => {
  const displayError = document.getElementById('card-errors');
  if (error) {
    displayError.textContent = error.message;
  } else {
    displayError.textContent = '';
  }
});

var form = document.getElementById('payment-form');



form.addEventListener('submit', function(event) {
  event.preventDefault();
  stripe.createToken(card).then(function(result) {
    if (result.error) {
      // Show error to your customer (e.g., insufficient funds)
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
      console.log(result.error.message);
    } else {
     
    	stripeTokenHandler(nextUrl,result.token);

    }
  });
 });

function redirectToNext(nextPath, timeoffset){

  if (nextPath){
   setTimeout(function(){
                window.location.href = nextPath
              },timeoffset) 
  }
}

function stripeTokenHandler(nextUrl, token){

	// console.log(token.id)

    var paymentMethodEndpoint = '/payment-method/create/'

    var data = {
      	'token': token.id
      }

    $.ajax({
      	type: 'POST',
      	data: data,
      	url: paymentMethodEndpoint,
      	success: function(data){
      		var successMsg = data.message || "Success! your card was added."
          card.clear()
      		// console.log(data)
      		// alert("this is succeded")
      		
      		// if (nextUrl){
      		// 	window.location.href = nextUrl
      		// }  //  else {
      		// 	window.location.reload()
      		// }
          if (nextUrl){
            successMsg = successMsg + "<br/><br/><i class='fa fa-spin fa-spinner'></i> Redirecting..."
          }
          if ($.alert){
            $.alert(successMsg)
          } else {
            alert(successMsg)
          }
          redirectToNext(nextUrl, 1500)

      	},
      	error: function(error){
      		console.log(error)
      		alert("this is an error")
      	}
    })

}

}

})
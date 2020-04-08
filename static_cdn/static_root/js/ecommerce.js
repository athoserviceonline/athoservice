$(document).ready(function(){
// Contact Form Handler
var contactForm = $(".contact-form")
var contactFormMethod = contactForm.attr("method")
var contactFormEndpoint = contactForm.attr("action") // /abc/

function displaySubmitting(submitBtn,defaultText, doSubmit){
if(doSubmit){
  submitBtn.addClass("disabled")
  submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
} else{
  submitBtn.removeClass("disabled")
  submitBtn.html(defaultText)
}
}

contactForm.submit(function(event){ 
event.preventDefault()

var contactFormSubmitBtn = contactForm.find("[type='submit']")
var contactFormSubmitBtntxt = contactFormSubmitBtn.text()

var contactFormData = contactForm.serialize()
var thisForm = $(this)
displaySubmitting(contactFormSubmitBtn,"",true)
$.ajax({
  method: contactFormMethod,
  url: contactFormEndpoint,
  data: contactFormData,
  success: function(data){
    contactForm[0].reset()
    
    setTimeout(function(){
      $.alert({title: "Success!!!", content: data.message, theme: "modern",}) 
    }, 500)

    setTimeout(function(){
      displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtntxt,false)
    }, 600)
  },
  error: function(error){
    console.log(error.responseJSON)

    var jsonData = error.responseJSON
    var msg = ""

    $.each(jsonData, function(key, value){
      msg += key + ": " + value[0].message + "<br/>"
    })

    setTimeout(function(){
      $.alert({title: "Oops!", content: msg, theme: "modern",})  
    }, 500)

    setTimeout(function(){
      displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtntxt,false)
    }, 600)

  }
})
})




// Auto Search

var searchForm = $(".search-form")
var searchInput = searchForm.find("[name='q']") //input name = q
var typingTimer;
var typingInterval = 1500 // .5 seconds
var searchBtn = searchForm.find("[type='submit']")

searchInput.keyup(function(event){
//key released
clearTimeout(typingTimer)
typingTimer = setTimeout(performSearch, typingInterval)
//console.log(event)
// console.log(searchInput.val())
// var query = searchInput.val()
// window.location.href='/search/?q=' + query 
})
// Cart + Add Products

searchInput.keydown(function(event){
// key pressed
clearTimeout(typingTimer)
})

function displaySearching(){
searchBtn.addClass("disabled")
searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
}

function performSearch(){
displaySearching()
var query = searchInput.val()
setTimeout(function(){window.location.href='/search/?q=' + query}, 1000)
}

var productForm = $(".form-product-ajax")

productForm.submit(function(event){
event.preventDefault();
// console.log("Form is not sending")
var thisForm = $(this)
// var actionEndpoint = thisForm.attr("action");
var actionEndpoint = thisForm.attr("data-endpoint");
var httpMethod = thisForm.attr("method");
var formData = thisForm.serialize();


$.ajax({
  url: actionEndpoint,
  method: httpMethod,
  data: formData,
  success: function(data){
    // console.log("success")
    // console.log(data)
    // console.log("Added", data.added)
    // console.log("Removed", data.removed)
    var submitSpan = thisForm.find(".submit-span")
    if (data.added){
     submitSpan.html("In Cart <button type='submit' class='btn btn-link btn-lg'>Remove?</button>") 
   } else {
    submitSpan.html("<button type='submit' class='btn btn-success btn-lg'>Add to cart</button>")
   }
    var navbarCount = $(".navbar-cart-count")
    navbarCount.text(data.cartItemCount)
    var currentPath = window.location.href 
    if (currentPath.indexOf("cart") != -1){
      refreshCart()
    }
  },
  error: function(errorData){
    $.alert({title: "Oops!", content: "An error occurred", theme: "modern",})
    // console.log("error")
    // console.log(errorData)
  }
})

})

function refreshCart(){
console.log("in current cart")
var cartTable = $(".cart-table")
var cartBody = cartTable.find(".cart-body")
// cartBody.html ("<h1>Changed</h1>")

var productRows = cartBody.find(".cart-product")
var  currentUrl = window.location.href

var refreshCartUrl='/api/cart/';
var refreshCartMethod = "GET";
var data = {};
$.ajax({
  url: refreshCartUrl,
  method: refreshCartMethod,
  data: data,
  success: function (data) {
   console.log("success")
   console.log(data)
   var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
   if(data.products.length > 0){
      productRows.html(" ")
      i = data.products.length
      $.each(data.products, function(index, value){
        console.log(value)
        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
        newCartItemRemove.css("display", "block")
        // newCartItemRemove.removeClass("hidden-class")
        newCartItemRemove.find(".cart-item-product_id").val(value.id)
        cartBody.prepend('<tr><th scope=\"row\">' + i + '</th><td><a href="' + value.url + '">' + value.name + '</a></td><td>' + value.price + '</td><td>'+ newCartItemRemove.html() +'</td><td><b>N/A</b></td></tr>')
        i -- 
      })
      
      cartBody.find(".cart-subtotal").text(data.subtotal)
      cartBody.find(".cart-total").text(data.total)
   } else {
    window.location.href = currentUrl
   }
  },
  error: function(errorData){
    $.alert({title: "Oops!", content: "An error occurred", theme: "modern",})
    // console.log("error")
    // console.log(errorData)
  }
})


}


})

// show and hide the password on click

$(document).on("click", ".toggle-password", function () {
  $(this).toggleClass("fa-regular fa-eye fa-eye-slash");
  const input = $("#password-input");
  // console.log("Input type before:", input.attr("type"));
  if (input.attr("type") === "password") {
    input.attr("type", "text");
  } else {
    input.attr("type", "password");
  }
});

// redirect btn to google auth & microsoft

const googleBtn = document.querySelector("#google");
const microsoftBtn = document.querySelector("#microsoft");
const github = document.querySelector('#github'); 
const inscription =document.querySelector('#inscription')
googleBtn.addEventListener("click", function (e) {
  e.preventDefault();
  window.location.href = "/login";
});
microsoftBtn.addEventListener("click", (e) => {
  e.preventDefault();
  window.location.href = "/getAToken";
});


github.addEventListener('click', (e) => {
  e.preventDefault();
  window.location.href = '/login/github'
})




// nofification close btn 

  const close =document.querySelector('.close')
  const notifEL = document.querySelector('.notification')
  document.addEventListener('DOMContentLoaded', function(){
    function hideNotification(){
      if(notifEL){
        notifEL.style.display ='none';
      }
    }
    setTimeout(hideNotification, 1000);

    if(close){
      close.addEventListener('click' ,hideNotification );
    }  
  })
 
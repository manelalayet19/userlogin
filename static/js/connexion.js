// animation based on the password 

const passwordInputEl = document.querySelector('#password-cnt') ; 

const emailInput =document.querySelector('#email-input')
const  btnCnx = document.querySelector('#conct-btn') 
const element = document.querySelector('.el')
const continueBrnEl = document.getElementById('continue-btn');  
const mail = document.querySelector('#mail')
const passEl = document.querySelector('#connct-pass')
const social = document.querySelector('.social')
const innerform = document.querySelector('form')
let emailProfile = document.querySelector('.profile-email'); 
const profile = document.querySelector('.profile'); 
const mdpsRest = document.querySelector('#mdps-oublier')
function inputError(){
if (!emailInput.value.includes('@')){
     element.textContent = 'Veuillez saisir une adresse e-mail valide et réessayer.'
}else{
    element.textContent=''
}


}


function displayPassword(e){
e.preventDefault() ; 
const valInput =  emailInput.value 

if (valInput.length > 0 ){
    continueBrnEl.style.backgroundColor ='#007aff'; 
    continueBrnEl.style.color ='white'; 

}else {
    continueBrnEl.style.backgroundColor ='transparent'; 
    continueBrnEl.style.color ='#092540'; 
}
}

function displaybtn(){
    mail.style.display='none' ; 
passEl.style.display ='block' ; 
social.style.display ='none'; 
profile.style.display ='flex' ; 
mdpsRest.style.display ='flex';
    innerform.style.height ='582.8px' 
passwordInputEl.style.dispaly ='block' ; 
if(passEl && passwordInputEl){
    continueBrnEl.style.display ='none'; 
    btnCnx.style.display ='block' ; 
    emailProfile.textContent = emailInput.value

}else{
    continueBrnEl.style.display ='block' ; 
    btnCnx.style.display ='none' ; 
}

}
function changeBtnBaseOnInput(){
    let passwordVal =passwordInputEl.value
    

    if(passwordVal.length > 0){
        btnCnx.style.backgroundColor ='#007aff'; 
        btnCnx.style.color ='white'; 

    }else{
        btnCnx.style.backgroundColor ='transparent';
        btnCnx.style.backgroundColor ='#092540'; 
    }
}

emailInput.addEventListener('input', displayPassword) ; 
emailInput.addEventListener('input', inputError)
continueBrnEl.addEventListener('click', displaybtn )
passwordInputEl.addEventListener('input', changeBtnBaseOnInput)

 // notification on each submit modification the flash always show the message no clear afterwards


document.addEventListener('DOMContentLoaded', function(){
    const notification = document.querySelector('.notification')
    const alert = document.querySelector('.alert')
    if(notification){
        setTimeout(()=>{
            alert.textContent=''
        }, 2000)
    }
})


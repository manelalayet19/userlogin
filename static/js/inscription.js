
// get the input value 
// if input value.length is diferent thAN  0 > 0 
// CHANGE THE BTN BG ? REMOVE INPUTS ID / EMAIL SHOW THE PASSWORD AND THE FAQ  

// hide these by on inscription pae only 
// #mdps-oubli, #inscription , #pass , .notification{
//   display:none ; 
// }
const inputID = document.querySelector('.inputID');
const email = document.querySelector('.emailInputGP');
const btContinue = document.querySelector('#btn-continue');
const password = document.querySelector('#pass');
const ins = document.querySelector('#inscription');
const hrefColorEl = document.querySelector('#href-continuer')
const notif = document.querySelector('.notification')
const meter = document.querySelector('.meter-evaluator')
const meterWrapper = document.querySelector('.meter')
const authenficateBTN = document.querySelector('.btns_authentificate')
const seperator = document.querySelector('.separator')
const innerform = document.querySelector('form')
const info = document.querySelector(".info")
function animatedInteraction() {
  const valsID = inputID.value
  const valEmail = email.value
  // console.log('valsID', valsID)
  // console.log('valEmail', valEmail)
  if (valsID.length > 0 && valEmail.length > 0) {
    btContinue.style.display = 'block';
    btContinue.style.backgroundColor = "#007aff";
    hrefColorEl.style.color = 'white';
    // notif.style.display = 'none';

  } else {
    btContinue.style.backgroundColor = 'transparent';
    hrefColorEl.style.color = "#092540";
    btContinue.style.display = 'block';
    // notif.style.display = 'none';
  }
}

email.addEventListener('input', animatedInteraction);
inputID.addEventListener('input', animatedInteraction);

animatedInteraction();

// on btn click hide emqil and input , display pass and remove the btn itself 
function removeItemsOnclick(e) {
  e.preventDefault()
  document.querySelector('.idItems').style.display = 'none';
  document.querySelector('.emailItems').style.display = 'none';
  document.querySelector('#mdps-oubli').style.display = 'flex';
  password.style.display = 'block';
  authenficateBTN.style.display='none'; 
  seperator.style.display ='none'; 
  innerform.style.height ='582.8px'
  meter.style.display = 'flex';
  info.style.display='flex'; 
  meterWrapper.style.display = 'block'; 
  // evaluateStrength()
  btContinue.removeEventListener('click', removeItemsOnclick)
  ModifyTheBtnType()
}

btContinue.addEventListener('click', removeItemsOnclick)

function ModifyTheBtnType() {
  const displayed = password.style.display === 'block'
  if (displayed) {
    btContinue.style.display = 'none'
    ins.style.display = 'block'
  }
}

// password strength evaluator 

const passwordInput = document.querySelector('#password-input')
const weakPass = document.querySelector('.weak')
const strongPass = document.querySelector('.strong')
const mediumPass = document.querySelector('.medium')
const textEl = document.querySelector('.textEl')
var spans = document.querySelectorAll('.meter-evaluator span');
function evaluateStrength(e) {
  e.preventDefault() ; 
  spans.forEach((sp)=> {
    sp.classList.remove('active', 'weak-color', 'medium-color', 'strong-color');
  })
  let passInput = passwordInput.value; 
  textEl.textContent = ''; 
  let regexLower = /[a-z]/;
  let regexUpper = /[A-Z]/;
  let regexNumber = /\d/;
  let regexSpecial = /[^a-zA-Z\d]/;
/* 
 weak  : Length is between 1 and 8 characters.
Contains either lowercase or uppercase characters.
Does not contain numbers or special characters.
Medium Password:
Length is between 8 and 12 characters inclusive.
Contains either lowercase or uppercase characters.
Contains numbers or special characters.
Strong Password:
Length is greater than 12 characters.
Contains lowercase, uppercase, numbers, and special characters.
*/

let isStrong = (passInput.length > 12) && 
  regexLower.test(passInput)&& 
  regexUpper.test(passInput) && 
  regexNumber.test(passInput) && 
  regexSpecial.test(passInput);

   let isMedium = !isStrong && 
  (passInput.length >= 8) && 
  (regexLower.test(passInput) || regexUpper.test(passInput)) && 
  (regexNumber.test(passInput) || regexSpecial.test(passInput)); 


  let isWeak = !isStrong && !isMedium && 
  (passInput.length > 0 && passInput.length <= 8) && 
  (regexLower.test(passInput) || regexUpper.test(passInput) || regexSpecial.test(passInput) ||regexNumber.test(passInput)) 
  
  meter.style.display = 'flex';
  meterWrapper.style.display = 'block'

  if (isWeak) {
    console.log('weak!', passInput.length)
    weakPass.classList.add('active','weak-color')
    
    textEl.textContent = 'Ce mot de passe est trop faible. Veuillez créer un mot de passe plus sûr.'
  }
  else if (isMedium) {
    weakPass.classList.add('active', 'medium-color');
    mediumPass.classList.add('active', 'medium-color')
    console.log('medium  ! ', passInput.length)
    textEl.textContent = 'C’est suffisant, mais vous devriez créer un mot de passe plus difficile à deviner.'
  }
  else if (isStrong) {
    mediumPass.classList.add('active', 'strong-color')
    weakPass.classList.add('active', 'strong-color')
    strongPass.classList.add('active', 'strong-color')
    console.log('strong pass ', passInput.length)
    textEl.textContent = 'Parfait ! Vous avez défini un mot de passe sûr.'
  }
  else {
    console.log('error') 
    spans.forEach((sp)=> {
      sp.style.backgroundColor = 'rgb(210 210 210)' ; 
    })
  }
}

passwordInput.addEventListener('input', evaluateStrength)
// make the btn create account change bg only whe the cchebox is checked 

const element  = document.querySelector('.form-check-input')
const BtnAccount = document.querySelector('.btn')
const link = document.getElementById('link')
function changeBgColorOnBtn(e){
e.preventDefault() ; 
if(element.checked){
  BtnAccount.style.backgroundColor = '#007aff' ; 
  link.style.color = 'white' ; 
}else {
  BtnAccount.style.backgroundColor = 'transparent' ; 
  link.style.color = '#092540' ; 
}
}
element.addEventListener('change', changeBgColorOnBtn )
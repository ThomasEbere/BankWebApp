console.log("We Dey Down ooooooo")

const deposit=document.querySelector('.sub-deposit');
const firstdepotext=document.querySelector('.newdeposit');
const seconddeposittext=document.querySelector('.deposits-menu');
const depositoption=document.querySelector('.deposit-page');
const successtext=document.querySelector('.success-transact');
const successmessage=document.querySelector('.deposit-option');

//deposit.addEventListener('submit', e=>{
//
//    function success(){
//        firstdepotext.style.setProperty('display','none');
//        seconddeposittext.style.setProperty('display','none');
//        depositoption.style.setProperty('display','none');
//        successtext.style.setProperty('display', 'block');
//        successmessage.style.setProperty('display', 'block');
//    }
//    setTimeout(success, 3000);
//});

function submitted(e){
    e.preventDefault();
    firstdepotext.style.setProperty('display','none');

}
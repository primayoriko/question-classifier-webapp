const buttonCheckGrammar =  document.querySelector("#buttonCheckGrammar");
const buttonSubmit = document.querySelector("#buttonSubmit");

function checkGrammar(event){
    event.preventDefault();
    const inputQuestion = document.getElementById("inputQuestion").value;
    console.log("checkGrammar");
    console.log(inputQuestion);
    // window.location.replace("");
}

function submitQuestion(event){
    event.preventDefault();
    const inputQuestion = document.getElementById("inputQuestion").value;
    console.log("submitQuestion");
    console.log(inputQuestion);
    // window.location.replace("");
}

buttonCheckGrammar.addEventListener('click', checkGrammar);
buttonSubmit.addEventListener('click', submitQuestion);
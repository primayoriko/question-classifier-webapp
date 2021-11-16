const buttonCheckGrammar =  document.querySelector("#buttonCheckGrammar");
const buttonCheckSimilarity =  document.querySelector("#buttonCheckSimilarity");
const buttonSubmit = document.querySelector("#buttonSubmit");
const buttonFindTopic = document.querySelector("#buttonFindTopic")

function checkGrammar(event){
    event.preventDefault();
    const inputQuestion = document.getElementById("inputQuestion").value;
    console.log("checkGrammar");
    console.log(inputQuestion);
    $.ajax({
        url: 'http://localhost:8000/api/questions/checker/grammar',
        method: "POST",
        contentType: 'application/json',
        data: JSON.stringify({"text": inputQuestion})
    }).done(function(responseBody) {
        console.log(responseBody);
        let isValidGrammar = responseBody['grammar_correctness']
        console.log(isValidGrammar)
        if (isValidGrammar){
            $("#resultGrammar").html("Passed: The grammar is correct")
        }
        else{
            $("#resultGrammar").html("Not passed: The grammar is wrong")
        }
    }).fail(function(jqXHR, textStatus){
        console.log(textStatus);
        alert("Error: " + textStatus);
    });
}
function checkGrammar(event){
    event.preventDefault();
    const inputQuestion = document.getElementById("inputQuestion").value;
    console.log("findTopic");
    console.log(inputQuestion);
    $.ajax({
        url: 'http://localhost:8000/api/questions/checker/topic',
        method: "POST",
        contentType: 'application/json',
        data: JSON.stringify({"text": inputQuestion})
    }).done(function(responseBody) {
        console.log(responseBody);
        let topicQuestion = responseBody['topic']
        console.log(topicQuestion)
        $("#resultTopic").html(topicQuestion)
    }).fail(function(jqXHR, textStatus){
        console.log(textStatus);
        alert("Error: " + textStatus);
    });
}
function checkSimilarity(event){
    event.preventDefault();
    const inputQuestion = document.getElementById("inputQuestion").value;
    console.log("checkSimilarity");
    console.log(inputQuestion);
    $.ajax({
        url: 'http://localhost:8000/api/questions/checker/similiar',
        method: "POST",
        contentType: 'application/json',
        data: JSON.stringify({"text": inputQuestion})
    }).done(function(responseBody) {
        console.log(responseBody);
        let listSimilarQuestion = responseBody['similiar_questions'];
        let resultHtml = "";
        if (listSimilarQuestion.length > 0){
            resultHtml += "<p>List of similar questions</p>";
            resultHtml += "<ul>"
            for (let i = 0; i<listSimilarQuestion.length; ++i){
                resultHtml += "<li>" + listSimilarQuestion[i]['question_text'] + "</li>";
            }
            resultHtml += "</ul>";
            console.log(resultHtml);
            $("#similarQuestions").html(resultHtml);
        }
        else{
            $("#similarQuestions").html("There is no similar question");
        }
    }).fail(function(jqXHR, textStatus){
        console.log(textStatus);
        alert("Error: " + textStatus);
    });   
}

function submitQuestion(event){
    event.preventDefault();
    const inputQuestion = document.getElementById("inputQuestion").value;
    console.log("submitQuestion");
    console.log(inputQuestion);
    $.ajax({
        url: 'http://localhost:8000/api/questions',
        method: "POST",
        contentType: 'application/json',
        data: JSON.stringify({"text": inputQuestion})
    }).done(function(responseBody) {
        console.log(responseBody);
        alert("Input success");
        window.location.href = "";
    }).fail(function(jqXHR, textStatus){
        console.log(textStatus);
        alert("Error: " + textStatus);
    });   
}

buttonCheckGrammar.addEventListener('click', checkGrammar);
buttonCheckSimilarity.addEventListener('click', checkSimilarity);
buttonSubmit.addEventListener('click', submitQuestion);
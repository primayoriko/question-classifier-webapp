function showAllQuestions(){
    $.ajax({
        method: "GET",
        url: `http://localhost:8000/api/questions`,
      }).done(function(responseBody) {
        console.log(responseBody);
        htmlResult = `<table>
        <tr>
        <th>Question</th>
        <th>Topic</th>
        </tr>`;
        for (const [topic, listQuestion] of Object.entries(responseBody)){
            for (let i = 0; i<listQuestion.length; ++i){
                htmlResult += `<tr>
                <td>${listQuestion[i].question_text}</td>
                <td>${listQuestion[i].topic}</td>
                </tr>`
            }
        }
        htmlResult += `</table>`
        $("#listQuestion").html(htmlResult);
    });

    
}

showAllQuestions();
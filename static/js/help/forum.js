$(document).ready(function () {
    var para = document.createElement("p");
    var inputcomment = document.createTextNode("HI THERE");
    para.appendChild(inputcomment);
    var element = document.getElementById("commentsection");
    element.appendChild(para);
});


console.log((my_js_data["comment"]));
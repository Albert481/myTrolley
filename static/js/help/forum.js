var my_js_data = JSON.parse('{"comment1": "hi i like trolleys", "comment2": "Hello world!", "comment3": "gtg"}');
$(document).ready(function () {
    var para = document.createElement("p");
    var inputcomment = document.createTextNode("HI THERE");
    para.appendChild(inputcomment);
    var element = document.getElementById("commentsection");
    element.appendChild(para);
});


alert(my_js_data["comment1"]);
alert(my_js_data["comment2"]);

//var my_js_data = ["{{javascript_out"];
//console.log((my_js_data["comment"]));
//console.log(my_js_data);
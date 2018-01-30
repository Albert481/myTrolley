var my_js_data = JSON.parse('{"comment1": "hi i like trolleys", "comment2": "Hello world!"}');
var my_js_data = JSON.parse('{"comment1": "hi i like trolleys", "comment2": "Hello world!"}');
var my_js_data = JSON.parse('{"comment1": "hi i like trolleys", "comment2": "Hello world!"}');
var my_js_data = JSON.parse('{"comment1": "hi i like trolleys", "comment2": "Hello world!"}');
var my_js_data = JSON.parse('{"comment1": "hi i like trolleys", "comment2": "Hello world!"}');
var my_js_data = JSON.parse('{"comment1": "hi i like trolleys", "comment2": "Hello world!"}');
//var dict_keys = Object.keys(my_js_data);
//console.log(dict_keys);

for (var i in my_js_data) {
    // check if the key is defined in the object itself, not in parent
    if (my_js_data.hasOwnProperty(i)) {
        //console.log(my_js_data[i]);

        var para = document.createElement("div");   // create div element
        var firebase_comments = document.createTextNode(my_js_data[i]);     // text node with values from database
        para.appendChild(firebase_comments);    // append text node into div element
        para.className = "databasecomments";  // create class name for div element
        var element = document.getElementById("commentsection");    // get ID: 'commentsection' in html page
        element.appendChild(para);  // append var para into element
    }
}
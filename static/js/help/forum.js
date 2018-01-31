var my_js_data = JSON.parse('{"comment1": "Hi I like trolleys!", "comment2": "Hello world!", "comment3": "Blue moon", "comment4": "dadadada", "comment5": "Help!"}');var username_js_data = JSON.parse('["Albert", "Albert", "Albert", "Albert", "Albert"]');
var my_js_data = JSON.parse('{"comment1": "Hi I like trolleys!", "comment2": "Hello world!", "comment3": "Blue moon", "comment4": "dadadada"}');var username_js_data = JSON.parse('["Albert", "Albert", "Albert", "Albert"]');
var my_js_data = JSON.parse('{"comment1": "Hi I like trolleys!", "comment2": "Hello world!", "comment3": "Blue moon", "comment4": "dadadada"}');var username_js_data = JSON.parse('["Albert", "Albert", "Albert", "Albert"]');

//var dict_keys = Object.keys(my_js_data);
//console.log(dict_keys);

function disableComment() {
    alert("Log in to post a comment!");
    //var leavepage = confirm('Do you want to log in to your account?');
    //if (leavepage === true){
        //window.location = "login.html";
        //return false;       //When a form is submitted, it cancels any ongoing HTTP requests
    //} else {
        //nothing
    //}
}

for (var k in username_js_data) {               // check if the key is defined in the object itself, not in parent
    if (username_js_data.hasOwnProperty(k)) {
        if (my_js_data.hasOwnProperty(k)) {

            var userpara = document.createElement("div");
            var firebase_usernames = document.createTextNode(username_js_data[k]);
            userpara.appendChild(firebase_usernames);
            userpara.className = "databasenames";
            var elementname = document.getElementById("commentsection");
            elementname.appendChild(userpara);

            var para = document.createElement("div");           // create div element
            var firebase_comments = document.createTextNode(my_js_data[k]);             // text node with values from database
            para.appendChild(firebase_comments);            // append text node into div element
            para.className = "databasecomments";        // create class name for div element
            var element = document.getElementById("commentsection");            // get ID: 'commentsection' in html page
            element.appendChild(para);          // append var para into element
            //console.log(i);
            console.log(k);
        }
    }
}



/*
for (var i in my_js_data) {
    // check if the key is defined in the object itself, not in parent
    if (my_js_data.hasOwnProperty(i)) {
        //console.log(my_js_data[i]);

        var para = document.createElement("div");           // create div element
        var firebase_comments = document.createTextNode(my_js_data[i]);             // text node with values from database
        para.appendChild(firebase_comments);            // append text node into div element
        para.className = "databasecomments";        // create class name for div element
        var element = document.getElementById("commentsection");            // get ID: 'commentsection' in html page
        element.appendChild(para);          // append var para into element
    }
}
*/
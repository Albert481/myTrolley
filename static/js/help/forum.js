
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

/*
for (var y in my_js_data) {
    // check if the key is defined in the object itself, not in parent
    if (my_js_data.hasOwnProperty(y)) {
        var commentvalue = my_js_data[y];

        for (z=0; z < Object.keys(my_js_data).length; z++) {
            var usernamevalue = username_js_data[z];
            var new_dict = {}
            new_dict[usernamevalue] = commentvalue;

            console.log(new_dict);
        }
    }
}
*/

/*
for (z=0; z < Object.keys(my_js_data).length; z++){
    var usernamevalue = username_js_data[z];
    var new_dict = {}
    new_dict[usernamevalue] = commentvalue;

    console.log(new_dict);
}
*/

/*
loop1:
for (var k in username_js_data) {
    if (username_js_data.hasOwnProperty(k)) {           // check if the key is defined in the object itself, not in parent
        console.log(k);
        var userpara = document.createElement("div");
        var firebase_usernames = document.createTextNode(username_js_data[k] + ":");
        userpara.appendChild(firebase_usernames);
        userpara.className = "databasenames";
        var elementname = document.getElementById("commentsection");
        elementname.appendChild(userpara);

        for (var i in my_js_data) {
            if (my_js_data.hasOwnProperty(i)) {
                console.log(i);
                var para = document.createElement("div");           // create div element
                var firebase_comments = document.createTextNode(my_js_data[i]);             // text node with values from database
                para.appendChild(firebase_comments);            // append text node into div element
                para.className = "databasecomments";        // create class name for div element
                var element = document.getElementById("commentsection");            // get ID: 'commentsection' in html page
                element.appendChild(para);          // append var para into element
                continue loop1;
            }
        }
    }
}
*/

for (var key in my_js_data) {
        if (my_js_data.hasOwnProperty(key)) {
            //console.log(key + " -> " + my_js_data[key]);

            var userpara = document.createElement("div");
            var firebase_usernames = document.createTextNode(key);
            userpara.appendChild(firebase_usernames);
            userpara.className = "databasenames"
            var userelement = document.getElementById("commentsection");
            userelement.appendChild(userpara);

            var para = document.createElement("div");           // create div element
            var firebase_comments = document.createTextNode(my_js_data[key]);             // text node with values from database
            para.appendChild(firebase_comments);            // append text node into div element
            para.className = "databasecomments";        // create class name for div element
            var element = document.getElementById("commentsection");            // get ID: 'commentsection' in html page
            element.appendChild(para);          // append var para into element
        }
    }

/*
function js_load_comments() {
    for (var key in my_js_data) {
        if (my_js_data.hasOwnProperty(key)) {
            //console.log(key + " -> " + my_js_data[key]);

            var userpara = document.createElement("div");
            var firebase_usernames = document.createTextNode(key);
            userpara.appendChild(firebase_usernames);
            userpara.className = "databasenames"
            var userelement = document.getElementById("commentsection");
            userelement.appendChild(userpara);

            var para = document.createElement("div");           // create div element
            var firebase_comments = document.createTextNode(my_js_data[key]);             // text node with values from database
            para.appendChild(firebase_comments);            // append text node into div element
            para.className = "databasecomments";        // create class name for div element
            var element = document.getElementById("commentsection");            // get ID: 'commentsection' in html page
            element.appendChild(para);          // append var para into element
        }
    }
}
*/

/*
$( document ).ready(function() {
    js_load_comments();
});
*/

// Initialize Firebase
var config = {
    apiKey: "AIzaSyBwPlW-TqggkUeA69NI0DBAAjoxeKGiN3s",
    authDomain: "smarttrolley-c024a.firebaseapp.com",
    databaseURL: "https://smarttrolley-c024a.firebaseio.com",
    projectId: "smarttrolley-c024a",
    storageBucket: "smarttrolley-c024a.appspot.com",
    messagingSenderId: "260911627861"
  };
  firebase.initializeApp(config);

// Reference messages collection
var messagesRef = firebase.database().ref('messages');

// Listen for form submit
    document.getElementById('contactForm').addEventListener('submit', submitForm)

// Submit form
function submitForm(e) {
        e.preventDefault();
    }

    // Get values
    var username = getInputVal('username');
    var email = getInputVal('email');
    var password = getInputVal('password');

    // Save message
    saveMessage(username, email, password);
}

// Function to get get form values
function getInputVal(id) {
    return document.getElementById(id).value
}

// Save message to firebase
function saveMessage(username, email, password) {
    var newMessageRef = messagesRef.push();
    newMessageRef.set({
        username: username,
        email: email,
        password: password,
    });
}



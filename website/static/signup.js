// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation');
    
    var inputs;
    var passwords = [];
    // var passwordsMatch;
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms).forEach(function (form) {
        
            form.addEventListener('submit', function (event) {

                // inputs = form.getElementsByTagName("input");
                // for (var i=0; i<inputs.length; i++) {
                //     if (inputs[i].type.toLowerCase() === "password") {
                //         passwords.push(inputs[i].value);
                //       }
                // }
                // passwordsMatch = passwords.every( (val, i, arr) => val === arr[0] );
                // console.log(passwords);
                // console.log(passwordsMatch);

                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
  
                form.classList.add('was-validated');
            }, false)
        })
})()

function firstNameCheck(element) {
    var firstName = element.value;

    if (firstName.length >= 3) {
        element.classList.remove('is-invalid');
        element.classList.add('is-valid');
    } else {
        element.classList.remove('is-valid');
        element.classList.add('is-invalid');
    }
}

function emailCheck(element) {
    var email = element.value;

    var re = /\S+@\S+\.\S+/;  // email format anystring@anystring.anystring
    if (re.test(email)) {
        element.classList.remove('is-invalid');
        element.classList.add('is-valid');
    } else {
        element.classList.remove('is-valid');
        element.classList.add('is-invalid');
    }
}

function passwordsMatchAndValid(element) {

    var passwordsMatch = (function() {
        var inputs = document.getElementsByTagName("input");
        var passwords = [];
        for (var i=0; i<inputs.length; i++) {
            if (inputs[i].type.toLowerCase() === "password") {
                passwords.push(inputs[i].value);
                }
        }
        return passwords.every( (val, i, arr) => val === arr[0] );
    })();
    var inputPassword1Valid = document.getElementById('inputPassword1').classList.contains('is-valid');

    if (passwordsMatch && inputPassword1Valid) {
        element.classList.remove('is-invalid');
        element.classList.add('is-valid');
    } else if (!(inputPassword1Valid)) {
        element.classList.remove('is-invalid');
        element.classList.remove('is-valid');
    } else {
        element.classList.remove('is-valid');
        element.classList.add('is-invalid');
    }
}

function passwordStrengthCheck(element) {
    var password = element.value;
    var feedbackText = [];
    var textp;

    element.parentNode.querySelectorAll(':scope > .invalid-feedback')[0].innerHTML = '';

    if (password == '') {
        textp = document.createElement('p');
        textp.innerText = 'Enter a password:';
        element.parentNode.querySelectorAll(':scope > .invalid-feedback')[0].appendChild(textp);
        return 0;
    }

    if (password.length < 8) {
        feedbackText.push("at least 8 characters");
    }

    for (var i=0; i<password.length; i++) {
        if ('abcdefghijklmnopqrstuvwxyz'.indexOf(password[i]) == -1) {
            if (i == password.length - 1) {
                feedbackText.push("lower case");
            }
        } else {
            break;
        }
    }

    for (var i=0; i<password.length; i++) {
        if ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.indexOf(password[i]) == -1) {
            if (i == password.length - 1) {
                feedbackText.push("upper case");
            }
        } else {
            break;
        }
    }

    for (var n=0; n<10; n++) {
        if (password.indexOf(n.toString()) > -1) {
            break;
        } else if (n == 9) {
            feedbackText.push("a number");
        } else {
            continue;
        }
    }

    console.log(feedbackText);

    if (feedbackText.length == 0) {
        element.classList.remove('is-invalid');
        element.classList.add('is-valid');
    } else {

        textp = document.createElement('p');
        textp.innerHTML = 'Must contain: ';
        element.parentNode.querySelectorAll(':scope > .invalid-feedback')[0].appendChild(textp);

        textp = document.createElement('p');
        feedbackText.forEach((text, index, array) => {
            if (index >= 1) {
                textp.innerHTML += ', ';
            }
            // textp = document.createElement('p');
            textp.innerText += text;
        });

        element.parentNode.querySelectorAll(':scope > .invalid-feedback')[0].appendChild(textp);

        element.classList.remove('is-valid');
        element.classList.add('is-invalid');

    }

    // for (var i=0; i<password.length; i++) {
    //     if ('abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'.indexOf(password[i]) > -1) {
    //         if (i == password.length - 1) {
    //             feedbackText.push("Password must contain a special character");
    //         }
    //     } else {
    //         break;
    //     }
    // }

    // password.parentNode.childNodes.querySelectorAll('.invalid-feedback').value = "";
}

function toNextPage(element) {
    var currentSection = element.parentNode.parentNode;

    // validate that currentSection has valid inputs

    var inputs;
    inputs = currentSection.getElementsByTagName("input");
    for (var i=0; i < inputs.length; i++) {
        if (!(inputs[i].classList.contains('is-valid'))) {
            return 0;
        } 
    }

    var nextSection = currentSection.nextSibling;
    while(nextSection && nextSection.nodeType != 1) {  // For browsers that check for whitespace
        
        nextSection = nextSection.nextSibling;
    }

    // currentSection.classList.add('hide-section');
    nextSection.style.display = 'block';
    // window.setTimeout(function () {
        currentSection.style.display = 'none';
    // }, 1000);

    // window.setTimeout(function () {
        // nextSection.classList.toggle('start-hidden');
    // }, 1000);
}

function backPage(element) {
    var currentSection = element.parentNode.parentNode;

    var previousSection = currentSection.previousSibling;
    while(previousSection && previousSection.nodeType != 1) {  // For browsers that check for whitespace
        
        previousSection = previousSection.previousSibling;
    }

    // currentSection.classList.add('hide-section');
    previousSection.style.display = 'block';
    // window.setTimeout(function () {
    currentSection.style.display = 'none';
    // }, 1000);

    // window.setTimeout(function () {
        // nextSection.classList.toggle('start-hidden');
    // }, 1000);
}

function toggleReproduction(element) {
    var selectedSex = element.id;

    if (selectedSex.indexOf('Female') > -1) {
        document.getElementById('inputReproduction').parentNode.style.visibility = 'visible';
        document.getElementById('inputReproduction').value = '';
    } else if (selectedSex.indexOf('Male') > -1) {
        document.getElementById('inputReproduction').parentNode.style.visibility = 'hidden';
    } else {
        console.log("Error when toggling inputReproduction");
    }
}
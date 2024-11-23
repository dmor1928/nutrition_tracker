// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
    
    var inputs;
    var passwords = [];
    var passwordsMatch;
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {

                inputs = form.getElementsByTagName("input");
                for (var i=0; i<inputs.length; i++) {
                    if (inputs[i].type.toLowerCase() === "password") {
                        passwords.push(inputs[i].value);
                      }
                }
                passwordsMatch = passwords.every( (val, i, arr) => val === arr[0] );
                console.log(passwords);
                console.log(passwordsMatch);

                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
  
                form.classList.add('was-validated');
            }, false)
      })
  })()


function passwordsMatch(element) {
    var inputs = document.getElementsByTagName("input");
    var passwords = [];
    var passwordsMatch;

    for (var i=0; i<inputs.length; i++) {
        if (inputs[i].type.toLowerCase() === "password") {
            passwords.push(inputs[i].value);
            }
    }

    passwordsMatch = passwords.every( (val, i, arr) => val === arr[0] );

    console.log(passwords);
    console.log(passwordsMatch);

    if (passwordsMatch) {
        element.classList.remove('is-invalid');
        element.classList.add('is-valid');
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
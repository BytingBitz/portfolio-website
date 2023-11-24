
// Footer Copyright
var footertext = document.getElementById('footertext')
var text = (((new Date().getFullYear()).toString()).concat(' \u00A9 Jordan Amalfitano'))
var footercontent = document.createTextNode(text)
footertext.appendChild(footercontent)

//Menu Active
function getClosest(elem, selector) {
    // Element.matches() polyfill
    if (!Element.prototype.matches) {
        Element.prototype.matches =
            Element.prototype.matchesSelector ||
            Element.prototype.mozMatchesSelector ||
            Element.prototype.msMatchesSelector ||
            Element.prototype.oMatchesSelector ||
            Element.prototype.webkitMatchesSelector ||
            function (s) {
                var matches = (this.document || this.ownerDocument).querySelectorAll(s),
                    i = matches.length;
                while (--i >= 0 && matches.item(i) !== this) { }
                return i > -1;
            };
    }
    // Get the closest matching element
    for (; elem && elem !== document; elem = elem.parentNode) {
        if (elem.matches(selector)) return elem;
    }
    return null;
};
function activateMenu() {
    var menuItems = document.getElementsByClassName("sub-menu-item");
    if (menuItems) {
        var matchingMenuItem = null;
        for (var idx = 0; idx < menuItems.length; idx++) {
            if (menuItems[idx].href === window.location.href) {
                matchingMenuItem = menuItems[idx];
            }
        }
        if (matchingMenuItem) {
            matchingMenuItem.classList.add('active');
            var immediateParent = getClosest(matchingMenuItem, 'li');
            if (immediateParent) {
                immediateParent.classList.add('active');
            }
            var parent = getClosest(matchingMenuItem, '.parent-menu-item');
            if (parent) {
                parent.classList.add('active');
                var parentMenuitem = parent.querySelector('.menu-item');
                if (parentMenuitem) {
                    parentMenuitem.classList.add('active');
                }
                var parentOfParent = getClosest(parent, '.parent-parent-menu-item');
                if (parentOfParent) {
                    parentOfParent.classList.add('active');
                }
            } else {
                var parentOfParent = getClosest(matchingMenuItem, '.parent-parent-menu-item');
                if (parentOfParent) {
                    parentOfParent.classList.add('active');
                }
            }
        }
    }
}

function componentToHex(value) {
    var hex = value.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(rgb) {
    return "#" + componentToHex(rgb[0]) + componentToHex(rgb[1]) + componentToHex(rgb[2]);
}

function getRandColor(brightness) {
    // Six levels of brightness from 0 to 5, 0 being the darkest
    var num = [Math.random() * 256, Math.random() * 256, Math.random() * 256];
    var mix = [brightness*51, brightness*51, brightness*51]; //51 => 255/5
    var rgb = [num[0] + mix[0], num[1] + mix[1], num[2] + mix[2]].map(function(x){ return Math.round(x/2.0)})
    return rgbToHex(rgb);
}

function getNewShade(hexColor, magnitude) {
    hexColor = hexColor.replace(`#`, ``);
    if (hexColor.length === 6) {
        const decimalColor = parseInt(hexColor, 16);
        let r = (decimalColor >> 16) + magnitude;
        r > 255 && (r = 255);
        r < 0 && (r = 0);
        let g = (decimalColor & 0x0000ff) + magnitude;
        g > 255 && (g = 255);
        g < 0 && (g = 0);
        let b = ((decimalColor >> 8) & 0x00ff) + magnitude;
        b > 255 && (b = 255);
        b < 0 && (b = 0);
        return `#${(g | (b << 8) | (r << 16)).toString(16)}`;
    } else {
        return hexColor;
    }
}

document.getElementById('colour-button').onclick = function () {
    var new_colour = getRandColor(3);
    var new_dark_colour = getNewShade(new_colour, -25);
    var colour = {
        main: new_colour,
        dark: new_dark_colour
    };
    localStorage.setItem("colour", JSON.stringify(colour));
    loadColour();
}

function loadColour() {
    var colour = JSON.parse(localStorage.getItem("colour"));
    if (!colour)
        var colour = {
            main: "#fe5f55", 
            dark: "#fd4337"
        };
    var root = document.querySelector(":root");
    root.style.setProperty("--colour-main", colour["main"]);
    root.style.setProperty("--colour-dark", colour["dark"]);
}
loadColour();

window.onload = function loader() {
    activateMenu();
}

function fadeIn() {
    var fade = document.getElementById("error-msg");
    var opacity = 0;
    var intervalID = setInterval(function () {
        if (opacity < 1) {
            opacity = opacity + 0.5
            fade.style.opacity = opacity;
        } else {
            clearInterval(intervalID);
        }
    }, 200);
}

try {
    var slideIndex = 1;
    showSlides(slideIndex);
}
catch (e) {}

try {
    document.getElementById('prev-button').onclick = function () {plusSlides(-1)}
    document.getElementById('next-button').onclick = function () {plusSlides(-1)}
}
catch (e) {}

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("carousel-slide");
    if(n > slides.length) {
        slideIndex = 1
    }
    if(n < 1) {
        slideIndex = slides.length
    }
    for(i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex - 1].style.display = "block";
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('contactForm').addEventListener('submit', function(event) {
        var submitButton = document.getElementById('contactFormSubmit');
        submitButton.blur();
        if (!contactValidation(event)) {
            event.preventDefault(); // Prevent form submission if validation fails
            return false;
        }
        submitButton.disabled = true;
        submitButton.value = 'Sending...';
    });
});

const contactValidation = (event) => {
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var subject = document.getElementById('subject').value;
    var message = document.getElementById('comments').value;
    if (name.length === 0 || name.length > 60) {
        event.preventDefault();
        document.getElementById('error-msg').innerText = "Name is required and must not exceed 60 characters.";
        return false;
    }
    var emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (email.length === 0 || email.length > 60 || !emailRegex.test(email)) {
        event.preventDefault();
        document.getElementById('error-msg').innerText = "Email is required, must be a valid email address and must not exceed 60 characters.";
        return false;
    }
    if (subject.length === 0 || subject.length > 60) {
        event.preventDefault();
        document.getElementById('error-msg').innerText = "Subject is required and must not exceed 60 characters.";
        return false;
    }
    if (message.length === 0 || message.length > 1000) {
        event.preventDefault();
        document.getElementById('error-msg').innerText = "Message is required and must not exceed 1000 characters.";
        return false;
    }
    document.getElementById('error-msg').innerText = "";
    return true;
};

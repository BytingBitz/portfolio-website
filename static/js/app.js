/*   
    File Description: Main JS file of the template
*/


// feather icon
feather.replace()



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

window.onload = function loader() {
    // Menus
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

// Set Default Mode
defaultMode();
function defaultMode(e) {
    console.log('test')
    if (window.localStorage.getItem('mode') == null) {
        var mode = 'light'
    }else{
        var mode = window.localStorage.getItem('mode');
    }
    if (mode == "light") {
        var x = document.getElementById("app-css");  
        var y = document.getElementById("mode");  
        x.setAttribute('href', '../static/css/style.css')
        y.setAttribute('data-class', mode)
    }else{
        var x = document.getElementById("app-css");
        var y = document.getElementById("mode");  
        x.setAttribute('href', '../static/css/style-dark.css')
        y.setAttribute('data-class', mode)
    }    
}


// light/dark mode button
function changeMode(event) {
    var currentMode = event.currentTarget.dataset.class;
    var x = document.getElementById("app-css");
    var y = document.getElementById("mode");
    if (currentMode === "light") {
        x.setAttribute('href', '../static/css/style-dark.css');
        y.setAttribute('data-class', 'dark');
        window.localStorage.removeItem('mode');
        window.localStorage.setItem("mode", "dark");
    } else {
        x.setAttribute('href', '../static/css/style.css');
        y.setAttribute('data-class', 'light');
        window.localStorage.removeItem('mode');
        window.localStorage.setItem("mode", "light");
    }
}

// Swicher
function toggleSwitcher() {
    var i = document.getElementById('style-switcher');
    if (i.style.left === "-189px") {
        i.style.left = "-0px";
    } else {
        i.style.left = "-189px";
    }
};

function setColor(theme) {
    window.localStorage.removeItem('color');
    window.localStorage.setItem("color", theme);
    document.getElementById('color-opt').href = '../static/css/colors/' + theme + '.css';
    toggleSwitcher(false);
};

// Set Default  Color
defaultColor();
function defaultColor(e) {
    if (window.localStorage.getItem('color') == null) {
        color = 'default'
    }else{
        color = window.localStorage.getItem('color');
    }
    document.getElementById('color-opt').href = '../static/css/colors/' + color + '.css';
}


// To remove section content from index and contact page
if(window.location.pathname == '/contact' || window.location.pathname == '/'
    || window.location.pathname == '/blog/singlepost') {
    document.getElementById('brand_logo').style.display = "none" ;
}

if(window.location.pathname == '/shop/products' || window.location.pathname == '/shop/productlist'
    || window.location.pathname == '/blog/bloglisting' || window.location.pathname == '/blog/bloggrid') {
    document.getElementById('title_logo').style.display = "none";
}
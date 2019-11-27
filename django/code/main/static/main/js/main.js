"use strict";

// SPMenu
var btn = document.getElementsByClassName("hamburger")[0];
btn.onclick = function() {
  if (btn.classList.contains("is-active")) {
    btn.classList.remove("is-active");
    document.getElementsByClassName("global-sp-menu")[0].classList.remove("expanded");
    document.body.classList.remove("open-menu");
  } else {
    window.scrollTo(0, 0);
    btn.classList.add("is-active");
    document.getElementsByClassName("global-sp-menu")[0].classList.add("expanded");
    document.body.classList.add("open-menu");
  }
};
var sp_menu_a = Array.prototype.slice.call(document.querySelectorAll(".global-sp-menu a"),0)
sp_menu_a.forEach(function (item) {
  item.onclick = function () {
    btn.classList.remove("is-active");
    document.getElementsByClassName("global-sp-menu")[0].classList.remove("expanded");
    document.body.classList.remove("open-menu");
  };
});

// SmoothScroll
var scrollElm = function() {
  if ('scrollingElement' in document) return document.scrollingElement;
  if (navigator.userAgent.indexOf('WebKit') != -1) return document.body;
  return document.documentElement;
}();
(function () {
  var duration = 500;
  var ignore = '.noscroll';
  var easing = function easing(t, b, c, d) {
    return c * ((t = t / d - 1) * t * t + 1) + b;
  };
  var smoothScrollElm = document.querySelectorAll('a[href^="#"]:not(' + ignore + ')');
  Array.prototype.forEach.call(smoothScrollElm, function (elm) {
    elm.addEventListener('click', function (e) {
      e.preventDefault();
      var targetElm;
      try {
        targetElm = document.querySelector(elm.getAttribute('href'));
        if (!targetElm) throw "";
      } catch (e) {
        targetElm = document.body;
      }
      var targetPos = targetElm.getBoundingClientRect().top;
      var startTime = Date.now();
      var scrollFrom = scrollElm.scrollTop;
      (function loop() {
        var currentTime = Date.now() - startTime;
        if (currentTime < duration) {
          scrollTo(0, easing(currentTime, scrollFrom, targetPos, duration));
          window.requestAnimationFrame(loop);
        } else {
          scrollTo(0, targetPos + scrollFrom);
        }
      })();
    });
  });
})();

// ColorChanger
function colorChange() {
  var ay = document.querySelector("body > header").clientHeight + document.querySelector("body > header").getBoundingClientRect().top;
  var fy = document.getElementsByClassName("global-footer")[0].getBoundingClientRect().top;
  var sidebar_li = Array.prototype.slice.call(document.querySelectorAll(".global-sidebar li"),0);
  sidebar_li.forEach(function (item) {
    var sp = item.getBoundingClientRect().top + item.clientHeight / 2;
    if (ay < sp && sp < fy) {
      item.classList.add("black-chara");
      item.classList.remove("white-chara");
    } else {
      item.classList.add("white-chara");
      item.classList.remove("black-chara");
    }
  });
};
colorChange();
window.onscroll = function(){colorChange();};
window.onresize = function(){colorChange();};

(function () {
  "use strict";
  var nav = document.querySelector(".nav");
  if (!nav) return;
  var button = nav.querySelector(".primary-menu");
  var links = nav.querySelector(".nav-links");
  if (!button || !links) return;
  var active = links.querySelector(".active");
  button.querySelector("span").textContent = active ? active.textContent : "Menu";
  button.setAttribute("aria-label", "Navigation: " + button.querySelector("span").textContent);
  function close() {
    nav.classList.remove("is-open");
    button.setAttribute("aria-expanded", "false");
  }
  button.addEventListener("click", function () {
    var open = button.getAttribute("aria-expanded") !== "true";
    nav.classList.toggle("is-open", open);
    button.setAttribute("aria-expanded", String(open));
  });
  links.addEventListener("click", function (event) {
    if (event.target.closest("a")) close();
  });
  document.addEventListener("click", function (event) {
    if (!nav.contains(event.target)) close();
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && button.getAttribute("aria-expanded") === "true") {
      close();
      button.focus();
    }
  });
  window.matchMedia("(max-width:700px)").addEventListener("change", close);
}());

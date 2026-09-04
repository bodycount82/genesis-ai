/* GENESIS prototype — shared page chrome */
(function () {
  "use strict";

  // --- nav active state ---
  var path = (location.pathname.split("/").pop() || "index.html").toLowerCase();
  document.querySelectorAll(".nav-links a").forEach(function (a) {
    var href = (a.getAttribute("href") || "").toLowerCase();
    if (href === path) a.classList.add("active");
  });

  // --- reveal on scroll ---
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach(function (el) {
    el.classList.add("in"); // default visible if IO unavailable
    if ("IntersectionObserver" in window) { el.classList.remove("in"); io.observe(el); }
  });

  // --- footer year ---
  var y = document.getElementById("yr");
  if (y) y.textContent = new Date().getFullYear();
})();

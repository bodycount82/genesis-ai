/* Runs in <head> of every shell page (index.html, memory.html, ...).
   A shell must only ever exist once, at the top of the tab. If a shell page
   ends up inside the site frame (a link clicked before the frame was wired
   up, a restored history entry, ...), hand the route back to the real shell
   and swap this frame to the plain view page, so no second soundtrack or
   second shell is ever created. */
(function () {
  "use strict";
  if (window.self === window.top) return;

  document.documentElement.setAttribute("data-nested-shell", "");
  var name = window.location.pathname.split("/").pop() || "index.html";
  var hash = window.location.hash || "";

  try {
    if (window.parent.genesisShell && window.parent.genesisShell.adopt(name, hash)) return;
  } catch (error) {
    /* cross-origin parent: fall through */
  }
  window.location.replace(name.replace(/\.html$/, ".view.html") + hash);
}());

(function () {
  "use strict";

  var routes = {
    "index.html": "index.view.html",
    "memory.html": "memory.view.html",
    "modes.html": "modes.view.html",
    "genesis.html": "genesis.view.html",
    "honesty.html": "honesty.view.html"
  };

  var shell = document.getElementById("siteShell");
  var frame = document.getElementById("siteView");
  var status = document.getElementById("routeStatus");
  var currentRoute = document.body.getAttribute("data-route") || "index.html";

  if (!shell || !frame) return;

  function routeFromUrl(value) {
    var url;
    try {
      url = new URL(value, window.location.href);
    } catch (error) {
      return null;
    }

    if (url.origin !== window.location.origin) return null;

    var parts = url.pathname.split("/");
    var name = parts[parts.length - 1] || "index.html";
    if (!routes[name]) return null;

    return { name: name, hash: url.hash };
  }

  function updateHistory(route, hash, replace) {
    var destination = route + (hash || "");
    var state = { genesisRoute: route };
    if (replace) {
      window.history.replaceState(state, "", destination);
    } else {
      window.history.pushState(state, "", destination);
    }
  }

  function navigate(route, hash, addHistory) {
    if (!routes[route]) return;

    if (route === currentRoute) {
      if (!hash && addHistory) return;
      if (addHistory) updateHistory(route, hash, false);
      try {
        if (hash) {
          var id = decodeURIComponent(hash.slice(1));
          var anchor = frame.contentDocument.getElementById(id);
          if (anchor) anchor.scrollIntoView();
        } else {
          frame.contentWindow.scrollTo(0, 0);
        }
      } catch (error) {
        frame.contentWindow.location.replace(routes[route] + (hash || ""));
      }
      return;
    }

    currentRoute = route;
    shell.classList.add("is-loading");
    if (status) status.textContent = "Loading " + route.replace(".html", "");
    if (addHistory) updateHistory(route, hash, false);
    try {
      frame.contentWindow.location.replace(routes[route] + (hash || ""));
    } catch (error) {
      frame.src = routes[route] + (hash || "");
    }
  }

  function handleViewClick(event) {
    if (event.defaultPrevented || event.button !== 0) return;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

    var target = event.target;
    if (!target || typeof target.closest !== "function") return;

    var link = target.closest("a[href]");
    if (!link || link.hasAttribute("download")) return;
    if (link.target && link.target.toLowerCase() !== "_self") return;

    var rawHref = link.getAttribute("href");
    if (!rawHref || rawHref.charAt(0) === "#") return;

    var route = routeFromUrl(link.href);
    if (!route) return;

    event.preventDefault();
    navigate(route.name, route.hash, true);
  }

  function viewReady() {
    var viewDocument;
    try {
      viewDocument = frame.contentDocument;
    } catch (error) {
      return;
    }

    if (!viewDocument) return;
    viewDocument.removeEventListener("click", handleViewClick);
    viewDocument.addEventListener("click", handleViewClick);

    if (viewDocument.title) {
      document.title = viewDocument.title;
      frame.title = viewDocument.title;
    }

    shell.classList.remove("is-loading");
    if (status) status.textContent = "";
  }

  frame.addEventListener("load", viewReady);

  window.addEventListener("popstate", function () {
    var route = routeFromUrl(window.location.href);
    if (!route) route = { name: "index.html", hash: "" };
    navigate(route.name, route.hash, false);
  });

  var initial = routeFromUrl(window.location.href) || { name: currentRoute, hash: "" };
  currentRoute = initial.name;
  updateHistory(initial.name, initial.hash, true);

  if (frame.contentDocument && frame.contentDocument.readyState === "complete") {
    viewReady();
  }
}());

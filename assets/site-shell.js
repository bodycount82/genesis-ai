(function () {
  "use strict";

  var routes = {
    "index.html": "index.view.html",
    "memory.html": "memory.view.html",
    "modes.html": "modes.view.html",
    "genesis.html": "genesis.view.html",
    "honesty.html": "honesty.view.html",
    "tutorials.html": "tutorials/index.view.html"
  };

  var shell = document.getElementById("siteShell");
  var frame = document.getElementById("siteView");
  var status = document.getElementById("routeStatus");
  var currentRoute = document.body.getAttribute("data-route") || "index.html";

  if (!shell || !frame) return;
  // Only the top-level page is the shell; a nested copy is handed back to it
  // by shell-guard.js and must not start its own router.
  if (window.self !== window.top) return;

  var siteRoot = new URL(".", document.baseURI);
  var base = document.querySelector("base");
  if (base) base.href = siteRoot.href;
  function viewUrl(route, hash) {
    return new URL(routes[route] + (hash || ""), siteRoot).href;
  }

  function routeFromUrl(value) {
    var url;
    try {
      url = new URL(value, window.location.href);
    } catch (error) {
      return null;
    }

    if (url.origin !== window.location.origin) return null;

    var relative = url.pathname.slice(siteRoot.pathname.length);
    if (url.pathname.indexOf(siteRoot.pathname) !== 0) return null;
    var name = relative === "tutorials/" || relative === "tutorials/index.html" ? "tutorials.html" : relative || "index.html";
    if (!routes[name]) return null;

    return { name: name, hash: url.hash };
  }

  function updateHistory(route, hash, replace) {
    var path = route === "tutorials.html" ? "tutorials/" : route;
    var destination = new URL(path + (hash || ""), siteRoot).href;
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
      if (!hash && addHistory && route !== "tutorials.html") return;
      if (addHistory) updateHistory(route, hash, false);
      try {
        if (route === "tutorials.html") {
          if (frame.contentWindow.location.hash !== (hash || "")) {
            frame.contentWindow.location.replace(viewUrl(route, hash));
          }
        } else if (hash) {
          var id = decodeURIComponent(hash.slice(1));
          var anchor = frame.contentDocument.getElementById(id);
          if (anchor) anchor.scrollIntoView();
        } else {
          frame.contentWindow.scrollTo(0, 0);
        }
      } catch (error) {
        frame.contentWindow.location.replace(viewUrl(route, hash));
      }
      return;
    }

    currentRoute = route;
    shell.classList.add("is-loading");
    watchFrame();
    if (status) status.textContent = "Loading " + route.replace(".html", "");
    if (addHistory) updateHistory(route, hash, false);
    try {
      frame.contentWindow.location.replace(viewUrl(route, hash));
    } catch (error) {
      frame.src = viewUrl(route, hash);
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
    if (!rawHref) return;
    if (rawHref.charAt(0) === "#") {
      if (currentRoute !== "tutorials.html") return;
      event.preventDefault();
      navigate(currentRoute, rawHref === "#" ? "" : rawHref, true);
      return;
    }

    var route = routeFromUrl(link.href);
    if (!route) return;

    event.preventDefault();
    navigate(route.name, route.hash, true);
  }

  // Wire link handling into a view document as soon as it exists, not at its
  // load event: the 3D views take seconds to load, and a link clicked in that
  // window would otherwise load a whole second shell (and soundtrack) inside
  // the frame.
  var wiredDocument = null;
  var watchUntil = 0;

  function wireView(viewDocument) {
    if (!viewDocument || viewDocument === wiredDocument) return;
    if (viewDocument.location.href === "about:blank") return;
    viewDocument.addEventListener("click", handleViewClick);
    wiredDocument = viewDocument;
    viewDocument.defaultView.addEventListener("hashchange", function () {
      if (viewDocument !== wiredDocument || currentRoute !== "tutorials.html") return;
      var hash = viewDocument.location.hash;
      if (window.location.hash !== hash) updateHistory(currentRoute, hash, true);
    });
  }

  function watchFrame() {
    var alreadyWatching = watchUntil > Date.now();
    watchUntil = Date.now() + 30000;
    if (alreadyWatching) return;
    (function tick() {
      try {
        wireView(frame.contentDocument);
      } catch (error) {
        return;
      }
      if (Date.now() < watchUntil) window.requestAnimationFrame(tick);
    }());
  }

  function viewReady() {
    var viewDocument;
    try {
      viewDocument = frame.contentDocument;
    } catch (error) {
      return;
    }

    if (!viewDocument) return;
    wireView(viewDocument);

    if (viewDocument.title) {
      document.title = viewDocument.title;
      frame.title = viewDocument.title;
    }

    shell.classList.remove("is-loading");
    if (status) status.textContent = "";
  }

  frame.addEventListener("load", viewReady);

  // Called by shell-guard.js when a shell page loaded inside the frame anyway.
  window.genesisShell = {
    navigateTutorial: function (hash) {
      navigate("tutorials.html", hash, true);
    },
    adopt: function (route, hash) {
      if (!routes[route]) return false;
      if (route !== currentRoute) updateHistory(route, hash, false);
      currentRoute = route;
      shell.classList.add("is-loading");
      watchFrame();
      frame.contentWindow.location.replace(viewUrl(route, hash));
      return true;
    }
  };

  window.addEventListener("popstate", function () {
    var route = routeFromUrl(window.location.href);
    if (!route) route = { name: "index.html", hash: "" };
    navigate(route.name, route.hash, false);
  });

  var initial = routeFromUrl(window.location.href) || { name: currentRoute, hash: "" };
  currentRoute = initial.name;
  updateHistory(initial.name, initial.hash, true);

  // A direct public lesson link must reach the guide on first load too.
  if (initial.hash) frame.src = viewUrl(initial.name, initial.hash);
  watchFrame();
  if (frame.contentDocument && frame.contentDocument.readyState === "complete") {
    viewReady();
  }
}());

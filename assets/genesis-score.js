(function () {
  "use strict";

  var toggle = document.getElementById("soundToggle");
  var player = document.getElementById("genesisSong");
  var status = document.getElementById("soundChapter");

  if (!toggle || !player || !status) return;

  // A shell that ended up inside the site frame must stay silent; the top
  // shell owns the one and only soundtrack (see shell-guard.js).
  if (window.self !== window.top) {
    player.pause();
    player.removeAttribute("src");
    return;
  }

  player.volume = 0.72;

  function showPlaying() {
    toggle.classList.add("is-on");
    toggle.setAttribute("aria-pressed", "true");
    toggle.setAttribute("aria-label", "Pause Life Is Life by Laibach");
    status.textContent = "Laibach · playing";
  }

  function showPaused() {
    toggle.classList.remove("is-on");
    toggle.setAttribute("aria-pressed", "false");
    toggle.setAttribute("aria-label", "Play Life Is Life by Laibach");
    status.textContent = "Laibach · play";
  }

  function showWaiting() {
    toggle.classList.add("is-loading");
    status.textContent = "Laibach · loading";
  }

  function clearWaiting() {
    toggle.classList.remove("is-loading");
  }

  function play() {
    if (player.ended) player.currentTime = 0;
    var attempt = player.play();
    if (attempt && typeof attempt.catch === "function") {
      attempt.catch(function () {
        showPaused();
      });
    }
  }

  toggle.addEventListener("click", function () {
    if (player.paused) {
      play();
    } else {
      player.pause();
    }
  });

  // One soundtrack per browser: when another Genesis tab starts the song,
  // this one pauses instead of layering a second copy on top.
  var channel = null;
  try {
    channel = new BroadcastChannel("genesis-soundtrack");
    channel.onmessage = function (event) {
      if (event.data === "playing" && !player.paused) player.pause();
    };
  } catch (error) {
    channel = null;
  }

  player.addEventListener("play", function () {
    if (channel) channel.postMessage("playing");
    showPlaying();
  });
  player.addEventListener("playing", function () {
    clearWaiting();
    showPlaying();
  });
  player.addEventListener("pause", function () {
    clearWaiting();
    if (!player.ended) showPaused();
  });
  player.addEventListener("waiting", showWaiting);
  player.addEventListener("canplay", clearWaiting);
  player.addEventListener("ended", function () {
    clearWaiting();
    toggle.classList.remove("is-on");
    toggle.setAttribute("aria-pressed", "false");
    toggle.setAttribute("aria-label", "Replay Life Is Life by Laibach");
    status.textContent = "Laibach · replay";
  });
  player.addEventListener("error", function () {
    clearWaiting();
    toggle.classList.remove("is-on");
    toggle.disabled = true;
    status.textContent = "Audio unavailable";
  });

  play();
}());

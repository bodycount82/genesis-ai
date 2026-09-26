/* "See it" rig: slides, pointer tilt, scroll assembly, lightbox. */
(function () {
  "use strict";
  var rig = document.getElementById("showcaseRig");
  if (!rig) return;

  var slides = [
    {
      tab: "Modern desktop",
      desk: "assets/showcase/desktop-chat.webp", phone: "assets/showcase/android-chat.webp",
      lede: "One request, four tools, one answer. Genesis searches, plans the drive, checks the weather and books the calendar — and shows every step it took.",
      hud: [["Every tool call visible", "web · maps · weather · calendar"], ["Hands off to you", "it never pays for you"], ["Your model", "local · offline capable"]]
    },
    {
      tab: "Voice orb",
      desk: "assets/showcase/desktop-orb-transcript.webp", phone: "assets/showcase/android-calendar.webp",
      lede: "Talk to it. The orb speaks while it works, listens while it speaks — interrupt it mid-sentence and it stops, hears you, and carries on from what you actually heard.",
      hud: [["Barge-in", "talk over it any time"], ["Streamed speech", "starts before it finishes"], ["Transcript on demand", "slide it open"]]
    },
    {
      tab: "Android companion",
      desk: "assets/showcase/desktop-orb.webp", phone: "assets/showcase/android-drawer.webp",
      lede: "Your Genesis in your pocket. Pair once by QR, then chat, check projects, answer what needs you and see its memories — connected securely to the Genesis on your computer.",
      hud: [["Paired by QR", "no account, no cloud relay"], ["Needs-you alerts", "phone and Telegram"], ["Memory in your pocket", "memories · journal · intentions"]]
    }
  ];

  var desk = rig.querySelector(".device.desk");
  var phone = rig.querySelector(".device.phone");
  var huds = rig.querySelectorAll(".hud");
  var tabs = document.querySelectorAll(".showcase-tab");
  var lede = document.getElementById("showcaseLede");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var current = -1, timer = null, paused = false, SLIDE_MS = 7000;

  function screenImages(device, key) {
    var screen = device.querySelector(".device-screen");
    return slides.map(function (slide, index) {
      var img = new Image();
      img.alt = "";
      img.decoding = "async";
      if (index > 0) img.loading = "lazy";
      img.src = slide[key];
      screen.appendChild(img);
      return img;
    });
  }
  var deskImgs = screenImages(desk, "desk");
  var phoneImgs = screenImages(phone, "phone");

  function boot(device, imgs, index, previous) {
    imgs.forEach(function (img, i) {
      img.classList.remove("on", "off");
      if (i === previous && previous !== index) img.classList.add("off");
    });
    void imgs[index].offsetWidth; // restart the wipe animation
    imgs[index].classList.add("on");
    device.classList.remove("booting"); void device.offsetWidth; device.classList.add("booting");
  }

  function show(index, fromUser) {
    if (index === current) return;
    var previous = current;
    current = index;
    var slide = slides[index];
    rig.setAttribute("data-slide", String(index));
    boot(desk, deskImgs, index, previous);
    window.setTimeout(function () { boot(phone, phoneImgs, index, previous); }, reduce ? 0 : 180);
    desk.setAttribute("aria-label", "Enlarge: " + slide.tab + " — desktop");
    phone.setAttribute("aria-label", "Enlarge: " + slide.tab + " — Android");

    tabs.forEach(function (tab, i) {
      tab.setAttribute("aria-selected", i === index ? "true" : "false");
      tab.tabIndex = i === index ? 0 : -1;
    });
    lede.classList.add("swap");
    window.setTimeout(function () { lede.textContent = slide.lede; lede.classList.remove("swap"); }, reduce ? 0 : 260);

    huds.forEach(function (hud, i) { hud.classList.add("hide"); window.setTimeout(function () {
      hud.innerHTML = "<span>" + slide.hud[i][0] + "<small>" + slide.hud[i][1] + "</small></span>";
      hud.classList.remove("hide");
    }, reduce ? 0 : 520 + i * 140); });

    if (fromUser) paused = true;
    restartTimer();
  }

  // Tab progress ticks drive the autoplay, so the bar and the change always agree.
  var elapsed = 0, lastFrame = 0;
  function restartTimer() {
    elapsed = 0;
    tabs.forEach(function (tab) { var t = tab.querySelector(".tick"); if (t) t.style.transform = "scaleX(0)"; });
  }

  tabs.forEach(function (tab, i) {
    tab.addEventListener("click", function () { show(i, true); });
    tab.addEventListener("keydown", function (event) {
      var step = event.key === "ArrowRight" ? 1 : event.key === "ArrowLeft" ? -1 : 0;
      if (!step) return;
      event.preventDefault();
      var next = (current + step + slides.length) % slides.length;
      show(next, true); tabs[next].focus();
    });
  });

  /* ---------- lightbox ---------- */
  var view = document.getElementById("shotView");
  var viewImg = view.querySelector("img");
  var viewCap = view.querySelector("figcaption");
  var opener = null;
  function openView(device, src, caption) {
    opener = device;
    viewImg.src = src; viewImg.alt = caption; viewCap.textContent = caption + " · click anywhere to close";
    view.classList.add("open"); view.setAttribute("aria-hidden", "false");
    document.body.classList.add("shot-open"); paused = true;
    view.focus();
  }
  function closeView() {
    if (!view.classList.contains("open")) return;
    view.classList.remove("open"); view.setAttribute("aria-hidden", "true");
    document.body.classList.remove("shot-open");
    if (opener) opener.focus();
  }
  desk.addEventListener("click", function () { openView(desk, slides[current].desk, slides[current].tab + " · Windows"); });
  phone.addEventListener("click", function () { openView(phone, slides[current].phone, slides[current].tab + " · Android"); });
  view.addEventListener("click", closeView);
  document.addEventListener("keydown", function (event) { if (event.key === "Escape") closeView(); });

  /* ---------- motion: pointer tilt + scroll assembly + autoplay ---------- */
  var target = { x: 0, y: 0 }, tilt = { x: 0, y: 0 }, enter = reduce ? 1 : 0, visible = false;
  window.addEventListener("pointermove", function (event) {
    var r = rig.getBoundingClientRect();
    target.x = Math.max(-1, Math.min(1, (event.clientX - (r.left + r.width / 2)) / (r.width * 0.7)));
    target.y = Math.max(-1, Math.min(1, (event.clientY - (r.top + r.height / 2)) / (r.height * 0.9)));
  }, { passive: true });
  rig.addEventListener("pointerenter", function () { paused = true; });
  rig.addEventListener("pointerleave", function () { paused = false; restartTimer(); });

  function assembly() {
    var r = rig.getBoundingClientRect(), vh = window.innerHeight;
    // 0 when the rig's top is at the bottom of the viewport, 1 once it is well in view.
    var t = (vh - r.top) / (vh * 0.6);
    return Math.max(0, Math.min(1, t));
  }

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) { visible = entries[0].isIntersecting; }, { rootMargin: "120px" }).observe(rig);
  } else visible = true;

  function frame(now) {
    window.requestAnimationFrame(frame);
    if (!visible) { lastFrame = 0; return; }
    if (!reduce) {
      var e = assembly(); e = e * e * (3 - 2 * e);
      enter += (e - enter) * 0.12;
      tilt.x += (target.x - tilt.x) * 0.06;
      tilt.y += (target.y - tilt.y) * 0.06;
      rig.style.setProperty("--enter", enter.toFixed(4));
      rig.style.setProperty("--tx", tilt.x.toFixed(4));
      rig.style.setProperty("--ty", tilt.y.toFixed(4));
    }
    var dt = lastFrame ? Math.min(100, now - lastFrame) : 0;
    lastFrame = now;
    if (paused || reduce || enter < 0.9 || document.hidden) return;
    elapsed += dt;
    var tab = tabs[current], tick = tab && tab.querySelector(".tick");
    var progress = Math.min(1, elapsed / SLIDE_MS);
    if (tick) tick.style.transform = "scaleX(" + progress.toFixed(4) + ")";
    if (progress >= 1) show((current + 1) % slides.length, false);
  }
  if (reduce) rig.style.setProperty("--enter", "1");
  show(0, false);
  window.requestAnimationFrame(frame);
}());

(function () {
  "use strict";

  function initialize() {
    if (!window.HTMLDialogElement || document.querySelector(".sdk-image-viewer")) {
      return;
    }
    var chinese = document.documentElement.lang.toLowerCase().indexOf("zh") === 0;
    var labels = chinese
      ? { title: "\u56fe\u7247\u9884\u89c8", open: "\u653e\u5927\u56fe\u7247", out: "\u7f29\u5c0f", inside: "\u653e\u5927", reset: "\u9002\u5e94\u7a97\u53e3", close: "\u5173\u95ed", hint: "\u6eda\u8f6e\u6216\u53cc\u6307\u7f29\u653e \u00b7 \u62d6\u52a8\u67e5\u770b \u00b7 Esc \u5173\u95ed" }
      : { title: "Image preview", open: "Enlarge image", out: "Zoom out", inside: "Zoom in", reset: "Fit to window", close: "Close", hint: "Scroll or pinch to zoom \u00b7 Drag to pan \u00b7 Esc to close" };
    var dialog = document.createElement("dialog");
    dialog.className = "sdk-image-viewer";
    dialog.setAttribute("aria-label", labels.title);
    var toolbar = document.createElement("div");
    toolbar.className = "sdk-image-viewer__toolbar";
    var status = document.createElement("output");
    status.setAttribute("aria-live", "polite");
    var stage = document.createElement("div");
    stage.className = "sdk-image-viewer__stage";
    stage.tabIndex = 0;
    stage.setAttribute("aria-label", labels.hint);
    var canvas = document.createElement("div");
    canvas.className = "sdk-image-viewer__canvas";
    var preview = document.createElement("img");
    preview.draggable = false;
    canvas.appendChild(preview);
    stage.appendChild(canvas);
    var hint = document.createElement("p");
    hint.className = "sdk-image-viewer__hint";
    hint.textContent = labels.hint;
    var zoom = 1;
    var translateX = 0;
    var translateY = 0;
    var trigger = null;
    var previousOverflow = "";
    var pointers = new Map();
    var gesture = null;
    var moved = false;
    var dimensions = null;
    var minimumZoom = 0.8;
    var maximumZoom = 4;

    function render() {
      if (!dialog.open) {
        return;
      }
      if (dimensions) {
        var limitX = Math.max(0, (dimensions.imageWidth * zoom - dimensions.width) / 2);
        var limitY = Math.max(0, (dimensions.imageHeight * zoom - dimensions.height) / 2);
        translateX = Math.max(-limitX, Math.min(limitX, translateX));
        translateY = Math.max(-limitY, Math.min(limitY, translateY));
      }
      preview.style.transform = "translate(" + translateX + "px, " + translateY + "px) scale(" + zoom + ")";
      status.textContent = Math.round(zoom * 100) + "%";
      zoomOut.disabled = zoom <= minimumZoom;
      zoomIn.disabled = zoom >= maximumZoom;
    }

    function fitImage() {
      if (!dialog.open || !preview.naturalWidth) {
        return;
      }
      var bounds = stage.getBoundingClientRect();
      var stageWidth = stage.clientWidth;
      var stageHeight = stage.clientHeight;
      var fit = Math.min(1, stageWidth / preview.naturalWidth, stageHeight / preview.naturalHeight);
      dimensions = {
        width: stageWidth,
        height: stageHeight,
        centerX: bounds.left + bounds.width / 2,
        centerY: bounds.top + bounds.height / 2,
        imageWidth: preview.naturalWidth * fit,
        imageHeight: preview.naturalHeight * fit
      };
      preview.style.width = dimensions.imageWidth + "px";
      preview.style.height = dimensions.imageHeight + "px";
      render();
    }

    function changeZoom(value) {
      var nextZoom = Math.max(minimumZoom, Math.min(maximumZoom, value));
      translateX *= nextZoom / zoom;
      translateY *= nextZoom / zoom;
      zoom = nextZoom;
      render();
    }

    function reset() {
      zoom = 1;
      translateX = 0;
      translateY = 0;
      render();
    }

    function addButton(label, paths, action) {
      var button = document.createElement("button");
      button.type = "button";
      button.setAttribute("aria-label", label);
      button.title = label;
      button.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + paths + '</svg>';
      button.addEventListener("click", action);
      toolbar.appendChild(button);
      return button;
    }

    var magnifier = '<circle cx="10.5" cy="10.5" r="7.5"/><path d="m16 16 5 5M7 10.5h7"/>';
    var zoomOut = addButton(labels.out, magnifier, function () { changeZoom(zoom - 0.4); });
    toolbar.appendChild(status);
    var zoomIn = addButton(labels.inside, magnifier + '<path d="M10.5 7v7"/>', function () { changeZoom(zoom + 0.4); });
    addButton(labels.reset, '<path d="M3 12a9 9 0 1 0 3-6.7L3 8M3 3v5h5"/>', reset);
    var close = addButton(labels.close, '<path d="m6 6 12 12M18 6 6 18"/>', function () { dialog.close(); });
    close.className = "sdk-image-viewer__close";
    dialog.appendChild(close);
    dialog.appendChild(stage);
    dialog.appendChild(hint);
    dialog.appendChild(toolbar);
    document.body.appendChild(dialog);
    preview.addEventListener("load", fitImage);
    window.addEventListener("resize", fitImage);
    dialog.addEventListener("close", function () {
      if (dialog.open) {
        return;
      }
      document.documentElement.style.overflow = previousOverflow;
      pointers.clear();
      gesture = null;
      stage.classList.remove("is-interacting");
      if (trigger) {
        trigger.focus({ preventScroll: true });
      }
    });
    dialog.addEventListener("click", function (event) {
      if (!moved && (event.target === dialog || event.target === stage || event.target === canvas)) {
        dialog.close();
      }
      moved = false;
    });
    stage.addEventListener("wheel", function (event) {
      event.preventDefault();
      if (event.deltaY) {
        changeZoom(zoom + (event.deltaY < 0 ? 0.1 : -0.1));
      }
    }, { passive: false });
    preview.addEventListener("dblclick", function () {
      if (zoom > 1) {
        reset();
      } else {
        changeZoom(2);
      }
    });
    dialog.addEventListener("keydown", function (event) {
      if (event.key === "Tab") {
        var controls = Array.from(dialog.querySelectorAll("button:not(:disabled), [tabindex='0']"));
        var first = controls[0];
        var last = controls[controls.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
        return;
      }
      if (event.key === "+" || event.key === "=") {
        event.preventDefault();
        changeZoom(zoom + 0.4);
      } else if (event.key === "-") {
        event.preventDefault();
        changeZoom(zoom - 0.4);
      }
    });

    function startGesture() {
      var points = Array.from(pointers.values());
      if (!points.length) {
        gesture = null;
        stage.classList.remove("is-interacting");
        return;
      }
      stage.classList.add("is-interacting");
      var first = points[0];
      var second = points[1] || first;
      gesture = {
        x: (first.x + second.x) / 2,
        y: (first.y + second.y) / 2,
        distance: Math.hypot(first.x - second.x, first.y - second.y),
        zoom: zoom,
        translateX: translateX,
        translateY: translateY
      };
    }

    stage.addEventListener("pointerdown", function (event) {
      if (event.button !== 0) {
        return;
      }
      if (!pointers.size) {
        moved = false;
        if (event.target !== preview) {
          return;
        }
      }
      event.preventDefault();
      pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
      stage.setPointerCapture(event.pointerId);
      startGesture();
    });
    stage.addEventListener("pointermove", function (event) {
      if (!pointers.has(event.pointerId) || !gesture || !dimensions) {
        return;
      }
      pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
      var points = Array.from(pointers.values());
      var first = points[0];
      var second = points[1] || first;
      var centerX = (first.x + second.x) / 2;
      var centerY = (first.y + second.y) / 2;
      var deltaX = centerX - gesture.x;
      var deltaY = centerY - gesture.y;
      if (Math.abs(deltaX) + Math.abs(deltaY) > 3) {
        moved = true;
      }
      if (points.length > 1 && gesture.distance > 0) {
        moved = true;
        zoom = Math.max(minimumZoom, Math.min(maximumZoom, gesture.zoom * Math.hypot(first.x - second.x, first.y - second.y) / gesture.distance));
        var ratio = zoom / gesture.zoom;
        var anchorX = gesture.x - dimensions.centerX;
        var anchorY = gesture.y - dimensions.centerY;
        translateX = anchorX + (gesture.translateX - anchorX) * ratio + deltaX;
        translateY = anchorY + (gesture.translateY - anchorY) * ratio + deltaY;
      } else if (zoom > 1) {
        translateX = gesture.translateX + deltaX;
        translateY = gesture.translateY + deltaY;
      }
      render();
    });
    function finishPointer(event) {
      if (pointers.delete(event.pointerId)) {
        startGesture();
      }
    }
    stage.addEventListener("pointerup", finishPointer);
    stage.addEventListener("pointercancel", finishPointer);
    stage.addEventListener("lostpointercapture", finishPointer);
    document.querySelectorAll(".sdk-reading-main .rst-content img").forEach(function (image) {
      var anchor = image.closest("a");
      if (image.closest("button, .headerlink")) {
        return;
      }
      if (anchor && new URL(anchor.href).pathname !== new URL(image.src).pathname) {
        return;
      }
      var button = anchor || document.createElement("button");
      var media = image.closest("picture") || image;
      var paragraph = media.closest("p");
      var hasSurroundingText = paragraph && paragraph.textContent.trim();
      if (!anchor) {
        button.type = "button";
        media.parentNode.insertBefore(button, media);
        button.appendChild(media);
      }
      button.classList.add("sdk-image-trigger");
      function updateImageLayout() {
        var inline = Boolean(hasSurroundingText && image.naturalWidth > 0 && image.naturalWidth <= 64 && image.naturalHeight <= 64);
        button.classList.toggle("sdk-image-trigger--inline", inline);
        image.classList.toggle("sdk-inline-image", inline);
      }
      image.addEventListener("load", updateImageLayout);
      updateImageLayout();
      button.setAttribute("aria-label", labels.open + (image.alt ? ": " + image.alt : ""));
      button.setAttribute("aria-haspopup", "dialog");
      button.addEventListener("click", function (event) {
        event.preventDefault();
        trigger = button;
        dimensions = null;
        moved = false;
        preview.alt = image.alt;
        preview.removeAttribute("style");
        preview.src = image.currentSrc || image.src;
        previousOverflow = document.documentElement.style.overflow;
        document.documentElement.style.overflow = "hidden";
        dialog.showModal();
        reset();
        fitImage();
        close.focus();
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize);
  } else {
    initialize();
  }
})();

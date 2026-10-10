(function () {
  "use strict";

  function headingId(heading) {
    var ownId = heading.getAttribute("id");
    if (ownId) {
      return ownId;
    }

    var headerLink = heading.querySelector("a.headerlink[href], a[href^='#']");
    if (headerLink) {
      var href = headerLink.getAttribute("href") || "";
      var hashIndex = href.indexOf("#");
      if (hashIndex >= 0 && hashIndex < href.length - 1) {
        try {
          return decodeURIComponent(href.slice(hashIndex + 1));
        } catch (error) {
          return href.slice(hashIndex + 1);
        }
      }
    }

    // Sphinx HTML5 places section IDs on the wrapper around h2/h3.
    var section = heading.closest("section[id], [role='region'][id]");
    return section ? section.getAttribute("id") : null;
  }

  function resolveHeading(id) {
    var target = document.getElementById(id);
    if (!target) {
      return null;
    }
    if (target.tagName === "H2" || target.tagName === "H3") {
      return target;
    }

    // Sphinx HTML5 normally puts the anchor on a section wrapper and the
    // visible heading immediately inside it. Support direct heading anchors
    // as well so this stays compatible with other builders/themes.
    return target.querySelector("h2, h3");
  }

  function headingText(heading) {
    var copy = heading.cloneNode(true);
    copy.querySelectorAll("a.headerlink, a[href^='#']").forEach(function (link) {
      link.remove();
    });
    return copy.textContent.replace(/\s+/g, " ").trim();
  }

  function makeLink(entry) {
    var link = document.createElement("a");
    link.className = entry.level === "H3"
      ? "sdk-page-outline__link sdk-page-outline__link--h3"
      : "sdk-page-outline__link sdk-page-outline__link--h2";
    link.href = "#" + encodeURIComponent(entry.id);
    link.dataset.outlineTarget = entry.id;
    // Assigning textContent explicitly prevents inline code/highlight markup
    // from leaking into the right-hand outline.
    link.textContent = entry.text;
    link.textContent = link.textContent;
    entry.link = link;
    entry.heading.dataset.outlineId = entry.id;
    return link;
  }

  function appendEntry(list, entry) {
    var item = document.createElement("li");
    item.appendChild(makeLink(entry));
    list.appendChild(item);
    entry.item = item;
    return item;
  }

  function buildOutline(outline) {
    var list = outline.querySelector(".sdk-page-outline__list");
    if (!list) {
      return [];
    }
    list.textContent = "";

    var entries = [];
    var currentH2 = null;
    var seenIds = new Set();
    document.querySelectorAll(".rst-content h2, .rst-content h3").forEach(function (heading) {
      var id = headingId(heading);
      var text = headingText(heading);
      if (!id || !text || seenIds.has(id)) {
        return;
      }
      seenIds.add(id);
      var entry = { id: id, text: text, heading: heading, level: heading.tagName };
      entries.push(entry);

      if (entry.level === "H2") {
        currentH2 = appendEntry(list, entry);
        var children = document.createElement("ul");
        currentH2.appendChild(children);
        entry.children = children;
      } else if (currentH2 && currentH2.children.length > 1) {
        appendEntry(currentH2.children[1], entry);
      } else {
        appendEntry(list, entry);
      }
    });
    return entries;
  }

  function initialize() {
    var outline = document.querySelector(".sdk-page-outline");
    if (!outline) {
      return;
    }

    var entries = buildOutline(outline);
    var links = entries.map(function (entry) { return entry.link; });
    var headings = entries.map(function (entry) { return entry.heading; });
    if (!headings.length) {
      outline.classList.add("is-empty");
      var emptyLayout = outline.closest(".sdk-reading-layout");
      if (emptyLayout) {
        emptyLayout.classList.add("sdk-reading-layout--no-outline");
      }
      return;
    }

    function setActive(id) {
      links.forEach(function (link) {
        var active = link.dataset.outlineTarget === id;
        link.classList.toggle("is-active", active);
        if (active) {
          link.setAttribute("aria-current", "location");
        } else {
          link.removeAttribute("aria-current");
        }
      });
    }

    entries.forEach(function (entry) {
      entry.link.addEventListener("click", function (event) {
        var target = resolveHeading(entry.id) || entry.heading;
        if (!target) {
          return;
        }
        event.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
        if (window.history && window.history.replaceState) {
          window.history.replaceState(null, "", "#" + encodeURIComponent(entry.id));
        } else {
          window.location.hash = entry.id;
        }
        setActive(entry.id);
      });
    });

    function selectFromHash() {
      var hash = window.location.hash;
      if (!hash) {
        return false;
      }
      var id;
      try {
        id = decodeURIComponent(hash.slice(1));
      } catch (error) {
        id = hash.slice(1);
      }
      if (links.some(function (link) { return link.dataset.outlineTarget === id; })) {
        setActive(id);
        return true;
      }
      return false;
    }

    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function (observed) {
        var visible = observed.filter(function (entry) {
          return entry.isIntersecting;
        }).sort(function (left, right) {
          return left.boundingClientRect.top - right.boundingClientRect.top;
        });
        if (visible.length) {
          setActive(visible[0].target.dataset.outlineId);
        }
      }, {
        rootMargin: "-12% 0px -70% 0px",
        threshold: [0, 1],
      });
      headings.forEach(function (heading) { observer.observe(heading); });
    } else {
      var ticking = false;
      var updateFromScroll = function () {
        ticking = false;
        var current = headings[0];
        headings.forEach(function (heading) {
          if (heading.getBoundingClientRect().top <= window.innerHeight * 0.25) {
            current = heading;
          }
        });
        setActive(current.dataset.outlineId);
      };
      window.addEventListener("scroll", function () {
        if (!ticking) {
          ticking = true;
          window.requestAnimationFrame(updateFromScroll);
        }
      }, { passive: true });
      updateFromScroll();
    }

    if (!selectFromHash()) {
      setActive(headings[0].dataset.outlineId);
    }
    window.addEventListener("popstate", selectFromHash);
    window.addEventListener("hashchange", selectFromHash);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
})();

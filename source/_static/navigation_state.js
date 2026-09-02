(function () {
  "use strict";

  var storagePrefix = "sdk-docs-navigation:";
  var anchorNavigationPending = false;

  function storageKey() {
    var language = document.documentElement.lang || "default";
    return storagePrefix + window.location.origin + ":" + language;
  }

  function getGlobalMenu() {
    var menu = document.querySelector(".wy-menu-vertical");
    return menu ? menu.querySelector(":scope > ul") : null;
  }

  function collapseTree(item) {
    item.classList.remove("current");
    item.setAttribute("aria-expanded", "false");
    item.querySelectorAll("li").forEach(function (nested) {
      nested.classList.remove("current");
      if (nested.querySelector(":scope > ul")) {
        nested.setAttribute("aria-expanded", "false");
      } else {
        nested.removeAttribute("aria-expanded");
      }
    });
  }

  function isExpanded(item) {
    return item.classList.contains("current") ||
      item.getAttribute("aria-expanded") === "true";
  }

  function containsCurrentArticle(item) {
    // querySelector searches descendants, so an item restored from storage
    // does not win merely because it carries its own `current` class.
    return !!item.querySelector("a.current, li.current");
  }

  function normalizeLevel(list, preferred) {
    if (!list) {
      return;
    }
    var branches = Array.from(list.children).filter(function (item) {
      return item.tagName === "LI" && item.querySelector(":scope > ul");
    });
    var expanded = branches.filter(isExpanded);
    if (!expanded.length) {
      return;
    }

    // Keep the branch selected by the user when possible. On a restored page,
    // prefer the current article, then a visible branch for deterministic UI.
    var keep = expanded.find(function (item) {
      return preferred && (item === preferred || item.contains(preferred));
    }) || expanded.find(containsCurrentArticle) || expanded.find(function (item) {
      return item.getClientRects().length > 0;
    }) || expanded[0];
    expanded.forEach(function (item) {
      if (item !== keep) {
        collapseTree(item);
      }
    });
    normalizeLevel(keep.querySelector(":scope > ul"), preferred);
  }

  function enforceSingleTopLevelBranch(preferred) {
    var menu = getGlobalMenu();
    if (menu) {
      normalizeLevel(menu, preferred || null);
    }
  }

  function itemKey(item) {
    var link = item.querySelector(":scope > a[href]");
    if (!link) {
      return null;
    }
    try {
      var url = new URL(link.getAttribute("href"), document.baseURI);
      return url.pathname + url.search;
    } catch (error) {
      return link.getAttribute("href");
    }
  }

  function readExpanded() {
    try {
      var value = window.sessionStorage.getItem(storageKey());
      var expanded = value ? JSON.parse(value) : [];
      return Array.isArray(expanded) ? expanded : [];
    } catch (error) {
      return [];
    }
  }

  function writeExpanded() {
    var menu = getGlobalMenu();
    if (!menu) {
      return;
    }
    enforceSingleTopLevelBranch();

    var expanded = [];
    menu.querySelectorAll("li").forEach(function (item) {
      if (!item.querySelector(":scope > ul")) {
        return;
      }
      var isExpanded = item.classList.contains("current") ||
        item.getAttribute("aria-expanded") === "true";
      var key = itemKey(item);
      // RTD can leave a descendant marked current after its parent is
      // collapsed. A layout check prevents saving such hidden descendants.
      var isVisible = item.getClientRects().length > 0;
      if (isExpanded && isVisible && key) {
        expanded.push(key);
      }
    });

    try {
      window.sessionStorage.setItem(storageKey(), JSON.stringify(expanded));
    } catch (error) {
      // Private browsing and file:// pages may deny sessionStorage.
    }
  }

  function restoreExpanded() {
    var menu = getGlobalMenu();
    if (!menu) {
      return;
    }

    var expanded = new Set(readExpanded());
    if (!expanded.size) {
      return;
    }

    menu.querySelectorAll("li").forEach(function (item) {
      if (expanded.has(itemKey(item)) && item.querySelector(":scope > ul")) {
        item.classList.add("current");
        item.setAttribute("aria-expanded", "true");
      }
    });
    enforceSingleTopLevelBranch();
  }

  function isHashLink(link) {
    var href = link.getAttribute("href");
    if (!href) {
      return false;
    }

    // Keep this broad enough for relative same-page links such as
    // ``article.html#section`` while excluding ordinary document links.
    try {
      var url = new URL(href, document.baseURI);
      return url.origin === window.location.origin &&
        url.pathname === window.location.pathname &&
        url.search === window.location.search &&
        !!url.hash;
    } catch (error) {
      return href.charAt(0) === "#" && href.length > 1;
    }
  }

  function restoreAfterHashChange() {
    // RTD registers its hashchange handler before this script initializes and
    // clears `.current` synchronously. Restore once immediately and once on
    // the next task for custom listeners that also adjust the navigation.
    anchorNavigationPending = false;
    restoreExpanded();
    window.setTimeout(restoreExpanded, 0);
  }

  function closestElement(target, selector) {
    return target && typeof target.closest === "function"
      ? target.closest(selector)
      : null;
  }

  function initialize() {
    // Wait for RTD's own reset() so restored classes are not overwritten.
    restoreExpanded();
    writeExpanded();
    document.addEventListener("click", function (event) {
      // Anchor clicks are persisted by the capture listener below. Delaying
      // those writes would let RTD's click handler overwrite the snapshot
      // immediately before a page navigation.
      if (!closestElement(event.target, "a[href]") &&
          closestElement(event.target, ".wy-menu-vertical")) {
        window.setTimeout(writeExpanded, 0);
      }
      var clickedItem = closestElement(event.target, ".wy-menu-vertical li");
      window.setTimeout(function () {
        enforceSingleTopLevelBranch(clickedItem);
      }, 0);
    });
    // Snapshot before RTD receives an anchor click. Its navigation/reset
    // handlers can otherwise discard expanded sibling branches, and a page
    // navigation may happen before a delayed callback gets to run.
    document.addEventListener("click", function (event) {
      var link = closestElement(event.target, "a[href]");
      if (link && (isHashLink(link) ||
          closestElement(link, ".wy-menu-vertical"))) {
        writeExpanded();
        anchorNavigationPending = true;
      }
    }, true);
    window.addEventListener("hashchange", restoreAfterHashChange);
    window.addEventListener("pageshow", function () {
      anchorNavigationPending = false;
      writeExpanded();
    });
    window.addEventListener("pagehide", function () {
      if (!anchorNavigationPending) {
        writeExpanded();
      }
    });
  }

  if (document.readyState === "complete") {
    initialize();
  } else {
    window.addEventListener("load", initialize, { once: true });
  }
})();

(function () {
  var KEY = "theme";
  var root = document.documentElement;

  function stored() {
    try {
      return localStorage.getItem(KEY);
    } catch (e) {
      return null;
    }
  }

  function systemDark() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function resolved() {
    var saved = stored();
    if (saved === "dark" || saved === "light") return saved;
    return systemDark() ? "dark" : "light";
  }

  function apply(theme) {
    if (theme === "dark" || theme === "light") {
      root.setAttribute("data-theme", theme);
    } else {
      root.removeAttribute("data-theme");
    }
    syncButtons();
  }

  function syncButtons() {
    var mode = resolved();
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      var next = mode === "dark" ? "light" : "dark";
      btn.setAttribute("aria-label", "Switch to " + next + " theme");
      btn.setAttribute("aria-pressed", mode === "dark" ? "true" : "false");
      btn.setAttribute("title", "Switch to " + next + " theme");
    });
  }

  function persist(theme) {
    try {
      if (theme === "dark" || theme === "light") localStorage.setItem(KEY, theme);
      else localStorage.removeItem(KEY);
    } catch (e) {}
    apply(theme);
  }

  apply(stored());

  document.addEventListener("DOMContentLoaded", function () {
    syncButtons();
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        persist(resolved() === "dark" ? "light" : "dark");
      });
    });
  });

  var media = window.matchMedia("(prefers-color-scheme: dark)");
  if (media.addEventListener) {
    media.addEventListener("change", function () {
      if (!stored()) apply(null);
    });
  }
})();

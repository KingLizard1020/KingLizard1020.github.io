(function () {
  var ENDPOINT =
    "https://api.github.com/repos/KingLizard1020/KingLizard1020.github.io/commits?per_page=1";
  var MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  function stamp(iso) {
    var d = new Date(iso);
    if (isNaN(d.getTime())) return null;
    return {
      datetime: d.toISOString().slice(0, 10),
      text: MONTHS[d.getUTCMonth()] + " " + d.getUTCDate() + ", " + d.getUTCFullYear(),
    };
  }

  fetch(ENDPOINT, { headers: { Accept: "application/vnd.github+json" } })
    .then(function (res) {
      if (!res.ok) return null;
      return res.json();
    })
    .then(function (data) {
      if (!data || !data[0] || !data[0].commit) return;
      var commit = data[0].commit;
      var iso =
        (commit.committer && commit.committer.date) || (commit.author && commit.author.date);
      var formatted = iso && stamp(iso);
      if (!formatted) return;
      var el = document.getElementById("last-updated");
      if (!el) return;
      el.setAttribute("datetime", formatted.datetime);
      el.textContent = formatted.text;
    })
    .catch(function () {});
})();

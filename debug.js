
    window.sbBreadcrumb = "Head-Start";
    window.onerror = function (msg, url, lineNo, columnNo, error) {
      const d = error ? "\nDetails: " + error.message : "";
      const b = window.sbBreadcrumb ? "\nLast Breadcrumb: " + window.sbBreadcrumb : "";
      alert("⚠️ APP CRASH: " + msg + " (Line " + lineNo + ")" + d + b);
      return false;
    };
    window.onunhandledrejection = function (event) {
      alert("⚠️ PROMISE CRASH: " + (event.reason?.message || "Unknown error"));
    };
    function trace(id) { window.sbBreadcrumb = id; console.log("📍 " + id); }
  
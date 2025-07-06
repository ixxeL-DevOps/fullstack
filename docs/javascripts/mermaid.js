/**
 * Mermaid initialization for MkDocs Material theme
 * 
 * This script initializes Mermaid diagrams with proper configuration
 * for the Material theme and handles theme switching (light/dark mode).
 */

document.addEventListener("DOMContentLoaded", function() {
  // Initialize Mermaid
  mermaid.initialize({
    startOnLoad: true,
    theme: document.body.getAttribute("data-md-color-scheme") === "slate" ? "dark" : "default",
    themeVariables: {
      fontFamily: "var(--md-text-font-family)",
    },
    flowchart: {
      htmlLabels: true,
      curve: "basis"
    },
    sequence: {
      diagramMarginX: 50,
      diagramMarginY: 10,
      boxTextMargin: 5,
      noteMargin: 10,
      messageMargin: 35
    },
    gantt: {
      leftPadding: 75,
      rightPadding: 20
    }
  });

  // Re-initialize Mermaid when theme changes
  var observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (mutation.type === "attributes" && mutation.attributeName === "data-md-color-scheme") {
        var scheme = mutation.target.getAttribute("data-md-color-scheme");
        mermaid.initialize({
          theme: scheme === "slate" ? "dark" : "default"
        });
        
        // Re-render all Mermaid diagrams
        var elements = document.querySelectorAll(".mermaid");
        elements.forEach(function(element) {
          element.removeAttribute("data-processed");
        });
        mermaid.init(undefined, elements);
      }
    });
  });

  observer.observe(document.body, {
    attributes: true,
    attributeFilter: ["data-md-color-scheme"]
  });
});

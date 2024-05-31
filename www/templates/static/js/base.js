document.addEventListener("DOMContentLoaded", function () {
  const overlayBg = document.getElementById("rnOverlay");

  // Function to toggle sidebar
  function toggleSidebar(target) {
    if (target.style.display === "block") {
      target.style.display = "none";
      overlayBg.style.display = "none";
    } else {
      target.style.display = "block";
      overlayBg.style.display = "block";
    }
  }

  // Add event listener to all elements with the class 'toggle-sidebar'
  document.querySelectorAll(".toggle-sidebar").forEach((button) => {
    button.addEventListener("click", function () {
      const target = document.querySelector(button.getAttribute("data-target"));
      toggleSidebar(target);
    });
  });

  // Add event listener to all elements with the class 'close-sidebar'
  document.querySelectorAll(".close-sidebar").forEach((button) => {
    button.addEventListener("click", function () {
      const target = document.querySelector(button.getAttribute("data-target"));
      target.style.display = "none";
      overlayBg.style.display = "none";
    });
  });

  // Add event listener to overlay to close sidebar when clicking outside
  overlayBg.addEventListener("click", function () {
    document.querySelectorAll(".sidebar").forEach((sidebar) => {
      sidebar.style.display = "none";
    });
    overlayBg.style.display = "none";
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".rn-accordion-btn");

  buttons.forEach((button) => {
    button.addEventListener("click", function () {
      const target = document.querySelector(button.getAttribute("data-target"));

      if (target.classList.contains("open")) {
        target.style.maxHeight = 0;
        target.classList.remove("open");
      } else {
        // Close all accordion contents before opening the selected one
        document
          .querySelectorAll(".rb-accordion-content")
          .forEach((content) => {
            content.style.maxHeight = 0;
            content.classList.remove("open");
          });

        target.style.maxHeight = target.scrollHeight + "px";
        target.classList.add("open");
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const button = document.querySelector(".toggle");
  if (button) {
    button.addEventListener("click", function () {
      const form = document.getElementById("edit-form");
      if (!form.style.display) {
        form.style.display = 'none';
      }
      form.style.display = form.style.display === "none" ? "block" : "none";
    });
  }
});

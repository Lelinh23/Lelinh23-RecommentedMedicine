// for multi-select dropdown
const dropdown = document.querySelector(".dropdown");
const dropdownSelect = dropdown.querySelector(".dropdown-select");
const dropdownContent = dropdown.querySelector(".dropdown-content");
const searchInput = dropdown.querySelector("#search-input");

// Cho phép người dùng tìm kiếm và chọn nhiều mục từ dropdown
dropdownSelect.addEventListener("click", function () {
  dropdownContent.style.display = "block";
});

searchInput.addEventListener("input", function () {
  const searchValue = searchInput.value.toLowerCase();
  const buttons = dropdownContent.querySelectorAll("button");

  buttons.forEach(function (button) {
    const text = button.textContent.toLowerCase();
    if (text.includes(searchValue)) {
      button.style.display = "block";
    } else {
      button.style.display = "none";
    }
  });

  const selectedItems = dropdownSelect.querySelectorAll(".selected-item");
  selectedItems.forEach(function (selectedItem) {
    const selectedButton = dropdownContent.querySelector(
      `button[value="${selectedItem.textContent}"]`
    );
    if (selectedButton) {
      selectedButton.style.display = "none";
    }
  });
});

dropdownContent.addEventListener("click", function (event) {
  if (event.target.nodeName === "BUTTON") {
    const selectedItems = dropdownSelect.querySelectorAll(".selected-item");
    const button = event.target;

    if (!button.classList.contains("selected")) {
      // Add selected item
      const selectedItem = document.createElement("div");
      selectedItem.className = "selected-item";
      selectedItem.id = button.getAttribute("value");
      selectedItem.textContent = button.getAttribute("value");

      const removeButton = document.createElement("span");
      removeButton.className = "remove";
      removeButton.textContent = "✕";
      removeButton.addEventListener("click", function () {
        dropdownSelect.removeChild(selectedItem);
        button.classList.remove("selected");
      });

      selectedItem.appendChild(removeButton);
      dropdownSelect.appendChild(selectedItem);

      button.classList.add("selected");
    } else {
      // Remove selected item
      selectedItems.forEach(function (selectedItem) {
        if (selectedItem.textContent === button.getAttribute("value")) {
          dropdownSelect.removeChild(selectedItem);
          button.classList.remove("selected");
        }
      });
    }
  }
});
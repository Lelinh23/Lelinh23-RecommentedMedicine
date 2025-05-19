// Ẩn lớp hiển thị trạng thái tải (loading overlay) ban đầu
document.getElementById("loadingOverlay").style.display = "none"; 

// Hiển thị overlay tải trong khi dữ liệu được lấy từ server
function onButtonClick(disease, probability) {
  // Show the loading overlay
  document.getElementById("loadingOverlay").style.display = "flex";
  // Get the disease and probability values from the clicked button

  // Make the API call here
  $.ajax({
    url: "/admin/medic", // Update this URL to match your API route
    type: "GET",
    success: function (response) {
      // Process the API response
      console.log(disease, probability, response);

      // For example, you can call a function to display more details about the disease
      displaymedic(disease, probability);
    }.bind(null, disease, probability),
    error: function (error) {
      console.log("Error:", error);
      // Hide the loading overlay in case of error
      document.getElementById("loadingOverlay").style.display = "none";
    },
  });
}

document.getElementById("medic").addEventListener("click", medic);
// Lấy danh sách các bệnh và xác suất từ server.
// Hiển thị các nút tương ứng với từng bệnh trong buttonContainer.
// Khi người dùng nhấn vào nút, gọi hàm onButtonClick để xử lý thông tin.
function medic() {
  document.getElementById("medic").style.display = "none";
  document.getElementById("loadingOverlay").style.display = "none";
  document.getElementById("buttonContainer").style.display = "block";

  $.ajax({
    url: "/admin/medic",
    type: "GET",

    success: function (response) {
      var buttonContainer = document.getElementById("buttonContainer");
      buttonContainer.innerHTML = "get medication for: &nbsp<br><br>";
      // Loop through the 'response' array

      for (var i = 0; i < response.length; i++) {
        var disease = response[i].disease;
        var probability = response[i].probability;
        // Create a new button element
        var buttonElement = document.createElement("button");
        buttonElement.className = "dis";
        buttonElement.style.marginRight = "5px";
        // buttonElement.classList.add("dis");

        // Set the value of the button to the disease name
        buttonElement.textContent = disease;
        buttonElement.value = disease;

        // Add an event listener to the button using an IIFE
        (function (d, p) {
          console.log("mediv funnnc", d, p);
          buttonElement.addEventListener("click", function () {
            // Handle button click event here
            // For example, you can call a function to display more details about the disease
            onButtonClick(d, p);
          });
        })(disease, probability);

        // Append the button to the container
        buttonContainer.appendChild(buttonElement);
      }



      var nextitem1 = document.createElement("span");
      nextitem1.innerHTML =
        "_________________________________________________________<br>";
      buttonContainer.appendChild(nextitem1);
    },
    error: function (error) {
      console.log("Error:", error);
    },
  });
}


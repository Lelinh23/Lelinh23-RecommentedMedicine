// Gửi yêu cầu POST với dữ liệu bệnh và xác suất đến endpoint /displaymedic.
// Phản hồi từ server sẽ quyết định:
    // Nếu bệnh nguy hiểm (urgent), yêu cầu đi gặp bác sĩ ngay lập tức.
    // Nếu không, hiển thị danh sách thuốc kèm lời khuyên từ server.

function displaymedic(disease, probability) {
    document.getElementById("medications-container").style.display = "block";
  
    // Send an AJAX request to the server
    $.ajax({
      url: "/admin/displaymedic",
      type: "POST",
      data: { disease: disease, probability: probability},
      success: function (response) {
        document.getElementById("loadingOverlay").style.display = "none";
        // Check if 'gotohospital' key exists in the response
  
        // Append the medication element to the medications container
  
        if ("gotohospital" in response) {
          if (response["gotohospital"] == "urgent") {
            $("#medications-container").empty();
            var medicationElement1 = document.createElement("div");
            medicationElement1.innerHTML =
              "AGE>>>>>>>......GO TO A DOCTOR -- <b>URGENT !!!!</b>";
  
            // Append the medication element to the medications container
            $("#medications-container").append(medicationElement1);
          } else {
            // If 'gotohospital' key is present, it means probability is below 50
            console.log(
              "medication will be given to symptoms, not the disease, as probability is less than the threshold"
            );
            $("#medications-container").empty();
  
            // Append the medication element to the medications container
            $("#medications-container").append(medicationElement1);
  
            // Create a number range asking "How long have you been experiencing symptoms? (in days)"
            var duration = prompt(
              "How long have you been experiencing symptoms? (in days)"
            );
            // Perform any action you want with the 'duration' value
            if (duration > 5) {
              $("#medications-container").empty();
  
              var medicationElement1 = document.createElement("div");
              medicationElement1.innerHTML =
                "Seek medical attention <b>immediately</b> --- experiencing symptoms for <b>" +
                duration +
                "</b> days. <br><br>Use the option to <b>LOCATE NEARBY HOSPITALS</b> for assistance.<br> Consider consulting a <b>"+response["doc_type"]+"</b> for Diagnosis and Clarification.";
  
              // Append the medication element to the medications container
              $("#medications-container").append(medicationElement1);
            } else {
              console.log("medication for choosen symptoms:");
  
              // Perform any action with the medication response data received from Flask
              console.log(response);
              // Clear previous medications container content
              var medicationsElement = document.getElementById(
                "medications-container"
              );
              medicationsElement.innerHTML =
                "Medications given to <b>SYMPTOMS</b> <br>(as possibility of having <b>  " +
                response["disease"] +
                " (" +
                response["probability"] +
                "%)</b> is less then Threshold) <br> Consider consulting a <b>"+response["doc_type"]+"</b> for a more accurate diagnosis and clarification." ; 
  
              // Loop through the medications in the response
              for (var disease in response.medications) {
                var medicationList = response.medications[disease];
  
                var medicationContainer = document.createElement("div");
                var diseaseElement = document.createElement("h3");
                diseaseElement.textContent = disease;
                medicationContainer.appendChild(diseaseElement);
  
                // Create an unordered list for the medications of the current disease
                var medicationListElement = document.createElement("ul");
  
                // Loop through the medications for the current disease
                for (var i = 0; i < medicationList.length; i++) {
                  var medicationItem = document.createElement("li");
                  medicationItem.textContent = medicationList[i];
                  medicationListElement.appendChild(medicationItem);
                }
  
                medicationContainer.appendChild(medicationListElement);
                medicationsElement.appendChild(medicationContainer);
              }
            }
          }
        } else {
          // If 'gotohospital' key is not present, it means probability is above 50
          console.log("Recommend medicines based on dataset:");
  
          // Perform any action with the medication response data received from Flask
          console.log(response);
          var dis = response["disease"];
          var prob = response["probability"];
          // Here you can update the web page with the recommended medicines
          // Clear previous medications container content
  
          var medicationsElement = document.getElementById(
            "medications-container"
          );
          medicationsElement.innerHTML =
            "Medications for <b>" +
            response["disease"] +
            "</b> (" +
            response["probability"] +
            "%) based of patient Details</b> : <br> Consider consulting a <b>"+response["doc_type"]+"</b> for a more accurate diagnosis and clarification.<br><br>";
          // medicationsElement.appendChild(medicationContainer);
  
          // Display medications on the page
          var medications = response[dis];
          // const medications = response[response.disease];
          console.log("medic for prob >50", medications);
  
          if (medications && Array.isArray(medications)) {
            medications.forEach(function (medication) {
              var medicationElement = document.createElement("div");
              medicationElement.textContent = medication;
              // medicationsContainer.appendChild(medicationElement);
  
              medicationsElement.appendChild(medicationElement);
            });
          }
        }
      },
  
      error: function (error) {
        console.log("Error:", error);
      },
    });
}

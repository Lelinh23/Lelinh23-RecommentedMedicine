function sendSymptoms() {
    var values = [];
    $(".dropdown-select > div").each(function () {
        var value = $(this)
            .contents()
            .filter(function () {
                return this.nodeType === 3;
            })
            .text()
            .trim();
        values.push(value);
    });
    console.log(values);
  
    var name = document.getElementById("name").value;
    var age = document.getElementById("age").value;
    var gender = document.querySelector('input[name="gender"]:checked');
  
    if (name !== "") {
        if (age !== "") {
            if (gender) {
                if (values.length > 2) {
                    // Gửi dữ liệu đến server
                    $.ajax({
                        url: "/admin/send_data",
                        type: "POST",
                        contentType: "application/json",
                        data: JSON.stringify(values),
  
                        success: function (response) {
                            console.log("Data received from Flask", response);
                            var resultsElement = document.getElementById("results");
                            resultsElement.innerHTML = ""; // Xóa kết quả trước đó
  
                            // Hiển thị tiêu đề kết quả
                            var title = document.createElement("h3");
                            title.innerHTML = "Based on the given symptoms:";
                            resultsElement.appendChild(title);
  
                            var symptomsList = document.createElement("p");
                            symptomsList.innerHTML = `<b>${values.join(", ")}</b>`;
                            resultsElement.appendChild(symptomsList);
  
                            // Hiển thị từng kết quả bệnh
                            response.forEach((item, index) => {
                                var card = document.createElement("div");
                                card.style.margin = "15px 0"; // Khoảng cách giữa các kết quả
                                card.style.border = "2px solid #007bff";
                                card.style.padding = "5px";
                                card.className = "result-card";
  
                                var diseaseTitle = document.createElement("h4");
                                diseaseTitle.textContent = `Disease ${index + 1}: ${item.disease}`;
                                card.appendChild(diseaseTitle);
  
                                var probability = document.createElement("p");
                                probability.innerHTML = `Possibility: <b style="color:${item.probability >= 50 ? 'green' : 'red'}">${item.probability}%</b>`;
                                card.appendChild(probability);
  
                                if (item.probability < 50) {
                                    var advice = document.createElement("p");
                                    advice.innerHTML = `<i>As the probability is below the threshold, we recommend consulting a <b>${item.doc_type}</b>.</i>`;
                                    card.appendChild(advice);
                                }
  
                                var wikiButton = document.createElement("button");
                                wikiButton.className = "btn-wiki";
                                wikiButton.textContent = "Search Wiki";
                                wikiButton.style.marginRight = "20px";
                                wikiButton.addEventListener("click", () => {
                                    redirectToWikipedia(item.disease);
                                });
                                card.appendChild(wikiButton);
  
                                var precautionsButton = document.createElement("button");
                                precautionsButton.className = "btn-precautions";
                                precautionsButton.textContent = "Show Precautions";
                                precautionsButton.addEventListener("click", () => {
                                    alert(`Precautions for ${item.disease}:\n${item.precautions.join("\n")}`);
                                });
                                card.appendChild(precautionsButton);
  
                                resultsElement.appendChild(card);
                            });
                        },
                        error: function (xhr, status, error) {
                            console.error("Error in AJAX request:", xhr.responseText || error);
                            var resultsElement = document.getElementById("results");
                            resultsElement.innerHTML =
                                "Error occurred while processing the request. Details: " + (xhr.responseText || error);
                        },
                    });
                } else {
                    alert("Select at least 3 symptoms for better results");
                }
            } else {
                alert("Please select a gender");
            }
        } else {
            alert("Please fill in the age field");
        }
    } else {
        alert("Please fill in the name field");
    }
  }
  
  function redirectToWikipedia(disease) {
    var url = `https://en.wikipedia.org/wiki/${encodeURIComponent(disease)}`;
    window.open(url, "_blank");
  }
  
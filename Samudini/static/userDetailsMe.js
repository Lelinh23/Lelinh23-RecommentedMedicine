$(document).ready(function () {
    $("#myForm").submit(function (e) {
      document.getElementById("output").style.display = "block";
      document.getElementById("results").style.display = "block";
  
      e.preventDefault(); // Prevent form submission
      var name = $("#name").val();  
      var age = $("#age").val();
      var weight = $("#weight").val();
      var height = $("#height").val();
      var gender = $("input[name=gender]:checked").val();
      var alcohol = $("input[name=alcohol]:checked").val();
      var cigar = $("input[name=cigar]:checked").val();
      var preg = $("input[name=pregyesno]:checked").val();
      console.log(preg);
      var trisemister = $("input[name=trisemister]:checked").val();
  
      // Send an AJAX request to the server
      $.ajax({
        url: "/admin/update",
        type: "POST",
        data: {
          name: name,
          age: age,
          weight: weight,
          height: height,
          gender: gender,
          alcohol: alcohol,
          cigar: cigar,
          preg: preg,
          trisemister: trisemister,
        },
        // success: function(response) {
        //   $('#output').html(response); // Update the content of the element
        // }
        success: function (response) {
          console.log(
            response.name,
            response.age,
            response.weight,
            response.height,
            response.gender,
            response.alcohol,
            response.preg,
            response.trisemister
          );
          $("#output").empty(); // Clear the content of the element
          $("#output").append(" <b>User Details</b>:<br>________________<br>");
          $("#output").append(
            "<b>Name</b>: &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + response.name + "<br>"
          );
          $("#output").append(
            "<b>Age</b>: &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" +
              response.age +
              "yr<br>"
          );
          console.log(response.weight.length);
          if (response.weight.length == 0) {
            $("#output").append("<b>Weight</b>: &nbsp&nbsp&nbsp " + "-" + "<br>");
          } else {
            $("#output").append(
              "<b>Weight</b>: &nbsp&nbsp&nbsp " + response.weight + "kg<br>"
            );
          }
  
          if (response.height.length == 0) {
            $("#output").append(
              "<b>Height</b>: &nbsp&nbsp&nbsp&nbsp  " + "-" + "<br>"
            );
          } else {
            $("#output").append(
              "<b>Height</b>: &nbsp&nbsp&nbsp " + response.height + "cm<br>"
            );
          }
  
          $("#output").append(
            "<b>Gender</b>:&nbsp&nbsp&nbsp&nbsp " + response.gender + "<br>"
          );
  
          // console.log((response.alcohol).length);
  
          if (cigar === undefined) {
            $("#output").append(
              "<b>Cigar</b>: &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + "No" + "<br>"
            );
          } else {
            $("#output").append(
              "<b>Cigar</b>: &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + cigar + "<br>"
            );
          }
  
          if (response.age > 16) {
            if (response.alcohol.length == 5) {
              $("#output").append(
                "<b>Alcohol</b>:&nbsp&nbsp&nbsp&nbsp " + "Yes" + "<br>"
              );
            } else {
              $("#output").append(
                "<b>Alcohol</b>:&nbsp&nbsp&nbsp&nbsp " + "No" + "<br>"
              );
            }
  
            if (response.gender === "male") {
              $("#output").append(
                "<b>Pregnant</b>: &nbsp" + "not-applicable" + "<br>"
              );
              $("#output").append(
                "<b>trimister</b>: &nbsp" + "not-applicable" + "<br>" + "<br>"
              );
            } else {
              $("#output").append("<b>Pregnant</b>: &nbsp" + preg + "<br>");
  
              if (preg === "Yes") {
                var isSubset = ["A", "B", "C", "D"].every((item) =>
                  response.trisemister.includes(item)
                );
  
                if (isSubset) {
                  $("#output").append(
                    "<b>trimister</b>: &nbsp" + "1" + "<br>" + "<br>"
                  );
                } else {
                  $("#output").append(
                    "<b>trimister</b>: &nbsp" + "2/3" + "<br>" + "<br>"
                  );
                }
              } else {
                $("#output").append(
                  "<b>trimister</b>: &nbsp" + "not-applicable" + "<br>" + "<br>"
                );
              }
            }
          } else {
            $("#output").append(
              "<b>Alcohol</b>:&nbsp&nbsp&nbsp&nbsp " + "No" + "<br>"
            );
            $("#output").append(
              "<b>Cigar</b>: &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + "No" + "<br>"
            );
            $("#output").append("<b>Pregnant</b>: &nbsp" + "No" + "<br>");
            $("#output").append(
              "<b>trimister</b>: &nbsp" + "not-applicable" + "<br>" + "<br>"
            );
          }
        },
      });
    });
  });
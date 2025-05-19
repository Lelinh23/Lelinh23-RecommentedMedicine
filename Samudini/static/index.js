function stopBlinking() {
  var myDiv = document.getElementById("locate-hospital");
  myDiv.style.border = "2px solid #ff0000"; // Set the border back to red
  myDiv.classList.remove("blink-animation"); // Remove the animation class
  myDiv.style.cursor = "auto"; // Reset the cursor to default
}

const roundDiv = document.querySelector(".round-div");
const rectangleForm = document.querySelector(".rectangle-form");
const closeButton = document.querySelector(".close-button");

roundDiv.addEventListener("click", () => {
  rectangleForm.style.display = "block";
  document.getElementById("center").style.filter = "blur(4px)";
});

closeButton.addEventListener("click", () => {
  rectangleForm.style.display = "none";
  document.getElementById("center").style.filter = "blur(0px)";
});

const hospitalForm = document.getElementById("locate");
let map; // Declare the map variable

hospitalForm.addEventListener("submit", (event) => {
  event.preventDefault();

  document.getElementById("map").style.display = "block";
  var data = {
    locationOption: $("input[name='locationOption']:checked").val(),
    locationInput: $("#locationInput").val(),
    hospitalRange: $("#hospitalRange").val(),
  };

  $.ajax({
    url: "/locate",
    type: "POST",
    data: data,
    success: function (response) {
      console.log(response);

      var nearestHospitalsElement = $("#ans");
      nearestHospitalsElement.empty(); // Clear previous content

      var hospitalElement = document.createElement("div");
      // hospitalElement.textContent = JSON.stringify(response);
      // Display the nearest hospitals on the page

      nearestHospitalsElement.append(hospitalElement);

      // Plot the hospitals on the map
      plotHospitals(response);
    },
    error: function (error) {
      console.log("Error:", error);
    },
  });
});

function plotHospitals(hospitalsData) {
  console.log("in the map plot function");

  // Remove existing map instance if it exists
  if (map) {
    map.remove();
  }

  const startPoint = [hospitalsData.latitude, hospitalsData.longitude];
  map = L.map("map").setView(startPoint, 13);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  // Create a custom marker icon
  const customMarkerIcon = L.divIcon({
    className: "custom-marker-icon",
  });

  // Create the marker for the start point with the custom green icon and a popup
  L.marker(startPoint, { icon: customMarkerIcon, draggable: false })
    .bindTooltip("Your Location", { permanent: true, direction: "left" })
    .addTo(map);

  // Plot the hospitals
  for (let i = 0; i < hospitalsData.hospitalcount; i++) {
    const lat = hospitalsData["lat" + i];
    const lng = hospitalsData["long" + i];
    const hospitalName = hospitalsData["hospital" + i];
    const endPoint = [lat, lng];

    // Create the marker for the hospital with a custom popup for the hospital name
    const hospitalMarker = L.marker(endPoint, { draggable: false })
      .bindPopup(hospitalName) // Bind a custom popup to the hospital marker
      .addTo(map);

    // Add a click event listener to the hospital marker
    hospitalMarker.on("click", function () {
      // Remove the previously added routing control, if exists
      if (map.routingControl) {
        map.removeControl(map.routingControl);
      }

      // Calculate and display the route between start point and hospital
      map.routingControl = L.Routing.control({
        waypoints: [L.latLng(startPoint), L.latLng(endPoint)],
        routeWhileDragging: false, // Allow route calculation while dragging the markers
        createMarker: function (i, wp, nWps) {
          // Create a custom marker for the waypoints with hospital name as popup
          if (i === 0) {
            return L.marker(wp.latLng, { icon: customMarkerIcon }).bindPopup(
              "Your Location"
            );
          } else {
            return L.marker(wp.latLng, { icon: customMarkerIcon }).bindPopup(
              hospitalName
            );
          }
        },
      })
        .addTo(map)
        .on("routesfound", function (e) {
          // Get the calculated route
          const routes = e.routes;
          if (routes.length > 0) {
            const route = routes[0];
            const distance = route.summary.totalDistance; // Distance in meters
            console.log("Route Distance:", distance, "meters");
          }
        });
    });
  }
}


const floatingInputs = document.querySelectorAll(".floating-input");

function handleInputFocus(event) {
  const input = event.target;
  const label = input.previousElementSibling;

  label.style.top = "-12px";
  label.style.left = "10px";
  label.style.fontSize = "14px";
  label.style.color = "rgb(32, 162, 32)";
}

function handleInputBlur(event) {
  const input = event.target;
  const label = input.previousElementSibling;

  if (input.value === "") {
    label.style.top = "0px";
    label.style.left = "10px";
    label.style.fontSize = "14px";
    label.style.color = "#282727";
    // label.style.fontWeight = 'normal';
  }
}

function handleInputLoad(input) {
  const label = input.previousElementSibling;

  if (input.value !== "") {
    label.style.top = "-12px";
    label.style.left = "10px";
    label.style.fontSize = "14px";
    // label.style.fontWeight = 'normal';
  }
}

floatingInputs.forEach((input) => {
  input.addEventListener("focus", handleInputFocus);
  input.addEventListener("blur", handleInputBlur);
  handleInputLoad(input);
});







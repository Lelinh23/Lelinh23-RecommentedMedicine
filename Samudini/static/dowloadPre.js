window.onload = function () {
    document.getElementById("print").addEventListener("click", () => {
      try {
        // Clone the required elements
        const a = document.getElementById("output")?.cloneNode(true) || document.createElement("div");
        const b = document.getElementById("results")?.cloneNode(true) || document.createElement("div");
        const c = document.getElementById("medications-container")?.cloneNode(true) || document.createElement("div");
  
        // Remove #precdiv elements from the cloned node safely
        const precdivs = b.querySelectorAll("#precdiv");
        precdivs.forEach(div => div.remove());
  
        // Options for the PDF generation
        const opt = {
          margin: 0.7,
          filename: 'prescription.pdf',
          image: { type: 'jpeg', quality: 0.98 },
          html2canvas: { scale: 2 },
          jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
  
        // Get current date and time in the specified formats
        const now = new Date();
        const dateString = now.toLocaleDateString('en-GB', { day: '2-digit', month: '2-digit', year: 'numeric' }).split('/').join('-');
        const timeString = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
  
        // HTML content for the PDF
        const content = `
          <div style="text-align: center; margin-bottom: -15px; font-family: Ubuntu; font-weight: bold; font-size: xx-large;">Prescription</div>
          <div style="position: absolute; top: 10px; right: 10px; font-size: xx-small;">
            <div>${dateString} ${timeString}</div>
          </div>
          <p>____________________________________________________________________________________________</p>
          <div>${a.innerHTML}</div>
          <p>____________________________________________________________________________________________</p>
          <div style="font-weight: bold; margin-bottom: 5px;">Predicted Diseases:</div><br>
          <div>${b.innerHTML}</div>
          <p>____________________________________________________________________________________________</p>
          <div style="font-weight: bold; margin-bottom: 5px;">Medication:</div><br>
          <div>${c.innerHTML}</div>
          <p>____________________________________________________________________________________________</p>
          <div style="text-align: center; font-size: small;">
            <div style="font-weight: bold; margin-bottom: 5px;">DISCLAIMER</div>
            <div>Please note is not a substitute for professional medical advice.</div>
            <div>It is intended for informational purposes only and should not be considered a medical diagnosis.</div>
            <div>Always consult a qualified healthcare professional for accurate medical evaluation and treatment.</div>
          </div>`
  
        // Generate and download the PDF
        html2pdf().from(content).set(opt).save();
      } catch (error) {
        console.error("Error generating PDF:", error);
      }
    });
  };
  
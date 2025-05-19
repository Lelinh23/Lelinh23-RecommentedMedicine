// Quản lý việc bật/tắt trạng thái chọn cho các nút bấm (thêm hoặc bỏ class selected)
var buttons = document.getElementsByName("sym");
for (var i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener("click", function () {
    if (this.classList.contains("selected")) {
      this.classList.remove("selected");
    } else {
      this.classList.add("selected");
    }
  });
}

const checkbox = document.getElementById("t-c");
const submitButton = document.getElementById("t-c-submit");
const head = document.getElementById("head");

// Kích hoạt nút submit (submitButton) chỉ khi checkbox (t-c) được chọn.
checkbox.addEventListener("change", function () {
  submitButton.disabled = !this.checked;
});

var forms = document.getElementsByClassName("formContainer");
var headings = document.getElementsByTagName("h2");
var currentFormIndex = -1;

// Hiển thị form tương ứng với chỉ số index và thêm định dạng (như gạch chân hoặc đổi màu) cho tiêu đề tương ứng
function showForm(index) {
  for (var i = 0; i < forms.length; i++) {
    forms[i].classList.remove("active");
    headings[i].classList.remove("underline");
    headings[i].classList.remove("color");
  }
  console.log(currentFormIndex);
  forms[index].classList.add("active");
  headings[index].classList.add("underline");
  headings[index].classList.add("color");
}

// Chuyển sang form tiếp theo 
function nextForm() {
  if (currentFormIndex < forms.length - 1) {
    currentFormIndex++;
    showForm(currentFormIndex);
  }


  if (currentFormIndex == 0) {
    document.getElementById("backbtn").disabled = true;
    document.getElementById("heads").style.display = "flex";
    
  }

  // Tính chỉ số BMI từ chiều cao và cân nặng, đánh dấu triệu chứng "béo phì" nếu BMI ≥ 30.
  if(currentFormIndex==1){
    // Get height and weight values from the form
    var height = parseFloat((document.getElementById('height').value)/100); // in meters
    var weight = parseFloat(document.getElementById('weight').value); // in kilograms
    console.log(height,weight);

    // Calculate BMI
    var bmi = weight / (height * height);

    // Determine if obesity is present
    var isObese = bmi >= 30;

    // If obesity is present, select the "Obesity" option in the dropdown, Nếu BMI ≥ 30, chọn mục "obesity" trong dropdown
    if (isObese) {
          document.getElementById('obesity').selected = true;
    }
    else{
      document.getElementById('obesity').selected = false;
    }
  }

  if (currentFormIndex == 3) {
    document.getElementById("t-c-submit").disabled = true;
  } else {
    document.getElementById("backbtn").disabled = false;
    document.getElementById("t-c-submit").disabled = false;
    document.getElementById("predict").style.display = "block";
    document.getElementById("medic").style.display = "block";
  }

  document.getElementById("form0Container").style.display = "none";
}

// Quay lại form trước
function prevForm() {
  if (currentFormIndex > 0) {
    currentFormIndex--;
    showForm(currentFormIndex);
    document.getElementById("form0Container").style.display = "none";
  }
  
  if (currentFormIndex == 0) {
    document.getElementById("backbtn").disabled = true;
    document.getElementById("heads").style.display = "flex";
  }
  if (currentFormIndex == 3) {
    document.getElementById("t-c-submit").disabled = true;
    
  } else {
    
    document.getElementById("backbtn").disabled = false;
    document.getElementById("t-c-submit").disabled = false;
    document.getElementById("predict").style.display = "block";
    document.getElementById("medic").style.display = "block";
  }

  document.getElementById("output").style.display = "none";
  document.getElementById("results").style.display = "none";
  document.getElementById("buttonContainer").style.display = "none";
  document.getElementById("medications-container").style.display = "none";
  $("#medications-container").empty();
}

var ageInput = document.getElementById("age");
var genderInputs = document.getElementsByName("gender");
var question3 = document.getElementById("alcohol");
var question3dup = document.getElementById("cigar");
var question4 = document.getElementById("pregyesno");
var preginputs = document.getElementsByName("pregyesno");
var question5 = document.getElementById("trisemister");

ageInput.addEventListener("input", updateQuestions);
for (var i = 0; i < genderInputs.length; i++) {
  genderInputs[i].addEventListener("input", updateQuestions);
}
ageInput.addEventListener("input", updateQuestions);
for (var i = 0; i < preginputs.length; i++) {
  preginputs[i].addEventListener("input", updateQuestions);
}

// Hiển thị câu hỏi tùy thuộc vào độ tuổi và giới tính
function updateQuestions() {
  var age = parseInt(ageInput.value);
  var gender = getSelectedValue(genderInputs);
  var preg = getSelectedValue(preginputs);

  if (age > 16) {
    question3.style.display = "block";
    question3dup.style.display = "block";
    if (gender === "female") {
      question4.style.display = "block";
      if (preg === "Yes") {
        question5.style.display = "block";
      } else {
        question5.style.display = "none";
      }
    } else {
      question4.style.display = "none";
      question5.style.display = "none";
    }
  } else {
    question3.style.display = "none";
    question3dup.style.display = "none";
    question4.style.display = "none";
    question5.style.display = "none";
    // preg.style.display = "none";
  }
}

function getSelectedValue(inputs) {
  for (var i = 0; i < inputs.length; i++) {
    if (inputs[i].checked) {
      return inputs[i].value;
    }
  }
  return null;
}
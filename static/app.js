/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imageResult')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

$(function () {
    $('#upload').on('change', function () {
        readURL(input);
    });
});

/*  ==========================================
    SHOW UPLOADED IMAGE NAME
* ========================================== */
var input = document.getElementById( 'upload' );
var infoArea = document.getElementById( 'upload-label' );

input.addEventListener( 'change', showFileName );
function showFileName( event ) {
  var input = event.srcElement;
  var fileName = input.files[0].name;
  infoArea.textContent = 'File name: ' + fileName;
}

const myForm = document.getElementById("myForm");
const inpImg  = document.getElementById("upload")


myForm.addEventListener("submit", e =>{
  e.preventDefault();
  document.getElementById("result").innerHTML = '<p style="margin: 0; color: white; visibility: hidden;" id="result"><img src="static/resources/loading.svg" alt="" style="width: 35px;background: white; border-radius: 51%; "> Photo Uploaded...Processing...</p>'
  document.getElementById("result").style.visibility = "visible"
  const endpoint = "upload";
  formData = new FormData();
  formData.append('user-img', inpImg.files[0]);

  fetch(endpoint, {
    method: "post",
    body: formData
  }).then(
    response => response.json()
  ).then(
      (data) => {
          document.getElementById("result").style.fontSize = "20px"
          document.getElementById("result").style.fontWeight = "Bold"
          document.getElementById("result").innerHTML = data["result"]
      }
  );
 
});


const webcamElement = document.getElementById('webcam');

const canvasElement = document.getElementById('canvas');

const snapSoundElement = document.getElementById('snapSound');

const webcam = new Webcam(webcamElement, 'user', canvasElement, snapSoundElement);


$("#webcam-switch").change(function () {
    if(this.checked) {
        webcam.start()
            .then(result =>{
               cameraStarted();
               console.log("webcam started");
            })
            .catch(err => {
                displayError();
            });
    }
    else {        
        cameraStopped();
        webcam.stop();
        console.log("webcam stopped");
    }        
});

$('#cameraFlip').click(function() {
    webcam.flip();
    webcam.start();  
});

$('#closeError').click(function() {
    $("#webcam-switch").prop('checked', false).change();
});

function displayError(err = ''){
    if(err!=''){
        $("#errorMsg").html(err);
    }
    $("#errorMsg").removeClass("d-none");
}

function cameraStarted(){
    $("#errorMsg").addClass("d-none");
    $('.flash').hide();
    $("#webcam-caption").html("on");
    $("#webcam-control").removeClass("webcam-off");
    $("#webcam-control").addClass("webcam-on");
    $(".webcam-container").removeClass("d-none");
    if( webcam.webcamList.length > 1){
        $("#cameraFlip").removeClass('d-none');
    }
    $("#takePhoto").removeClass('d-none');
    window.scrollTo(0, 0); 
    $('body').css('overflow-y','hidden');
}

function cameraStopped(){
    $("#errorMsg").addClass("d-none");
    $("#webcam-control").removeClass("webcam-on");
    $("#webcam-control").addClass("webcam-off");
    $("#cameraFlip").addClass('d-none');
    $("#takePhoto").addClass('d-none');
    $(".webcam-container").addClass("d-none");
    $("#webcam-caption").html("Click to Start Camera");
}


$("#takePhoto").click(function () {
    beforeTakePhoto();
    let picture = webcam.snap();
    document.querySelector('#cameraImageResult').src = picture;
    afterTakePhoto();
});

function beforeTakePhoto(){
    $('.flash')
        .show() 
	.animate({opacity: 0.3}, 500) 
        .fadeOut(500)
        .css({'opacity': 0.7});
    window.scrollTo(0, 0); 
    $('#webcam-control').addClass('d-none');
    $('#cameraControls').addClass('d-none');
}

function afterTakePhoto(){
    // webcam.stop();
    // $('#canvas').removeClass('d-none');
    // $('#take-photo').addClass('d-none');
    $('#download-photo').removeClass('d-none');
    $('#webcam-control').removeClass('d-none');
    $('#cameraControls').removeClass('d-none');
}

function removeCapture(){
    $('#canvas').addClass('d-none');
    $('#webcam-control').removeClass('d-none');
    $('#cameraControls').removeClass('d-none');
    $('#take-photo').removeClass('d-none');
    $('#exit-app').addClass('d-none');
    $('#download-photo').addClass('d-none');
    $('#resume-camera').addClass('d-none');
}

const cameraForm = document.getElementById("myCameraForm");
const cameraImg  = document.querySelector('#cameraImageResult')

cameraForm.addEventListener("submit", e =>{
  e.preventDefault();
  document.getElementById("result").innerHTML = '<p style="margin: 0; color: white; visibility: hidden;" id="result"><img src="static/resources/loading.svg" alt="" style="width: 35px;background: white; border-radius: 51%; "> Photo Uploaded...Processing...</p>'
  document.getElementById("result").style.visibility = "visible"
  const endpoint = "upload";
  formData = new FormData();
  fetch(cameraImg.src)
    .then(res => res.blob())
    .then(blob => {
        const file = new File([blob], "capture.png", {
            type: 'image/png'
        });
        formData.append('user-img', file);

        fetch(endpoint, {
          method: "post",
          body: formData })
	  .then(response => response.json())
          .then((data) => {
              document.getElementById("result").style.fontSize = "20px"
              document.getElementById("result").style.fontWeight = "Bold"
              document.getElementById("result").innerHTML = data["result"]
          });
    });

});


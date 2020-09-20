var headerimgarray = ['michael-behrens-@mfbehrens99.jpg','eric-muhr-@ericmuhr.jpg'];

function getRandomImage(imgArray) {
  var base_url = "url('/static/trailcondition/images/"; // default path here
  var num = Math.floor( Math.random() * imgArray.length );
  var img = imgArray[ num ];
  var img_url = base_url + img + "')";
  document.getElementById('head').style.backgroundImage = img_url;
}

function checkPhoneNo() {
  var elMsg = document.getElementById('phonemessage');
  if this.value.length < 10) {
    elMsg.textContent = 'phone number must be 10 characters or more';
  } else {
    elMsg.textContent = '';
  }
}

 var elPhoneNo = document.getElementById('phoneno');
 elPhoneNo.addEventListener('blur', checkPhoneNo, false);
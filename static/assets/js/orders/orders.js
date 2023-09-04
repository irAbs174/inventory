function convertToPersian(numberInput) {
    var persianDigits = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];
    var convertedNumber = "";
    for (var i = 0; i < numberInput.length; i++) {
      var charCode = numberInput.charCodeAt(i);
      if (charCode >= 48 && charCode <= 57) {
        // Convert ASCII digits to Persian digits
        var persianDigit = persianDigits[charCode - 48];
        convertedNumber += persianDigit;
      } else {
        convertedNumber += numberInput.charAt(i);
      }
    }
    return convertedNumber;
  }

  function handleInputChange() {
    var inputElement = document.getElementById("validationDefault01");
    var inputValue = inputElement.value;
    var persianValue = convertToPersian(inputValue);
    inputElement.value = persianValue;
  }
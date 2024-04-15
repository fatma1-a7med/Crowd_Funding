
document.addEventListener("DOMContentLoaded", function() {

    spans = document.querySelectorAll('span');
    for (var j = 0; j < spans.length; j++) {
        spans[j].classList.add('d-block');
    }
    
    
    labels = document.querySelectorAll('label');
    
    for (var i = 0; i < labels.length; i++) {
        labels[i].classList.add('form-label');
    }
    
    inputs = document.querySelectorAll('input');
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].classList.add('form-control');
    }
   
    
    divs = document.getElementsByClassName("form_element")
    for (var d =0; d < divs.length; d++){
        divs[d].classList.add('mb-3')
    }
    
    checkboxex = document.querySelectorAll('input[type="checkbox"]');
    for (var c = 0; c < checkboxex.length; c++) {
        checkboxex[d].classList.remove('form-control')
    
        // Add or modify CSS properties to adjust the styling of checkboxes
        checkboxex[c].style.width = '20px'; // Example: Set width to 20px
        checkboxex[c].style.height = '20px'; // Example: Set height to 20px
        checkboxex[c].style.marginRight = '5px'; // Example: Add right margin of 5px
        checkboxex[c].style.verticalAlign = 'middle'; // Example: Vertically align to middle
        // Add more style properties as needed to customize the checkboxes
    }
    checkboxex=document.querySelectorAll('input[type="checkbox"]')
    for (var d =0; d < checkboxex.length; d++){
    }
    
    errors = document.getElementsByClassName('errorlist');
    for (var m = 0; m < errors.length; m++) {
        errors[m].style.color = 'red';
        errors[m].style.fontWeight = 'bold';
    }
    
    });
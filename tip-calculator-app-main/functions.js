function calc(discount){
    var bill = document.getElementById("bill").value;
    var amtPeople = document.getElementById("numberOfPeople").value;

    if(bill == 0 || amtPeople == 0) return;

    if(discount == -1){
        discount = document.getElementById("customButton").value / 100;
    }

    var tip = (bill * discount).toFixed(2);
    bill = (bill * (1+discount)).toFixed(2);

    document.getElementById("tipPerPerson").innerHTML = "$" + (tip / amtPeople).toFixed(2);
    document.getElementById("totalPerPerson").innerHTML = "$" + (bill / amtPeople).toFixed(2);
}

var activeButtonId = ""; // button that was recently pressed
function _resetActiveButton(){
    if(activeButtonId != ""){
        const activeButton = document.getElementById(activeButtonId);
        activeButton.style.backgroundColor = "hsl(183, 100%, 15%)";
        activeButton.style.color = "hsl(0, 0%, 100%)";
        activeButton.disabled = true;
        activeButtonId = "";
    }
}

function validateNumber(){
    var amtPeople = document.getElementById("numberOfPeople").value;
    if(amtPeople != 0){
        document.getElementById("errorMessage").innerHTML = "";
        document.getElementById("numberOfPeople").style.borderColor = "transparent";
        return true;
    }
    
    document.getElementById("errorMessage").innerHTML = "Can't be zero";
    document.getElementById("numberOfPeople").style.border = "2px solid hsl(22, 82%, 47%)";
    document.getElementById("tipPerPerson").innerHTML = "$" + (0).toFixed(2);
    document.getElementById("totalPerPerson").innerHTML = "$" + (0).toFixed(2);
    _resetActiveButton();
    return false;
}

function setButton(id, discount){ // sets the color of a button to 'clicked' color
    if(id != "reset"){
        const ret = validateNumber();
        if(!ret) return;
    } 
    
    document.getElementById(id).style.backgroundColor = "hsl(172, 67%, 45%)";
    document.getElementById(id).style.color = "hsl(183, 100%, 15%)";

    if(id == "reset") return;

    calc(discount);

    if(activeButtonId != "" && activeButtonId != id){
        _resetActiveButton();
    }
    activeButtonId = id;
}

function reset(){
    // zmiana kolorow
    document.getElementById("reset").style.backgroundColor = "hsl(183, 98%, 21%)";
    _resetActiveButton();
    
    // usuwanie wartosci ze zmiennych
    document.getElementById("bill").value = 0;
    document.getElementById("numberOfPeople").value = 0;
    document.getElementById("tipPerPerson").innerHTML = "$" + (0).toFixed(2);
    document.getElementById("totalPerPerson").innerHTML = "$" + (0).toFixed(2);
    document.getElementById("errorMessage").innerHTML = "";
    document.getElementById("numberOfPeople").style.borderColor = "transparent";
    document.getElementById("customButton").value = "Custom";
}
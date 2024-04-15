"use strict";

// currencies as a list
/*const currencies = [
  {name: "USD", value: 1}, 
  {name: "EUR", value: 0.94}, 
  {name: "JPY", value: 153.06}, 
  {name: "PLN", value: 4.02},
];

// adding names of currencies as options to select

function addToSelect(selectName) { 
  const selectField = document.querySelector(selectName);

  currencies.forEach(function(entry) {
    selectField.options.add(new Option(entry.name, entry.name));
  });
}*/



// list of all available currencies (as a dictionary)
// value - how much for 1 USD (as of 14.04.2024)

// POTENTIAL FOR DEVELOPMENT: add exchange rates that are taken real time from the internet
const currencies = {
  USD : 1,
  EUR : 0.94,
  JPY: 153.06,
  PLN: 4.02,
};


// adding names of currencies as options to select

function addToSelect(selectName) {
  const selectField = document.querySelector(selectName);

  for(const [key, ] of Object.entries(currencies)) {
    selectField.options.add(new Option(key, key));
  }
}

addToSelect("#currencyFrom");
addToSelect("#currencyTo");

// !!!! ustawic domyslne EUR dla currencyTo - zeby nie bylo to samo co w przypadku currencyFrom




// converting currencies A -> B (A to USD, USD to B)

function onConvert() {
  if(document.querySelector("#amtToConvert").value < 0){
     document.querySelector("#error").innerHTML = "The value must be greater or equal to 0.";
     return;
  }

  const result = getConvertedAmount(
    document.querySelector("#amtToConvert").value, 
    document.querySelector("#currencyFrom").value,
    document.querySelector("#currencyTo").value
  );
  document.querySelector("#resultAmount").innerHTML = result + " " + document.querySelector("#currencyTo").value;
}

function getConvertedAmount(amountToConvert, currencyA, currencyB) {
  return (amountToConvert / currencies[currencyA] * currencies[currencyB]).toFixed(2);
}
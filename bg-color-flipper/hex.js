"use strict";

let colors = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F'];

const buttonColorFlip = document.querySelector('#btn-color-flip');
buttonColorFlip.addEventListener('click', () => {
    let newColor = getColor();
      
    document.body.style.backgroundColor = newColor;

    document.getElementById("bg-color-text").innerHTML = newColor;
    document.getElementById("bg-color-text").style.color = newColor;
  });

function getColor(){
  let result = '#';
  for(let i=0; i<6; ++i){
    result += colors[Math.floor(Math.random() * colors.length)];
  }
  return result;
}
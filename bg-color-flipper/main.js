"use strict";

const colors = ["#EDF6F9", "#83C5BE", "#006D77", "#FFDDD2", "#E29578"];

const buttonColorFlip = document.querySelector('#btn-color-flip');
buttonColorFlip.addEventListener('click', () => {
    let newColor = colors[Math.floor(Math.random() * colors.length)];
    document.body.style.backgroundColor = newColor;

    document.getElementById("bg-color-text").innerHTML = newColor;
    document.getElementById("bg-color-text").style.color = newColor;
  });

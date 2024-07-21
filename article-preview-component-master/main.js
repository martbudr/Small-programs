"use strict";

const shareButton = document.getElementById("share-button"),
  shareMenuTriangle = document.getElementById("share-menu-triangle"),
  shareMenu = document.getElementById("share-menu");

let shareMenuVisible = Boolean(false);

shareButton.addEventListener('click', () => {

  if(shareMenuVisible === Boolean(false)){
    shareMenu.style.display = 'block';
    shareMenuTriangle.style.display = 'block';
    shareMenuVisible = Boolean(true);

    shareButton.style.background = '#6d7f97';
    document.getElementById('button-icon').src = 'images/icon-share-light.svg';

    return;
  }

  shareMenu.style.display = 'none';
  shareMenuTriangle.style.display = 'none';
  shareMenuVisible = Boolean(false);

  shareButton.style.background = '#ecf2f8';
  document.getElementById('button-icon').src = 'images/icon-share.svg';
});
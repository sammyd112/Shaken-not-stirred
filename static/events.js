'use strict';
// import * as crud from crud.py
// //Add event listener for search cocktail button//
const searchCocktail = document.querySelector('#search_cocktail')
searchCocktail.addEventListener("submit", (evt) => {
  evt.preventDefault()
  const formInputs = {
    drink_input: document.querySelector('#drink_input').value,
  };
  console.log("test")

  fetch('/stayin', {
    method: 'post',
    body: JSON.stringify(formInputs),
    headers: {
      'Content-Type': 'application/json'
  }})
  .then((response) => response.json())
  .then((drinkData) => {
    console.log(drinkData)
    document.getElementById('cocktail_result').innerHTML = `<div>${drinkData['name']}</div>
                                                          <br>
                                                          <div> The Ingredients are as follows: </div>
                                                          <div> ${drinkData['ingredients']}  </div>
                                                          <br>
                                                          <div> How to make: </div>
                                                          <div> ${drinkData['instruction']} </div>`
})})

// loop with java//
// ul with li elements inside//
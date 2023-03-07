'use strict';

//Add event listener for search cocktail button//
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
                                                          <ul>`
    for (const ingredient of drinkData['ingredients']){                                                   
    document.getElementById('cocktail_result').innerHTML += `<li> ${ingredient} </li>`
                                                        }
    document.getElementById('cocktail_result').innerHTML += `</ul>
                                                            <br>
                                                             <div> How to make: </div>
                                                             <div> ${drinkData['instruction']} </div>`
})})

// loop with java//
// ul with li elements inside//


// Add event listeners for quiz//
const quizButton = document.querySelector('#quiz')
quizButton.addEventListener("click", (evt) => {
  evt.preventDefault()
  console.log('Q1')
  fetch('/goingout', {
    method: 'post',
    body: document.querySelector('form'),
    headers: {
      'Content-Type': 'application/json'
  }})
      .then((response) => response.json())
      .then((quizData) => {
        console.log(quizData)
        document.getElementById('question1').innerHTML = `<div> What is your perferred cocktail strength? </div>
                                                          <br>`
        for (const strength of quizData['strengths']) {
          document.getElementById('question1').innerHTML += `<input type ="checkbox" name="strengths" value=${strength} id="strengths">
                                                            <label for="strengths">${strength}</label>`;
        }
        document.getElementById('question1').innerHTML += `<br><input type= "submit" id="q1"></input>`


        document.querySelector('#q1').addEventListener("click", (evt) => {
          evt.preventDefault()
          console.log('Q1 sumbitted')
          document.getElementById('question2').innerHTML = `<div> What are your perferred cocktail flavors? </div>
                                                          <br>`
          for (const flavor of quizData['flavors']) {
          document.getElementById('question2').innerHTML += `<input type ="checkbox" name="flavors" value=${flavor} id="flavors">
                                                            <label for="flavors">${flavor}</label>`;
        }
        document.getElementById('question2').innerHTML += `<br><input type= "submit" id="q2"></input>`
      



        document.querySelector('#q2').addEventListener("click", (evt) => {
          evt.preventDefault()
          console.log('Q2 sumbitted')
          document.getElementById('question3').innerHTML = `<div> What are your perferred spirits? </div>
                                                          <br>`
          for (const spirit of quizData['spirits']) {
          document.getElementById('question3').innerHTML += `<input type ="checkbox" name="spirit" value=${spirit} id="spirits">
                                                            <label for="spirits">${spirit}</label>`;
        }
        document.getElementById('question3').innerHTML += `<br><input type= "submit" id="q3"></input>`


        document.querySelector('#q3').addEventListener("click", (evt) => {
          evt.preventDefault()
          console.log('Q3 sumbitted')
        })})})
})});

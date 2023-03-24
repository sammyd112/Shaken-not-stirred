'use strict';

// Add event listeners for quiz//

const quizButton = document.querySelector('#quiz')
quizButton.addEventListener("click", (evt) => {
  evt.preventDefault()
  fetch('/quizchoices') 
      .then((response) => response.json())
      .then((quizData) => {
               
        for (const strength of quizData['strengths']) {
          document.getElementById('question-content1').innerHTML += `<div><input type ="checkbox" name="strengths" value="${strength}">
                                                                    <label for="strengths">${strength}</label><div>`;
        }
        for (const flavor of quizData['flavors']) {
          document.getElementById('question-content2').innerHTML += `<div><input type ="checkbox" name="flavors" value="${flavor}">
                                                                    <label for="flavors">${flavor}</label></div>`;
        }
        for (const spirit of quizData['spirits']) {
          document.getElementById('question-content3').innerHTML += `<div><input type ="checkbox" name="spirits" value="${spirit}">
                                                                    <label for="spirits">${spirit}</label></div>`;
        }

        document.querySelector('#next').addEventListener("click", (evt) => {
          evt.preventDefault()
          document.getElementById("q1").classList.add("d-none");
          document.getElementById("q2").classList.remove("d-none");
          document.getElementById("question-content1").classList.add("d-none");
          document.getElementById("question-content2").classList.remove("d-none");



        document.querySelector('#next').addEventListener("click", (evt) => {
          evt.preventDefault()
          document.getElementById("q2").classList.add("d-none");
          document.getElementById("q3").classList.remove("d-none");
          document.getElementById("question-content2").classList.add("d-none");
          document.getElementById("question-content3").classList.remove("d-none");
          document.getElementById("next").classList.add("d-none");
          document.getElementById("exit").classList.add("d-none");
          document.getElementById("submit-quiz").classList.remove("d-none");
 
        })})
})});

///Add event listener to submission of quiz//
let idChange= -1
const quizsubButton = document.querySelector("#submit-quiz")
quizsubButton.addEventListener("click", (evt) => {
  evt.preventDefault()
  const quizData = new FormData(document.getElementById("quiz-questions"));
  console.log(quizData)
  fetch('/quiz', {
    method: 'post',
    body: quizData,
  })
  .then((response) => response.json())
  .then((quizData) => {
    console.log(quizData)
    let num = 0
    for (const cocktail of quizData['matches']) {
      num += 1
      document.getElementById('suggestionbody').innerHTML += `<div class="col">
                                                                <div class="card h-100 w-300">
                                                                  <img src="..." class="card-img-top" alt="...">
                                                                  <div class="card-body">
                                                                    <h5 class="card-title" id=${num}>${cocktail['name']}</h5>
                                                                    <div class="card-text">Ingredients:</div>
                                                                    <div class="card-text" id="ingredients${num}"></div>
                                                                    
                                                                    <div class="card-text">Flavors:</div>
                                                                    <div class="card-text" id="flavors${num}"></div>
                                                                    <div class="card-text">Strength:</div>
                                                                    <div class="card-text" id="strength${num}"></div>
                                                                    <div class="card-footer text-muted">
                                                                    <a href="#" onclick='idChange=${num}' data-bs-toggle="modal" data-bs-target="#addfav">Add to Favorites!</a>
                                                                    </div>
                                                                  </div>
                                                                </div>
                                                              </div>`;
      for (const ingredient of cocktail['ingredients']){
            document.getElementById(`ingredients${num}`).innerHTML += `<li>${ingredient}</li>`;
      }
      
      for (const flavor of cocktail['flavors']){
        if (flavor != null) {
        document.getElementById(`flavors${num}`).innerHTML += `<li>${flavor}</li>`;
      }}
      document.getElementById(`strength${num}`).innerHTML += `<li>${cocktail['strength']}</li>`;
  
  }})})

// Add event listener for random cocktail//
const randomButton = document.querySelector('#random')
randomButton.addEventListener("click", (evt) => {
  evt.preventDefault()
  console.log('random')
  fetch('/random')
  .then((response) => response.json())
  .then((randomData) => {
    console.log(randomData)
    document.getElementById('random-contents').innerHTML = `<h1 id="cocktailname"> ${randomData['name']} </h1> <br>`
    document.getElementById('random-contents').innerHTML += '<div> The Ingredients are as follows: </div> <ul>'              
    for (const ingredient of randomData['ingredients']){                                                   
    document.getElementById('random-contents').innerHTML += `<li> ${ingredient} </li>`
                                                        }
    document.getElementById('random-contents').innerHTML += '</ul>'
})})


// Add event listener for cocktail Roulette//
const routletteButton = document.querySelector('#roulette')
routletteButton.addEventListener("click", (evt) => {
  evt.preventDefault()
  console.log('roulette')
  fetch('/russian')
  .then((response) => response.json())
  .then((russianData) => {
    console.log(russianData)
    document.getElementById("routlette-contents").innerHTML = `<div> Do not blame me </div> 
                                                              <br> <ul>
                                                              <li> Your spirit is: ${russianData['spirit']}</li>
                                                              <li> Your coridal is: ${russianData['cordial']}</li>
                                                              <li> Your ingredient is: ${russianData['ingredient']}</li></ul>`
})})

  // /Add Event Listener to Favorite///
  const favoriteCocktail = document.getElementById('addfavorite')
  favoriteCocktail.addEventListener("click", (evt) => {
    evt.preventDefault()
    const drinkName = {
      drink_name : document.getElementById(`${idChange}`).innerText,
    };
    fetch('/addfavorite', {
      method: 'post',
      body: JSON.stringify(drinkName),
      headers: {
        'Content-Type': 'application/json'
    }})
    .then((response) => response.json())
    .then((drinkData) => {
      document.getElementById('insert').innerHTML = `<div class='alert alert-${drinkData['message'][0]} alert-dismissible fade show' role='alert' 
                                                      data-mdb-delay="3000" style="margin-bottom: 0px";>
                                                      ${drinkData['message'][1]}
                                                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                                      </div>`          
  })
})

  const favCocktail = document.getElementById('favorite')
  favCocktail.addEventListener("click", (evt) => {
    evt.preventDefault()
    const drinkName = {
      drink_name : document.getElementById('cocktailname').innerText,
    };
    fetch('/addfavorite', {
      method: 'post',
      body: JSON.stringify(drinkName),
      headers: {
        'Content-Type': 'application/json'
    }})
    .then((response) => response.json())
    .then((drinkData) => {
      document.getElementById('insert').innerHTML = `<div class='alert alert-${drinkData['message'][0]} alert-dismissible fade show' role='alert' 
      data-mdb-delay="3000" style="margin-bottom: 0px";>
      ${drinkData['message'][1]}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>`        
  })
       
        
})


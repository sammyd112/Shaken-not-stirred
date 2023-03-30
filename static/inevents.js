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
    if("name" in drinkData === true){
      document.getElementById('cocktail-name').innerHTML = `<div id='cocktailname'> ${drinkData['name']}</div>`
      document.getElementById('ingredients').innerHTML = '<div> The Ingredients are as follows: </div> <ul>'              
      for (const ingredient of drinkData['ingredients']){ 
        if (ingredient[0] != null)  {  
          if (ingredient[1] != null){                                           
              document.getElementById('ingredients').innerHTML += `<li> ${ingredient[0]}, ${ingredient[1]}</li>`
          }else{
            document.getElementById('ingredients').innerHTML += `<li> ${ingredient[0]} </li>`
        }}}
      document.getElementById('ingredients').innerHTML += `</ul>`
      if ("cocktail_id" in drinkData === true){
        console.log("true1")
      document.getElementById('ingredients').innerHTML +=  `<img src="https://res.cloudinary.com/dbdyyg3uy/image/upload/v1679991595/cocktails/${drinkData['cocktail_id']}.jpg" class='center'>
                                                              <br>`
      }
      else if ("instruction" in drinkData === true){
        console.log("true")
       document.getElementById('ingredients').innerHTML += `<div> How to make: </div>
                                                              <div> ${drinkData['instruction']} </div> <br>`;
        }
      if (document.getElementById('favorite').classList.contains('disabled') == true){
        document.getElementById('favorite').classList.remove('disabled')
      }
    } else {
      document.getElementById('cocktail-name').innerHTML = `<div> No Result </div>`
      document.getElementById('ingredients').innerHTML = '<div>..Check spelling or search a different cocktail..</div> <ul>' 
      document.getElementById('favorite').classList.add('disabled')
    }
                        
})})


///Add event listener for make cocktail///
const makeButton = document.querySelector('#make_cocktail')
makeButton.addEventListener("click", (evt) => {
  evt.preventDefault()
  fetch('/makechoices') 
      .then((response) => response.json())
      .then((choicesData) => {
        console.log(choicesData)
               
        for (const rum of choicesData['spirits']['Rums']) {
          document.getElementById('rums').innerHTML += `<br><input type ="checkbox" name="ingred" value="${rum}" id="${rum}">
                                                        <label for="${rum}">${rum}</label>`;
        }
        for (const vodka of choicesData['spirits']['Vodkas']) {
          document.getElementById('vodka').innerHTML += `<br><input type ="checkbox" name="ingred" value="${vodka}" id="${vodka}">
                                                          <label for="${vodka}">${vodka}</label>`;
        }
        for (const whiskey of choicesData['spirits']['Whiskey and Similar']) {
          document.getElementById('whiskeys').innerHTML += `<br><input type ="checkbox" name="ingred" value="${whiskey}" id="${whiskey}">
                                                            <label for="${whiskey}">${whiskey}</label>`;
        }
        for (const cordial of choicesData['cordials']) {
          document.getElementById('question-content2').innerHTML += `<input type ="checkbox" name="ingred" value="${cordial}" id="${cordial}">
                                                                    <label for="${cordial}">${cordial}</label><br>`;
        }
        for (const ingredient of choicesData['ingredients']) {
          document.getElementById('question-content3').innerHTML += `<input type ="checkbox" name="ingred" value="${ingredient}" id="${ingredient}">
                                                                      <label for="${ingredient}">${ingredient}</label><br>`;
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
          document.getElementById("submit-make").classList.remove("d-none");
 
        })})
})});


///Add event listener to submission of make cocktail//
let idChange = -1
const submakeButton = document.querySelector("#submit-make")
submakeButton.addEventListener("click", (evt) => {
  evt.preventDefault()
  const quizData = new FormData(document.getElementById("make-questions"));
  console.log(quizData)
  fetch('/makesuggestions', {
    method: 'post',
    body: quizData,
  })
  .then((response) => response.json())
  .then((matchData) => {
    let num = 0
    for (const cocktail of matchData) {
      num += 1
      document.getElementById('suggestionbody').innerHTML += `<div class="col">
                                                                <div class="card h-100 w-300">
                                                                  <img src="https://res.cloudinary.com/dbdyyg3uy/image/upload/v1679991595/cocktails/${cocktail['cocktail_id']}.jpg" class="center" alt="...">
                                                                  <div class="card-body">
                                                                    <h5 class="card-title" id="${num}">${cocktail['name']}</h5>
                                                                    <p class="card-text">Ingredients:</p>
                                                                    <div class="card-text" id="parts${num}">
                                                                    <ul>
                                                                  </div>
                                                                  <br>
                                                                  <div class="card-footer text-muted">
                                                                    <a href="#" class="center" onclick='idChange=${num}' data-bs-toggle="modal" data-bs-target="#addfav"<p style="text-align:center">Add to Favorites!</a>
                                                                </div>
                                                              </div>`;
      for (const ingredient of cocktail['ingredients']){
            console.log(ingredient)
            document.getElementById(`parts${num}`).innerHTML += `<li>${ingredient[0]}-${ingredient[1]}</li>`;
      }
            document.getElementById(`parts${num}`).innerHTML += `</ul>`
          if (cocktail['missing'].length === 1){
            document.getElementById(`parts${num}`).innerHTML += `<br>Missing: ${cocktail['missing']}</div>`;
          } else {
            continue;
      }}
  })})

  ///Add Event Listener to Favorite///
const favoriteSearch = document.getElementById("addfavorite")
favoriteSearch.addEventListener("click", (evt) => {
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

  ///Add Event Listener to Favorite///
  const favoriteCocktail = document.getElementById('favorite')
  favoriteCocktail.addEventListener("click", (evt) => {
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
'use strict'

// showing favorites from databases
let idChange = -1 
const displayFavorites = document.getElementById('show-favorites')
displayFavorites.addEventListener("click", (evt) => {
    evt.preventDefault()
    fetch('/showfavorites',)
    .then((response) => response.json())
    .then((favData) => {
      console.log(favData)
      let num = 0;
    for (const cocktail of favData['personal']){
        num += 1
        if (cocktail['ingredients'][7] == 'database'){
          document.getElementById('lovedcocktails').innerHTML +=`<div class="col">
                                                                <div class="card h-100">
                                                                   <div class="card-body">
                                                                      <h5 class="card-title" id="${num}">${cocktail['name']}</h5>
                                                                      <p class="card-text" id="body${num}"><ul></p>
                                                                    </div>
                                                                    <div class="card-footer text-muted">
                                                                    <a href="#" onclick='idChange=${num}' data-bs-toggle="modal" data-bs-target="#confirmModal">Remove This Favorite</a>
                                                                    </div>
                                                                  </div>
                                                                </div>`
        } else {
        document.getElementById('lovedcocktails').innerHTML +=`<div class="col">
                                                                <div class="card h-100">
                                                                   <div class="card-body">
                                                                      <h5 class="card-title" id="${num}">${cocktail['name']}</h5><span>(You Created)</span>
                                                                      <p class="card-text" id="body${num}"><ul></p>
                                                                    </div>
                                                                    <div class="card-footer text-muted">
                                                                    <a href="#" onclick='idChange=${num}' data-bs-toggle="modal" data-bs-target="#confirmModal">Remove This Favorite</a>
                                                                    </div>
                                                                  </div>
                                                                </div>`
        }
        for (const ingredient of cocktail ['ingredients']){
          // '(,)'
            if (ingredient != 'database'){
              if (ingredient != "(,)"){
              if (ingredient != ''){
                document.getElementById(`body${num}`).innerHTML += `<li>${ingredient}</li>`;
            }}} 
        }
        document.getElementById(`body${num}`).innerHTML+= `</ul>`;
        document.getElementById(`body${num}`).innerHTML+= `<div>Note: ${cocktail['notes']}</div>`
    }
    for (const cocktail of favData['favorites']){
        num += 1
        document.getElementById('lovedcocktails').innerHTML += `<div class="col">
                                                              <div class="card h-100">
                                                                <img src="..." class="card-img-top" alt="...">
                                                                <div class="card-body">
                                                                    <h5 class="card-title" id="${num}">${cocktail['name']}</h5>
                                                                    <p class="card-text" id="body${num}"><ul></p>
                                                                </div>
                                                                <div class="card-footer text-muted">
                                                                    <a href="#" onclick='idChange=${num}' data-bs-toggle="modal" data-bs-target="#confirmModal">Remove This Favorite</a>
                                                                </div>
                                                              </div>
                                                            </div>`
        for (const ingredient of cocktail['ingredients']){
            document.getElementById(`body${num}`).innerHTML+= `<li>${ingredient}</li>`;
      }
        document.getElementById(`body${num}`).innerHTML+= `</ul>`;
    }
    document.getElementById("show-favorites").classList.add("d-none");
    document.getElementById("hide-favorites").classList.remove("d-none");          
  })})

// event listener for confirmation of delete from modal
const confirmdelete = document.getElementById('confirmdelete')
  confirmdelete.addEventListener("click", (evt) => {
      evt.preventDefault()
      const drinkName = {
        drink_name : document.getElementById(`${idChange}`).innerText,
      };
      console.log("work")
      console.log(drinkName)
      fetch('/deletefav', {
        method: 'post',
        body: JSON.stringify(drinkName),
        headers: {
          'Content-Type': 'application/json'
      }})
  })
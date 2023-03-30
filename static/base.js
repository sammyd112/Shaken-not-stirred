'use strict'
  const confirmAge = document.getElementById('confirmage')
confirmAge.addEventListener("click", (evt) => {
    evt.preventDefault()
    const age = {
      age : document.getElementById('confirmage').innerText,
    };
    console.log(age)
    fetch('/getage', {
      method: 'post',
      body: JSON.stringify(age),
      headers: {
        'Content-Type': 'application/json'
    }})
  })
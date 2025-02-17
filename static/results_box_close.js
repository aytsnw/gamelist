document.addEventListener('DOMContentLoaded', ()=>{
    let body = document.body;
    let searchBar = document.querySelector('.navInput')
    let resultsBox = document.querySelector('.navResults');
    body.addEventListener('click', (event)=>{
        if (!(resultsBox.contains(event.target)) && !(searchBar.contains(event.target))){
        resultsBox.style.display = "none";
        }
    });
});
document.addEventListener('DOMContentLoaded', ()=>{
    let menuIconButton = document.getElementById('menuIconButton');
    let navButtons = document.querySelectorAll('.navButton')
    let searchBar = document.querySelector('.navForm')
    menuIconButton.addEventListener('click', ()=>{
        if (searchBar.style.display != "none"){
            searchBar.style.display = "none";
            for (let i = 0; i < navButtons.length; i++){
                navButtons[i].style.display = "flex";
            }
        }
        else{
            searchBar.style.display = "flex";
            for (let i = 0; i < navButtons.length; i++){
                navButtons[i].style.display = "none";
            }
        }
    });
});
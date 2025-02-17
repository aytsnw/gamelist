document.addEventListener('DOMContentLoaded', () =>{
    toggleButton = document.getElementById('toggleButton');
    chevron = document.getElementById('chevron')
    toggleMenu = document.getElementById('toggleMenu');
    toggleButton.addEventListener('click', ()=>{
        if (toggleMenu.style.display === "none"){
            toggleMenu.style.display = "flex";
            chevron.style.display = "flex";
            chevron.innerHTML = "chevron_left"
        }
        else{
            toggleMenu.style.display = "none";
            chevron.style.display = "none";
        }
    });

});
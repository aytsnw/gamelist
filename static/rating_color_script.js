document.addEventListener('DOMContentLoaded', ()=>{
    ratingSquare = document.querySelectorAll('.rating');

    for (let i = 0; i < ratingSquare.length; i++){
        if (parseFloat(ratingSquare[i].innerHTML) >= 8){
            ratingSquare[i].style.backgroundColor = "green";
        }
        else if (parseFloat(ratingSquare[i].innerHTML) < 4){
            ratingSquare[i].style.backgroundColor = "red";
        }
        else{
            ratingSquare[i].style.backgroundColor = "rgb(204, 153, 0)";
        }
    }
});

document.addEventListener('DOMContentLoaded', ()=>{
    ratingSquare = document.querySelectorAll('.ratingMylist');

    for (let i = 0; i < ratingSquare.length; i++){
        if (parseFloat(ratingSquare[i].innerHTML) >= 8){
            ratingSquare[i].style.backgroundColor = "green";
        }
        else if (parseFloat(ratingSquare[i].innerHTML) < 4){
            ratingSquare[i].style.backgroundColor = "red";
        }
        else{
            ratingSquare[i].style.backgroundColor = "rgb(204, 153, 0)";
        }
    }
});

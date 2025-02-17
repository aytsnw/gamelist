document.addEventListener('DOMContentLoaded', ()=>{
    let results = document.querySelector('.navResults');
    let searchBar = document.querySelector('.navInput');
    let check = 0;
    let timeout;
    searchBar.addEventListener('input', ()=>{
        clearTimeout(timeout);
        results.style.display = 'flex';
        if (searchBar.value === ''){
            results.style.display = 'none';
        }
        timeout = setTimeout(()=> {fetch(`/api/searchbar?query=${encodeURIComponent(searchBar.value)}`, {
            method: "GET",
        })
        .then(response =>{
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (check === 1){
                for (let i = 0; i<data.length; i++){
                    let elementMain = document.getElementById(`result${i}`);
                    if (elementMain){
                        elementMain.remove();
                    }
                }
            }
            console.log(data)
            for (let i = 0; i<data.length; i++){
                let newElementTitle = document.createElement('div');
                newElementTitle.setAttribute('id', `resultTitle${i}`);
                newElementTitle.setAttribute('style', 'color: white;');
                newElementTitle.innerHTML = `${data[i].name}, ${data[i].release_dates[0].y}`;
                let newElementImage = document.createElement('img');
                newElementImage.setAttribute('id', `resultImage${i}`);
                let newElementGenres= document.createElement('div');
                newElementGenres.setAttribute('id', `resultGenre${i}`);
                
                let newElementInput = document.createElement('input');
                newElementInput.setAttribute('hidden', 'true')
                newElementInput.setAttribute('name', 'query');
                newElementInput.setAttribute('value', `${data[i].id}`);
                let newElementButton = document.createElement('button');
                newElementButton.setAttribute('class', 'clickableResult')
                newElementButton.appendChild(newElementTitle);
                newElementButton.appendChild(newElementImage);
                newElementButton.appendChild(newElementGenres);
                let newElementForm = document.createElement('form');
                newElementForm.appendChild(newElementInput);
                newElementForm.appendChild(newElementButton);
                newElementForm.setAttribute('action', '/game');
                let newElementMain = document.createElement('div');
                newElementMain.setAttribute('id', `result${i}`);
                newElementMain.appendChild(newElementForm);
                results.appendChild(newElementMain)
                
                if (data[i].genres){
                    for (let j = 0; j<data[i].genres.length; j++){
                    newElementGenres.innerHTML += ` ${data[i].genres[j].name}`;
                    }
                }
                if (data[i].cover){
                    newElementImage.setAttribute('src', `//images.igdb.com/igdb/image/upload/t_thumb/${data[i].cover.image_id}.jpg`);
                    newElementImage.setAttribute
                }
            }
            check = 1;
        })
        .catch(error => {
            console.error('An error ocurred: ', error.message)
        }), 1000});
    })
});
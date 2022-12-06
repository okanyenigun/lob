const addBtns = document.querySelectorAll('#add');
const parameterContainer = document.querySelector('.parameter-list')
const dropDowns = document.querySelectorAll('SELECT')
const titleEls = document.querySelectorAll('h2')
const cardEls = document.querySelectorAll('.card-body')



dropDowns.forEach((d) =>{
    d.addEventListener('change',()=>{
        var options = d.options;
        for(var i=0; i< options.length;i++){
            options[i].removeAttribute("selected")
        }      
        d.options[d.options.selectedIndex].setAttribute("selected", "selected")
    })
})

function removeCard () {
    const closeIcons = document.querySelectorAll('.card__exit')
    closeIcons.forEach((close) =>{
        close.addEventListener('click', ()=>{
            parentCard = close.parentNode;
            var title = parentCard.childNodes[1].innerHTML;
            for(let i=0;i<titleEls.length;i++){
                if (title == titleEls[i].innerHTML){
                    cardEls[i].classList.remove('card-body-clicked')
                }
            }
            parentCard.remove();
        })
    })
}


addBtns.forEach((btn) => {

    btn.addEventListener('click', () =>{
        //up to card div
        const cardBodyDiv = btn.parentNode.parentNode;
        //title
        const title = cardBodyDiv.childNodes[1].innerHTML;
        //inputs
        els = cardBodyDiv.querySelectorAll('input,select')
        //create card
        let newDiv = document.createElement('div');
        newDiv.className = 'bucket-card-body';
        newDiv.innerHTML += `
        <p>${title}</p>
        <p class="card__exit">
          <span
            class="iconify"
            data-icon="material-symbols:cancel-rounded"
          ></span>
        </p>
        <div class="row g-3 align-items-center">
        </div>
        <div class="row">
          <div class="col-auto">
            <label class="col-form-label" for="weight">Weight:</label>
          </div>
          <div class="col-auto">
            <input
              class="form-control-sm"
              type="number"
              name="weight_${title}"
              value="25"
              id="weight-${title}"
            />
          </div>
        </div>`
        //input div
        inputDiv = newDiv.querySelector('.row.g-3')
        //append input elements into div
        for(var i=0; i < els.length; i++){
            var newNode = els[i].cloneNode(true)
            inputDiv.appendChild(newNode)
        }
        parameterContainer.appendChild(newDiv)
        removeCard()
        cardBodyDiv.classList.add('card-body-clicked')
        
    })
})
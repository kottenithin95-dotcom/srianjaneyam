const slides = document.querySelectorAll(".slide");

let current = 0;

function nextSlide(){

    slides[current].classList.remove("active");

    current++;

    if(current >= slides.length){
        current = 0;
    }

    slides[current].classList.add("active");
}

setInterval(nextSlide,5000);




const categoryBtn =
document.getElementById(
    "categoryBtn"
);

const dropdownMenu =
document.getElementById(
    "dropdownMenu"
);

categoryBtn.addEventListener(
    "click",
    function(){

        dropdownMenu.classList.toggle(
            "show"
        );

    }
);


// Close if clicked outside

document.addEventListener(
    "click",
    function(e){

        if(
            !categoryBtn.contains(e.target)
            &&
            !dropdownMenu.contains(e.target)
        ){

            dropdownMenu.classList.remove(
                "show"
            );

        }

    }
);
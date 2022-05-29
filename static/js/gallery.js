// import { getFilenames } from "./filenames.js";

// Loading animation when fetching data
window.addEventListener("load", function () {
    const loader = document.querySelector(".loader");
    loader.className += " hidden"; // class "loader hidden"
});

const gallery = document.getElementById('gallery');
const popup = document.getElementById('popup');
const selectedImage = document.getElementById('selectedImage');


$.getJSON('http://127.0.0.1:5000/archives/tuscola', function(data) {

    // Get array of filenames created in directory
    const f_names = data.filenames;
    console.log(f_names);

    f_names.forEach(i => {
        const image = document.createElement('img');
        image.src = `../../archives/tuscola/${i}`
        image.alt = `Alternate image goes here ${i}`
        image.classList.add('galleryImg');

        image.addEventListener('click', () => {
            //popup stuff
            popup.style.transform = 'translateY(0)';
            selectedImage.src = `../../archives/tuscola/${i}`
            selectedImage.alt = `Alternate image goes here ${i}`
        })
        gallery.appendChild(image);
    })
    
    popup.addEventListener('click', () => {
        popup.style.transform = 'translateY(-100%)';
        popup.src = '';
        popup.alt = '';
    })
    
});
import { getFilenames } from "./filenames.js";

const gallery = document.getElementById('gallery');
const popup = document.getElementById('popup');
const selectedImage = document.getElementById('selectedImage');
const imageIndexes = [1, 2, 3, 4];
const selectedIndex = null;

// var arr = [];

// let f_names = await getFilenames("archives", "tuscola");
// console.log("filenames: " + f_names.filenames);
// let f_names = fetch(`http://127.0.0.1:5000/archives/tuscola`)
// .then((response) => {
//     if (!response.ok) {
//         throw new Error("HTTP error " + response.status);
//     }
//     // f_names = response.json();
//     // console.log(f_names);
//     arr = response.json().filenames;
// });

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
            selectedImage.src = `../../archives/tuscola/${i}.jpg`
            selectedImage.alt = `Cover for episode ${i} of the compressed blah blah`
        })
        gallery.appendChild(image);
    })
    
    popup.addEventListener('click', () => {
        popup.style.transform = 'translateY(-100%)';
        popup.src = '';
        popup.alt = '';
    })
    
});


// console.log("f_names: " + f_names);


// imageIndexes.forEach(i => {
//     const image = document.createElement('img');
//     image.src = `../../images/image-${i}.jpg`
//     image.alt = `Alternate image goes here ${i}`
//     image.classList.add('galleryImg');

//     image.addEventListener('click', () => {
//         //popup stuff
//         popup.style.transform = 'translateY(0)';
//         selectedImage.src = `../../images/image-${i}.jpg`
//         selectedImage.alt = `Cover for episode ${i} of the compressed blah blah`
//     })
//     gallery.appendChild(image);
// })

// popup.addEventListener('click', () => {
//     popup.style.transform = 'translateY(-100%)';
//     popup.src = '';
//     popup.alt = '';
// })
const gallery = document.getElementById('gallery');
const popup = document.getElementById('popup');
const selectedImage = document.getElementById('selectedImage');
const imageIndexes = [1, 2, 3, 4];
const selectedIndex = null;

imageIndexes.forEach(i => {
    const image = document.createElement('img');
    image.src = `../../images/image-${i}.jpg`
    image.alt = `Cover for episode ${i} of the compressed blah blah`
    image.classList.add('galleryImg');

    image.addEventListener('click', () => {
        //popup stuff
        popup.style.transform = 'translateY(0)';
        selectedImage.src = `../../images/image-${i}.jpg`
        selectedImage.alt = `Cover for episode ${i} of the compressed blah blah`
    })
    gallery.appendChild(image);
})

popup.addEventListener('click', () => {
    popup.style.transform = 'translateY(-100%)';
    popup.src = '';
    popup.alt = '';
})
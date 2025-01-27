// script.js
document.addEventListener('DOMContentLoaded', function () {
    console.log('Page chargée avec succès!');
    const header = document.querySelector('header');
    header.style.cursor = 'pointer';
    header.addEventListener('click', () => {
        alert('Bienvenue dans l\'application Django!');
    });
});

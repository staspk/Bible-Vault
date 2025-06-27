const searchInput = document.querySelector('.search-input');

const urlParams = new URLSearchParams(window.location.search);
const book         = urlParams.get('book');
const chapter      = urlParams.get('chapter');
const translations = (urlParams.get('translations') ?? '').split(';').filter(translation => translation);

if (book)
    searchInput.value = book;

if (chapter)
    searchInput.value += ` ${chapter}`;


for (translation in translations) {
    
}
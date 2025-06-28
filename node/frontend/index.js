const urlParams = new URLSearchParams(window.location.search);
const searchInput = document.getElementById('search-input');


const book         = urlParams.get('book');
const chapter      = urlParams.get('chapter');
const translations = (urlParams.get('translations') ?? '').split(';').filter(translation => translation);

let searchDebounceTimerID;





Timer.start();
console.log(isValidBibleReference('3 Cor'));
Timer.stop();
console.log('%cThis is yellow text', 'color: yellow');

searchInput.addEventListener('input', (event) => {
    clearTimeout(searchDebounceTimerID);
    
    const value = event.target.value.trim();
    if (!value || !isValidBibleReference(value)) return;
    
    searchDebounceTimerID = setTimeout(async () => {
        try {
            const response = await fetch(`/api/?book=${book}&chapter=${chapter}&translations=${translations}`);
            if (!response.ok) throw new Error('Network Error');
            
            const data = await response.json();
            console.log('Search results:', data);
            
        } catch (error) {
            console.error()
        }
    }, 1250);
});

if (book && chapter)
    searchInput.value = `${book} ${chapter}`;


for (translation in translations) {
    
}
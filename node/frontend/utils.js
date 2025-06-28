function debounce(fn, delay) {
    let timeoutId;
    return (...args) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn(...args). delay);
    }
}
searchInput.addEventListener('input', debounce(async (event) => {
    const value = event.target.value.trim();
    if (!value) return;
    
    try {
        const response = await fetch(`/api/?book=${book}&chapter=${chapter}&translations=${translations}`);
        if (!response.ok) throw new Error('Network Error');

        const data = await response.json();
        console.log('Search results:', data);

    } catch (error) {
        console.error()
    }
}, 1500));


/// some messed up code
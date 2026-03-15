// grounding.js
// Extract interactive elements and their coordinates for SoM labeling.

(function() {
    const interactiveSelectors = [
        'button', 'a', 'input', 'select', 'textarea', '[role="button"]', 
        '[role="link"]', '[role="checkbox"]', '[role="menuitem"]'
    ];
    
    const elements = document.querySelectorAll(interactiveSelectors.join(','));
    const results = [];
    
    elements.forEach((el, index) => {
        const rect = el.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0 && rect.top >= 0 && rect.left >= 0) {
            results.push({
                id: index + 1,
                tag: el.tagName.toLowerCase(),
                text: el.innerText || el.placeholder || el.getAttribute('aria-label') || '',
                type: el.type || el.getAttribute('role') || 'element',
                x: rect.left + rect.width / 2,
                y: rect.top + rect.height / 2,
                width: rect.width,
                height: rect.height
            });
        }
    });
    
    return results;
})();

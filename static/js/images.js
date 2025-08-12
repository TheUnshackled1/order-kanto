// Image handling utilities for OrderKanto

document.addEventListener('DOMContentLoaded', function() {
    // Initialize image lazy loading
    initLazyLoading();
    
    // Initialize image lightbox functionality
    initImageLightbox();
    
    // Initialize image zoom on hover
    initImageZoom();
});

// Lazy loading for images
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('image-loading');
                img.classList.add('image-loaded');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => {
        img.classList.add('image-loading');
        imageObserver.observe(img);
    });
}

// Simple lightbox functionality
function initImageLightbox() {
    const images = document.querySelectorAll('.menu-item-image, .product-image');
    
    images.forEach(img => {
        img.addEventListener('click', function() {
            openLightbox(this.src, this.alt);
        });
        
        // Add cursor pointer to indicate clickable
        img.style.cursor = 'pointer';
    });
}

function openLightbox(src, alt) {
    // Create lightbox overlay
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox-overlay';
    lightbox.innerHTML = `
        <div class="lightbox-content">
            <img src="${src}" alt="${alt}" class="lightbox-image">
            <button class="lightbox-close">&times;</button>
        </div>
    `;
    
    // Add styles
    lightbox.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    `;
    
    const content = lightbox.querySelector('.lightbox-content');
    content.style.cssText = `
        position: relative;
        max-width: 90%;
        max-height: 90%;
    `;
    
    const image = lightbox.querySelector('.lightbox-image');
    image.style.cssText = `
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    `;
    
    const closeBtn = lightbox.querySelector('.lightbox-close');
    closeBtn.style.cssText = `
        position: absolute;
        top: -40px;
        right: 0;
        background: none;
        border: none;
        color: white;
        font-size: 30px;
        cursor: pointer;
        padding: 0;
        width: 30px;
        height: 30px;
    `;
    
    // Close functionality
    closeBtn.addEventListener('click', () => {
        document.body.removeChild(lightbox);
    });
    
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            document.body.removeChild(lightbox);
        }
    });
    
    // Add to page
    document.body.appendChild(lightbox);
}

// Image zoom on hover
function initImageZoom() {
    const zoomImages = document.querySelectorAll('.menu-item-image, .product-image');
    
    zoomImages.forEach(img => {
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.zIndex = '10';
        });
        
        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.zIndex = 'auto';
        });
    });
}

// Image error handling
function handleImageError(img) {
    img.src = '/static/images/icons/image-placeholder.png';
    img.alt = 'Image not available';
    img.classList.add('image-error');
}

// Add error handling to all images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            handleImageError(this);
        });
    });
});

// Utility function to preload images
function preloadImage(src) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = reject;
        img.src = src;
    });
}

// Preload critical images
function preloadCriticalImages() {
    const criticalImages = [
        '/static/images/logos/logo.png',
        '/static/images/icons/cart-icon.png',
        '/static/images/icons/user-icon.png'
    ];
    
    criticalImages.forEach(src => {
        preloadImage(src).catch(() => {
            console.warn(`Failed to preload image: ${src}`);
        });
    });
}

// Initialize preloading
document.addEventListener('DOMContentLoaded', preloadCriticalImages); 
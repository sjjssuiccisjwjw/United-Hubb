// ===== MAIN JAVASCRIPT FILE =====

// ===== CONSTANTS =====
const COPY_SUCCESS_MESSAGE = 'Código copiado!';
const COPY_ERROR_MESSAGE = 'Erro ao copiar código';
const COPY_TIMEOUT = 2000;

// ===== UTILITY FUNCTIONS =====

/**
 * Copy text to clipboard with fallback methods
 * @param {string} text - Text to copy
 * @param {HTMLElement} button - Button element that triggered the copy
 */
async function copyToClipboard(text, button) {
    try {
        // Modern clipboard API
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers or non-secure contexts
            fallbackCopyTextToClipboard(text);
        }
        
        // Update button state
        updateCopyButtonState(button, true);
        
        // Show success toast
        showToast('copyToast');
        
        // Reset button after timeout
        setTimeout(() => {
            updateCopyButtonState(button, false);
        }, COPY_TIMEOUT);
        
    } catch (err) {
        console.error('Failed to copy text: ', err);
        updateCopyButtonState(button, false);
        showErrorToast('Erro ao copiar código');
    }
}

/**
 * Fallback method for copying text to clipboard
 * @param {string} text - Text to copy
 */
function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    
    // Avoid scrolling to bottom
    textArea.style.top = '0';
    textArea.style.left = '0';
    textArea.style.position = 'fixed';
    textArea.style.opacity = '0';
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (!successful) {
            throw new Error('Fallback copy failed');
        }
    } finally {
        document.body.removeChild(textArea);
    }
}

/**
 * Update copy button visual state
 * @param {HTMLElement} button - Button element
 * @param {boolean} copied - Whether the copy was successful
 */
function updateCopyButtonState(button, copied) {
    const icon = button.querySelector('i');
    const text = button.querySelector('.btn-text') || button.childNodes[button.childNodes.length - 1];
    
    if (copied) {
        button.classList.add('copied');
        button.classList.remove('btn-outline-primary');
        button.classList.add('btn-success');
        
        if (icon) {
            icon.className = 'fas fa-check me-1';
        }
        
        if (text && text.textContent) {
            text.textContent = ' Copiado!';
        }
        
        button.disabled = true;
    } else {
        button.classList.remove('copied', 'btn-success');
        button.classList.add('btn-outline-primary');
        
        if (icon) {
            icon.className = 'fas fa-copy me-1';
        }
        
        if (text && text.textContent) {
            text.textContent = ' Copiar';
        }
        
        button.disabled = false;
    }
}

/**
 * Show Bootstrap toast
 * @param {string} toastId - ID of the toast element
 */
function showToast(toastId) {
    const toastElement = document.getElementById(toastId);
    if (toastElement) {
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: 3000
        });
        toast.show();
    }
}

/**
 * Show error toast with custom message
 * @param {string} message - Error message to display
 */
function showErrorToast(message) {
    // Create dynamic error toast
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) return;
    
    const errorToast = document.createElement('div');
    errorToast.className = 'toast';
    errorToast.setAttribute('role', 'alert');
    errorToast.innerHTML = `
        <div class="toast-header">
            <i class="fas fa-exclamation-circle text-danger me-2"></i>
            <strong class="me-auto">Erro</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    toastContainer.appendChild(errorToast);
    
    const toast = new bootstrap.Toast(errorToast, {
        autohide: true,
        delay: 4000
    });
    
    toast.show();
    
    // Remove toast element after it's hidden
    errorToast.addEventListener('hidden.bs.toast', () => {
        errorToast.remove();
    });
}

// ===== SCROLL ANIMATIONS =====

/**
 * Initialize scroll animations for elements
 */
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                // Unobserve after animation to improve performance
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe script cards
    document.querySelectorAll('.script-card').forEach((card, index) => {
        // Add staggered delay for better visual effect
        card.style.animationDelay = `${index * 0.1}s`;
        observer.observe(card);
    });

    // Observe info cards
    document.querySelectorAll('.info-card').forEach((card, index) => {
        card.style.animationDelay = `${index * 0.15}s`;
        observer.observe(card);
    });
}

// ===== SMOOTH SCROLLING =====

/**
 * Add smooth scrolling behavior to anchor links
 */
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ===== NAVBAR SCROLL EFFECT =====

/**
 * Add scroll effect to navbar
 */
function initNavbarScrollEffect() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add shadow when scrolled
        if (scrollTop > 10) {
            navbar.classList.add('shadow-sm');
        } else {
            navbar.classList.remove('shadow-sm');
        }
        
        // Hide/show navbar on scroll (optional)
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    }, { passive: true });
    
    // Add transition for smooth hide/show
    navbar.style.transition = 'transform 0.3s ease-in-out, box-shadow 0.3s ease';
}

// ===== KEYBOARD SHORTCUTS =====

/**
 * Initialize keyboard shortcuts
 */
function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K to focus search (if implemented)
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals/toasts
        if (e.key === 'Escape') {
            // Close all visible toasts
            document.querySelectorAll('.toast.show').forEach(toast => {
                bootstrap.Toast.getInstance(toast)?.hide();
            });
        }
    });
}

// ===== PERFORMANCE OPTIMIZATIONS =====

/**
 * Lazy load images with Intersection Observer
 */
function initLazyLoading() {
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ===== INITIALIZATION =====

/**
 * Initialize all functionality when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize core functionality
    initScrollAnimations();
    initSmoothScrolling();
    initNavbarScrollEffect();
    initKeyboardShortcuts();
    initLazyLoading();
    
    // Add loading state management
    document.body.classList.add('loaded');
    
    // Initialize tooltips if Bootstrap tooltips are used
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers if Bootstrap popovers are used
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    console.log('MeepCity Scripts Hub initialized successfully');
});

// ===== ERROR HANDLING =====

/**
 * Global error handler
 */
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    // In production, you might want to send this to a logging service
});

/**
 * Unhandled promise rejection handler
 */
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    e.preventDefault();
});

// ===== EXPORT FOR GLOBAL ACCESS =====
window.MeepCityScripts = {
    copyToClipboard,
    showToast,
    showErrorToast
};

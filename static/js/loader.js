
/**
 * Advanced Loader System for प्रांतीय युवा प्रकोष्ठ
 * Real-time loading states and beautiful animations
 */

class LoaderManager {
    constructor() {
        this.currentLoader = null;
        this.loadingStates = new Map();
        this.init();
    }

    init() {
        this.createPageLoader();
        this.setupFormLoaders();
        this.setupAjaxLoaders();
        this.setupImageLoaders();
        this.bindEvents();
        
        console.log('Loader Manager initialized');
    }

    // Create main page loader
    createPageLoader() {
        if (document.querySelector('.page-loader')) return;

        const loader = document.createElement('div');
        loader.className = 'page-loader';
        loader.innerHTML = `
            <div class="loader-container">
                <div class="logo-loader">
                    <img src="/static/images/logo.svg" alt="Loading">
                </div>
                <div class="spinner spinner-dual-ring"></div>
                <div class="loader-text">प्रांतीय युवा प्रकोष्ठ</div>
                <div class="loader-subtitle">कृपया प्रतीक्षा करें...</div>
                <div class="progress-bar-container">
                    <div class="progress-bar-fill" id="main-progress"></div>
                </div>
            </div>
        `;
        
        document.body.appendChild(loader);
        this.currentLoader = loader;
        
        // Auto-hide page loader when page is fully loaded
        if (document.readyState === 'loading') {
            this.showPageLoader();
            window.addEventListener('load', () => {
                setTimeout(() => this.hidePageLoader(), 500);
            });
        }
    }

    // Show page loader
    showPageLoader(message = 'लोड हो रहा है...') {
        const loader = document.querySelector('.page-loader');
        if (loader) {
            const subtitle = loader.querySelector('.loader-subtitle');
            if (subtitle) subtitle.textContent = message;
            
            loader.classList.remove('fade-out');
            loader.style.display = 'flex';
            document.body.style.overflow = 'hidden';
            
            this.animateProgress();
        }
    }

    // Hide page loader
    hidePageLoader() {
        const loader = document.querySelector('.page-loader');
        if (loader) {
            loader.classList.add('fade-out');
            document.body.style.overflow = '';
            
            setTimeout(() => {
                loader.style.display = 'none';
            }, 500);
        }
    }

    // Animate progress bar
    animateProgress() {
        const progressBar = document.getElementById('main-progress');
        if (!progressBar) return;

        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            
            progressBar.style.width = progress + '%';
            
            if (progress >= 90) {
                clearInterval(interval);
            }
        }, 100);
    }

    // Setup form loaders
    setupFormLoaders() {
        document.addEventListener('submit', (e) => {
            const form = e.target;
            if (form.tagName === 'FORM') {
                this.showFormLoader(form);
            }
        });
    }

    // Show form loader
    showFormLoader(form) {
        const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
        if (submitBtn) {
            const originalText = submitBtn.innerHTML || submitBtn.value;
            submitBtn.classList.add('btn-loading');
            
            if (submitBtn.tagName === 'BUTTON') {
                submitBtn.innerHTML = `
                    <span class="mini-loader"></span>
                    सबमिट हो रहा है...
                `;
            } else {
                submitBtn.value = 'सबमिट हो रहा है...';
            }
            
            submitBtn.disabled = true;
            
            // Store original state
            this.loadingStates.set(submitBtn, {
                originalText,
                originalDisabled: submitBtn.disabled
            });
        }
    }

    // Hide form loader
    hideFormLoader(form) {
        const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
        if (submitBtn && this.loadingStates.has(submitBtn)) {
            const state = this.loadingStates.get(submitBtn);
            
            submitBtn.classList.remove('btn-loading');
            submitBtn.disabled = state.originalDisabled;
            
            if (submitBtn.tagName === 'BUTTON') {
                submitBtn.innerHTML = state.originalText;
            } else {
                submitBtn.value = state.originalText;
            }
            
            this.loadingStates.delete(submitBtn);
        }
    }

    // Setup AJAX loaders
    setupAjaxLoaders() {
        // Override fetch to show loaders
        const originalFetch = window.fetch;
        window.fetch = (...args) => {
            this.showAjaxLoader();
            return originalFetch(...args)
                .finally(() => {
                    setTimeout(() => this.hideAjaxLoader(), 300);
                });
        };

        // Override XMLHttpRequest
        const originalXHR = window.XMLHttpRequest;
        window.XMLHttpRequest = function() {
            const xhr = new originalXHR();
            const originalSend = xhr.send;
            
            xhr.send = function(...args) {
                window.loaderManager.showAjaxLoader();
                
                xhr.addEventListener('loadend', () => {
                    setTimeout(() => window.loaderManager.hideAjaxLoader(), 300);
                });
                
                return originalSend.apply(this, args);
            };
            
            return xhr;
        };
    }

    // Show AJAX loader
    showAjaxLoader() {
        if (!document.querySelector('.ajax-loader')) {
            const loader = document.createElement('div');
            loader.className = 'ajax-loader';
            loader.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #fd8535, #ffb300);
                z-index: 9998;
                animation: progressFlow 1s ease-in-out infinite;
            `;
            document.body.appendChild(loader);
        }
    }

    // Hide AJAX loader
    hideAjaxLoader() {
        const loader = document.querySelector('.ajax-loader');
        if (loader) {
            loader.style.opacity = '0';
            setTimeout(() => loader.remove(), 300);
        }
    }

    // Setup image loaders
    setupImageLoaders() {
        const images = document.querySelectorAll('img[data-src]');
        images.forEach(img => this.addImageLoader(img));
    }

    // Add loader to image
    addImageLoader(img) {
        const wrapper = document.createElement('div');
        wrapper.className = 'image-loader-wrapper';
        wrapper.style.cssText = `
            position: relative;
            display: inline-block;
            background: #f0f0f0;
        `;

        const loader = document.createElement('div');
        loader.className = 'image-loader';
        loader.innerHTML = `
            <div class="spinner spinner-ring"></div>
        `;
        loader.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1;
        `;

        img.parentNode.insertBefore(wrapper, img);
        wrapper.appendChild(img);
        wrapper.appendChild(loader);

        img.addEventListener('load', () => {
            loader.style.opacity = '0';
            setTimeout(() => loader.remove(), 300);
        });

        img.addEventListener('error', () => {
            loader.innerHTML = '<span style="color: #dc3545;">❌</span>';
        });
    }

    // Show skeleton loader
    showSkeletonLoader(container, type = 'card') {
        if (!container) return;

        let skeletonHTML = '';
        
        switch (type) {
            case 'card':
                skeletonHTML = `
                    <div class="skeleton skeleton-card"></div>
                    <div class="skeleton skeleton-text" style="margin-top: 1rem;"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text"></div>
                `;
                break;
            case 'list':
                skeletonHTML = `
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <div class="skeleton skeleton-avatar" style="margin-right: 1rem;"></div>
                        <div style="flex: 1;">
                            <div class="skeleton skeleton-text"></div>
                            <div class="skeleton skeleton-text"></div>
                        </div>
                    </div>
                `.repeat(3);
                break;
            case 'text':
                skeletonHTML = `
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text" style="width: 60%;"></div>
                `;
                break;
        }

        const skeletonWrapper = document.createElement('div');
        skeletonWrapper.className = 'skeleton-wrapper';
        skeletonWrapper.innerHTML = skeletonHTML;
        
        container.appendChild(skeletonWrapper);
        return skeletonWrapper;
    }

    // Hide skeleton loader
    hideSkeletonLoader(container) {
        const skeleton = container.querySelector('.skeleton-wrapper');
        if (skeleton) {
            skeleton.style.opacity = '0';
            setTimeout(() => skeleton.remove(), 300);
        }
    }

    // Show custom loader
    showCustomLoader(options = {}) {
        const {
            container = document.body,
            type = 'spinner',
            message = 'लोड हो रहा है...',
            overlay = true
        } = options;

        const loaderId = 'custom-loader-' + Date.now();
        
        let loaderHTML = '';
        
        switch (type) {
            case 'dots':
                loaderHTML = `
                    <div class="spinner spinner-dots">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                `;
                break;
            case 'wave':
                loaderHTML = `
                    <div class="spinner spinner-wave">
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                    </div>
                `;
                break;
            case 'pulse':
                loaderHTML = `<div class="spinner spinner-pulse"></div>`;
                break;
            case 'progress':
                loaderHTML = `
                    <div class="spinner spinner-progress">
                        <svg width="60" height="60">
                            <circle class="bg-circle" cx="30" cy="30" r="28"></circle>
                            <circle class="progress-circle" cx="30" cy="30" r="28"></circle>
                        </svg>
                    </div>
                `;
                break;
            default:
                loaderHTML = `<div class="spinner spinner-ring"></div>`;
        }

        const loader = document.createElement('div');
        loader.id = loaderId;
        loader.className = `custom-loader ${overlay ? 'overlay' : ''}`;
        loader.innerHTML = `
            <div class="loader-container">
                ${loaderHTML}
                <div class="loader-text">${message}</div>
            </div>
        `;

        if (overlay) {
            loader.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: rgba(255, 248, 225, 0.9);
                backdrop-filter: blur(5px);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 9997;
            `;
        }

        container.appendChild(loader);
        return loaderId;
    }

    // Hide custom loader
    hideCustomLoader(loaderId) {
        const loader = document.getElementById(loaderId);
        if (loader) {
            loader.style.opacity = '0';
            setTimeout(() => loader.remove(), 300);
        }
    }

    // Bind events
    bindEvents() {
        // Show loader on page navigation
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            if (link && !link.getAttribute('href').startsWith('#') && 
                !link.hasAttribute('download') && 
                !link.getAttribute('href').startsWith('mailto:') &&
                !link.getAttribute('href').startsWith('tel:')) {
                
                setTimeout(() => {
                    this.showPageLoader('पृष्ठ लोड हो रहा है...');
                }, 100);
            }
        });

        // Hide loaders on page visibility change
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                this.hidePageLoader();
            }
        });
    }

    // Utility methods
    showButtonLoader(button, text = 'लोड हो रहा है...') {
        if (!button) return;

        const originalText = button.innerHTML;
        button.classList.add('btn-loading');
        button.innerHTML = `<span class="mini-loader"></span>${text}`;
        button.disabled = true;

        this.loadingStates.set(button, { originalText, originalDisabled: button.disabled });
    }

    hideButtonLoader(button) {
        if (!button || !this.loadingStates.has(button)) return;

        const state = this.loadingStates.get(button);
        button.classList.remove('btn-loading');
        button.innerHTML = state.originalText;
        button.disabled = state.originalDisabled;
        this.loadingStates.delete(button);
    }

    showInputLoader(input) {
        if (!input) return;
        input.classList.add('input-loading');
    }

    hideInputLoader(input) {
        if (!input) return;
        input.classList.remove('input-loading');
    }
}

// Initialize loader manager
document.addEventListener('DOMContentLoaded', () => {
    window.loaderManager = new LoaderManager();
});

// Utility functions for global use
window.showLoader = (options) => window.loaderManager?.showCustomLoader(options);
window.hideLoader = (loaderId) => window.loaderManager?.hideCustomLoader(loaderId);
window.showPageLoader = (message) => window.loaderManager?.showPageLoader(message);
window.hidePageLoader = () => window.loaderManager?.hidePageLoader();

document.addEventListener('DOMContentLoaded', () => {
    // Load Header and Footer dynamically
    Promise.all([
        fetch('header.html').then(res => res.text()).then(data => {
            document.getElementById('header-placeholder').innerHTML = data;
        }),
        fetch('footer.html').then(res => res.text()).then(data => {
            document.getElementById('footer-placeholder').innerHTML = data;
        })
    ]).then(() => {
        // ELYFiC Modal Logic
        const elyficModal = document.getElementById('elyfic-modal');
        const elyficClose = document.getElementById('elyfic-close');
        const elyficOverlay = document.querySelector('.elyfic-modal__overlay');
        
        if (elyficModal) {
            const closeModal = () => {
                elyficModal.classList.remove('is-active');
            };
            
            if (elyficClose) elyficClose.addEventListener('click', closeModal);
            if (elyficOverlay) elyficOverlay.addEventListener('click', closeModal);
        }

        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                
                // Show ELYFiC Modal for CTA buttons and footer links
                if (targetId === '#join' || this.closest('.footer__links')) {
                    const elyficModal = document.getElementById('elyfic-modal');
                    if (elyficModal) {
                        elyficModal.classList.add('is-active');
                    }
                    return;
                }

                if(targetId === '#') return;
                
                const targetElement = document.querySelector(targetId);
                if(targetElement) {
                    // Offset for fixed header
                    const header = document.querySelector('.header');
                    const headerHeight = header ? header.offsetHeight : 0;
                    const elementPosition = targetElement.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerHeight;
      
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });

        // Add scroll effect to header
        const header = document.querySelector('.header');
        if (header) {
            window.addEventListener('scroll', () => {
                if (window.scrollY > 50) {
                    header.style.backgroundColor = 'rgba(17, 17, 17, 0.95)';
                    header.style.boxShadow = '0 4px 10px rgba(0, 0, 0, 0.5)';
                } else {
                    header.style.backgroundColor = 'rgba(17, 17, 17, 0.8)';
                    header.style.boxShadow = 'none';
                }
            });
        }

        // Simple scroll reveal animation for elements
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.15
        };

        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Apply animation to sections and cards
        const elementsToAnimate = document.querySelectorAll('.concept__content, .concept__image, .feature-card, .price-card, .case-card, .location-card');
        
        elementsToAnimate.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });

        // Impactful animation for solutions title
        const titleObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-impact');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        const solutionsTitle = document.querySelector('.solutions__title');
        if (solutionsTitle) {
            titleObserver.observe(solutionsTitle);
        }

        // Show sticky CTA after solutions section
        const solutionsSection = document.querySelector('.solutions');
        const stickyCta = document.getElementById('sticky-cta');
        
        if (solutionsSection && stickyCta) {
            const ctaObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    // Show when solutions section is on screen OR user has scrolled past it
                    if (entry.isIntersecting || entry.boundingClientRect.top < 0) {
                        stickyCta.classList.add('is-visible');
                    } else {
                        stickyCta.classList.remove('is-visible');
                    }
                });
            }, {
                root: null,
                threshold: 0
            });
            
            ctaObserver.observe(solutionsSection);
        }
    });
});

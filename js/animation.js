/* ==========================================================================
   animation orchestrator - scroll reveals & premium effects
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  
  // 1. Scroll Reveal Observer
  const revealElements = document.querySelectorAll('.reveal');
  
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        // Stop observing once animated
        observer.unobserve(entry.target);
      }
    });
  }, {
    root: null,
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px' // Trigger slightly before element is in full view
  });

  revealElements.forEach(element => {
    revealObserver.observe(element);
  });

  // 2. Skill Progress Bars Observer
  const skillProgressFills = document.querySelectorAll('.skill-progress-fill');
  
  const progressObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const fill = entry.target;
        const progressWidth = fill.getAttribute('data-progress');
        fill.style.setProperty('--progress-width', progressWidth);
        fill.style.width = progressWidth;
        fill.classList.add('progress-active');
      }
    });
  }, {
    root: null,
    threshold: 0.1
  });

  skillProgressFills.forEach(fill => {
    progressObserver.observe(fill);
  });

  // 3. Stats Counter Trigger Observer
  const statsSection = document.querySelector('.stats');
  if (statsSection) {
    const statsObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          if (typeof window.animateCounters === 'function') {
            window.animateCounters();
          }
          observer.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      threshold: 0.3
    });
    statsObserver.observe(statsSection);
  }

  // 4. Scroll Spy Navbar Highlight
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  const scrollSpyObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navLinks.forEach(link => {
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          } else {
            link.classList.remove('active');
          }
        });
      }
    });
  }, {
    root: null,
    threshold: 0.4, // Highlight link when 40% of section is visible
    rootMargin: '-10% 0px -50% 0px'
  });

  sections.forEach(section => {
    scrollSpyObserver.observe(section);
  });

  // 5. Interactive Cursor Spotlight Hover Effect (Stripe/Apple Card style)
  const spotlightCards = document.querySelectorAll(
    '.project-card, .skill-category-card, .service-card, .edu-card, .about-profile-card'
  );

  spotlightCards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      // Calculate coordinates relative to card
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    });
  });
});

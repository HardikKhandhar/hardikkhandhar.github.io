/* ==========================================================================
   primary portfolio logic - hardik khandhar
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // Calculate dynamic years of experience (started 1 May 2017)
  const startDate = new Date('2017-05-01');
  const diffYears = (Date.now() - startDate.getTime()) / (365.25 * 24 * 60 * 60 * 1000);
  const formattedYears = diffYears.toFixed(1); // e.g., "9.2"
  const yearsInt = Math.floor(diffYears);       // e.g., 9

  // Update experience count-up target
  const experienceCounter = document.getElementById('experience-counter');
  if (experienceCounter) {
    experienceCounter.setAttribute('data-target', formattedYears);
  }

  // Update references to experience years in text
  const dynamicExperienceTexts = document.querySelectorAll('.dynamic-experience-years');
  dynamicExperienceTexts.forEach(el => {
    el.textContent = yearsInt;
  });

  // 1. Preloader
  const preloader = document.querySelector('.preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.style.opacity = '0';
      setTimeout(() => {
        preloader.style.display = 'none';
      }, 600);
    });
  }

  // 2. Mobile Menu Toggle
  const hamburger = document.querySelector('.hamburger');
  const navMenu = document.querySelector('.nav-menu');
  const navLinks = document.querySelectorAll('.nav-link');

  const toggleMenu = () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
  };

  const closeMenu = () => {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
  };

  hamburger.addEventListener('click', toggleMenu);
  navLinks.forEach(link => link.addEventListener('click', closeMenu));

  // 3. Sticky Navbar & Scroll Progress
  const navbar = document.querySelector('.navbar');
  const scrollProgressBar = document.querySelector('.scroll-progress-bar');
  const backToTopBtn = document.querySelector('.back-to-top');

  const handleScroll = () => {
    const scrollY = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    
    // Scroll progress bar
    if (docHeight > 0 && scrollProgressBar) {
      const scrollPercent = (scrollY / docHeight) * 100;
      scrollProgressBar.style.width = `${scrollPercent}%`;
    }

    // Sticky Nav class
    if (scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    // Back to top button show/hide
    if (scrollY > 600) {
      backToTopBtn.classList.add('active');
    } else {
      backToTopBtn.classList.remove('active');
    }
  };

  window.addEventListener('scroll', handleScroll);
  handleScroll(); // Initial check on load

  // Back to Top Click
  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // 4. Hero Section Role Typing Animation
  const typeTarget = document.querySelector('.hero-typing');
  if (typeTarget) {
    const phrases = [
      'Node.js • Laravel • React • AI Solutions',
      'Senior Full Stack Developer',
      'REST API & Backend Specialist',
      'AI-Powered Solutions Creator'
    ];
    let phraseIdx = 0;
    let charIdx = 0;
    let isDeleting = false;
    let typeSpeed = 100;

    const typeAnimation = () => {
      const currentPhrase = phrases[phraseIdx];
      
      if (isDeleting) {
        typeTarget.textContent = currentPhrase.substring(0, charIdx - 1);
        charIdx--;
        typeSpeed = 40; // Erase faster
      } else {
        typeTarget.textContent = currentPhrase.substring(0, charIdx + 1);
        charIdx++;
        typeSpeed = 100; // Type standard speed
      }

      if (!isDeleting && charIdx === currentPhrase.length) {
        isDeleting = true;
        typeSpeed = 2000; // Wait 2 seconds before erasing
      } else if (isDeleting && charIdx === 0) {
        isDeleting = false;
        phraseIdx = (phraseIdx + 1) % phrases.length;
        typeSpeed = 500; // Wait 0.5s before typing next
      }

      setTimeout(typeAnimation, typeSpeed);
    };

    // Start typing after initial delay
    setTimeout(typeAnimation, 1000);
  }


});

// 6. Global Stats Counter Increment (called from IntersectionObserver in animation.js)
window.animateCounters = () => {
  const counters = document.querySelectorAll('.count-up');
  counters.forEach(counter => {
    // Prevent duplicate counting
    if (counter.classList.contains('counted')) return;
    counter.classList.add('counted');

    const targetVal = counter.getAttribute('data-target');
    const target = parseFloat(targetVal);
    const isFloat = targetVal.includes('.');
    const duration = 2000; // Duration of animation in ms
    const frameRate = 1000 / 60; // 60 FPS
    const totalFrames = Math.round(duration / frameRate);
    let frame = 0;

    const countTo = () => {
      frame++;
      const progress = frame / totalFrames;
      // Easing function: easeOutQuad
      const easedProgress = progress * (2 - progress);
      const currentVal = target * easedProgress;

      if (frame < totalFrames) {
        counter.textContent = isFloat ? currentVal.toFixed(1) : Math.round(currentVal);
        requestAnimationFrame(countTo);
      } else {
        counter.textContent = isFloat ? target.toFixed(1) : target;
      }
    };

    requestAnimationFrame(countTo);
  });
};

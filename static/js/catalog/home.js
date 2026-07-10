document.addEventListener('DOMContentLoaded', function() {
    const track = document.getElementById('carouselTrack');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    if (track && prevBtn && nextBtn) {
        let currentIndex = 0;
        const slides = track.children;
        const totalSlides = slides.length;
        const slidesPerView = 4;
        
        function updateCarousel() {
            const slideWidth = 100 / slidesPerView;
            const translateX = -(currentIndex * slideWidth);
            track.style.transform = `translateX(${translateX}%)`;
            
            // Disable buttons at boundaries
            prevBtn.disabled = currentIndex === 0;
            nextBtn.disabled = currentIndex >= totalSlides - slidesPerView;
        }
        
        prevBtn.addEventListener('click', function() {
            if (currentIndex > 0) {
                currentIndex--;
                updateCarousel();
            }
        });
        
        nextBtn.addEventListener('click', function() {
            if (currentIndex < totalSlides - slidesPerView) {
                currentIndex++;
                updateCarousel();
            }
        });
        
        // Initial state
        updateCarousel();
    }
});

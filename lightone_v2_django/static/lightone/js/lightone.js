document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.metric-card,.panel-card,.report-card,.strategy-list article,.roadmap-grid div');
  cards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(12px)';
    setTimeout(() => {
      card.style.transition = 'opacity .45s ease, transform .45s ease, box-shadow .2s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 60 + index * 35);
  });
});

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".cat-toggle").forEach(function (toggle) {
    toggle.addEventListener("click", function (e) {
      e.preventDefault();
      const children = this.nextElementSibling;
      const arrow = this.querySelector(".arrow-icon");
      if (children.style.display === "none") {
        children.style.display = "block";
        arrow.style.transform = "rotate(90deg)";
      } else {
        children.style.display = "none";
        arrow.style.transform = "rotate(0deg)";
      }
    });
  });
});

const observer = new MutationObserver(() => {
  document.querySelectorAll('#search-results article').forEach(article => {
    if (article.dataset.styled) return;
    article.dataset.styled = true;

    Object.assign(article.style, {
      borderRadius: '14px',
      background: '#fff8f0',
      border: '0.5px solid #f0dcc8',
      padding: '18px 22px',
      marginBottom: '12px',
      width: '100%',
      transition: 'all 0.2s ease',
      display: 'block'
    });

    const a = article.querySelector('h2 a');
    if (a) Object.assign(a.style, {
      color: '#5a3e2b',
      fontWeight: '700',
      fontSize: '1rem'
    });

    const meta = article.querySelector('.post-meta');
    if (meta) Object.assign(meta.style, {
      fontSize: '0.78rem',
      color: '#c9a882',
      marginBottom: '8px',
      display: 'flex',
      gap: '8px'
    });

    const p = article.querySelector('p');
    if (p) Object.assign(p.style, {
      fontSize: '0.85rem',
      color: '#a0846a',
      lineHeight: '1.6',
      overflow: 'hidden',
      display: '-webkit-box',
      webkitLineClamp: '2',
      webkitBoxOrient: 'vertical'
    });

    article.addEventListener('mouseenter', () => {
      article.style.background = '#fff0e0';
      article.style.transform = 'translateY(-2px)';
    });
    article.addEventListener('mouseleave', () => {
      article.style.background = '#fff8f0';
      article.style.transform = 'none';
    });
  });
});

observer.observe(document.body, { childList: true, subtree: true });

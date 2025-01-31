function navigate() {
  if (location.hash.startsWith('#modal-') || location.hash.startsWith('#detail-')) {
    document.querySelectorAll('.modal').forEach(modal => modal.classList.remove('active'));
    const modal = document.querySelector(location.hash);
    modal.classList.add('active');
    window.scrollTo(0, 0);
  }
  else {
    if (location.hash === '') {
      document.querySelectorAll('.modal').forEach(modal => modal.classList.remove('active'));
    }
  }
}

window.addEventListener("load", navigate);
window.addEventListener("hashchange", navigate);

document.onkeyup = function(event) {
  if (event.key === 'Escape') {
    if (location.hash.startsWith('#detail-')) {
      window.location.hash = '#modal-projects';
    }
    else {
      window.location.hash = '#';
    }
  }
}

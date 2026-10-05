'use strict';
document.documentElement.classList.add('js');
const menu = document.querySelector('.menu-toggle');
const navigation = document.getElementById('primary-navigation');
const mobile = window.matchMedia('(max-width: 860px)');

function updateNavigation() {
  const isExpanded = menu.getAttribute('aria-expanded') === 'true';
  navigation.hidden = mobile.matches && !isExpanded;
}

menu.addEventListener('click', () => {
  const wasExpanded = menu.getAttribute('aria-expanded') === 'true';
  menu.setAttribute('aria-expanded', String(!wasExpanded));
  /* Update the button label to reflect state */
  menu.innerHTML = !wasExpanded
    ? 'Close <span aria-hidden="true">✕</span>'
    : 'Menu <span aria-hidden="true">☰</span>';
  updateNavigation();
});

mobile.addEventListener('change', () => {
  /* Reset menu state on breakpoint change */
  menu.setAttribute('aria-expanded', 'false');
  menu.innerHTML = 'Menu <span aria-hidden="true">☰</span>';
  updateNavigation();
});

navigation.addEventListener('keydown', event => {
  if (event.key === 'Escape' && mobile.matches) {
    menu.setAttribute('aria-expanded', 'false');
    menu.innerHTML = 'Menu <span aria-hidden="true">☰</span>';
    updateNavigation();
    menu.focus();
  }
});

updateNavigation();

for (const button of document.querySelectorAll('.copy-button')) {
  button.addEventListener('click', async () => {
    const text = button.closest('.code-block').querySelector('code').textContent;
    const status = document.getElementById('copy-status');
    try {
      await navigator.clipboard.writeText(text);
      button.textContent = 'Copied';
      status.textContent = 'Command copied to clipboard.';
      /* Reset button text after a short delay */
      setTimeout(() => { button.textContent = 'Copy'; }, 2000);
    } catch {
      status.textContent = 'Clipboard unavailable. Select and copy the displayed text.';
    }
  });
}

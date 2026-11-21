const desktopGroups = [...document.querySelectorAll('.nav-group')];

for (const group of desktopGroups) {
  group.addEventListener('toggle', () => {
    if (!group.open) return;
    for (const other of desktopGroups) {
      if (other !== group) other.open = false;
    }
  });
  group.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape' || !group.open) return;
    group.open = false;
    group.querySelector('summary').focus();
  });
}

document.addEventListener('click', (event) => {
  for (const group of desktopGroups) {
    if (!group.contains(event.target)) group.open = false;
  }
});

const menu = document.getElementById('mobile-menu');
const menuButton = document.querySelector('[aria-controls="mobile-menu"]');
menuButton.addEventListener('click', () => {
  menu.showModal();
  menuButton.setAttribute('aria-expanded', 'true');
});
menu.addEventListener('click', (event) => {
  if (event.target !== menu) return;
  const bounds = menu.getBoundingClientRect();
  if (event.clientY < bounds.top) menu.close();
});
menu.addEventListener('close', () => {
  menuButton.setAttribute('aria-expanded', 'false');
  if (menuButton.getClientRects().length) menuButton.focus();
});
const desktopViewport = matchMedia('(min-width: 821px)');
desktopViewport.addEventListener('change', () => {
  if (desktopViewport.matches && menu.open) menu.close();
});

for (const form of document.querySelectorAll('.draft-form')) {
  form.querySelector('button[type="submit"]').disabled = false;
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const fields = new FormData(form);
    const name = [fields.get('first-name'), fields.get('last-name')].join(' ');
    fields.delete('first-name');
    fields.delete('last-name');
    const subject = String(fields.get('Subject') || form.dataset.draftSubject).trim();
    const lines = [...fields].map(([label, value]) => `${label}: ${String(value).trim()}`);
    const body = [`Name: ${name.trim()}`, ...lines].join('\r\n\r\n');
    const recipient = form.dataset.recipient;
    const draft = `mailto:${recipient}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    const status = form.querySelector('[role="status"]');
    status.textContent = 'If your email app did not open, use the official online form.';
    window.location.href = draft;
  });
}

const imageLinks = [...document.querySelectorAll('.gallery a')].filter((link) =>
  link.querySelector('img') && /\.(avif|gif|jpe?g|png|webp)(\?|$)/i.test(link.getAttribute('href'))
);
if (imageLinks.length && typeof HTMLDialogElement !== 'undefined') {
  const viewer = document.createElement('dialog');
  viewer.className = 'photo-viewer';
  viewer.setAttribute('aria-label', 'Property photography');
  const closeForm = document.createElement('form');
  closeForm.method = 'dialog';
  const close = document.createElement('button');
  close.type = 'submit';
  close.className = 'close-menu';
  close.setAttribute('aria-label', 'Close photograph');
  close.textContent = '×';
  closeForm.append(close);
  const photo = document.createElement('img');
  viewer.append(closeForm, photo);
  document.body.append(viewer);

  let opener;
  for (const link of imageLinks) {
    link.addEventListener('click', (event) => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || viewer.open) return;
      event.preventDefault();
      opener = link;
      photo.alt = link.querySelector('img').alt;
      photo.src = link.href;
      viewer.showModal();
    });
  }
  viewer.addEventListener('click', (event) => {
    if (event.target === viewer) viewer.close();
  });
  viewer.addEventListener('close', () => opener?.focus());
}

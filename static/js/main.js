// Highlight incomplete selects on form submit attempt
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('assessment-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    let valid = true;
    form.querySelectorAll('select[required]').forEach(sel => {
      const group = sel.closest('.field-group');
      if (!sel.value) {
        valid = false;
        group?.classList.add('field-error');
      } else {
        group?.classList.remove('field-error');
      }
    });

    if (!valid) {
      e.preventDefault();
      const firstError = form.querySelector('.field-error');
      firstError?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  });

  // Live clear error state when user selects a value
  form.querySelectorAll('select').forEach(sel => {
    sel.addEventListener('change', () => {
      if (sel.value) sel.closest('.field-group')?.classList.remove('field-error');
    });
  });
});

document.querySelectorAll('[data-copy]').forEach(button => {
  button.addEventListener('click', async () => {
    const field = document.getElementById(button.dataset.copy);
    const status = document.getElementById('copy-status');
    const label = button.textContent;
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(field.value);
      } else {
        field.focus();
        field.select();
        if (!document.execCommand('copy')) throw new Error('Copy was blocked');
      }
      button.textContent = 'Copied';
      status.textContent = `${label.replace(/^Copy /, '')} copied to clipboard.`;
      window.setTimeout(() => { button.textContent = label; }, 1800);
    } catch {
      field.focus();
      field.select();
      status.textContent = 'Copy was blocked. The text is selected; press Command C or Control C.';
    }
  });
});

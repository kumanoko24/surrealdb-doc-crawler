() =>
  Array.from(document.querySelectorAll('a[href]'))
    .map(a => a.getAttribute('href'))

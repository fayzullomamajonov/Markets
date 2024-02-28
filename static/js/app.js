// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();

  let alertWrappers = document.querySelectorAll('.alert');
  let alertCloses = document.querySelectorAll('.alert__close');

  if (alertWrappers.length > 0) {
    alertCloses.forEach((alertClose, index) => {
      alertClose.addEventListener('click', () => {
        alertWrappers[index].style.display = 'none';
      });

      setTimeout(() => {
        alertWrappers[index].style.display = 'none';
      }, 3000);
    });
  }
});



  
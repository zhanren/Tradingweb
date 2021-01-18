console.log('Begin...');

let interval = setInterval(function () {
  if (document.readyState === 'complete') {
    clearInterval(interval);
    const h1=document.querySelector('#title');
    console.log(h1);
  }
}, 100);
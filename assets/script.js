let count=0;

let interval = setInterval(function () {
  if (document.readyState === 'complete' && count===0) {
    const html_header=`
        <nav class="social">
            <ul>
                <li><a href="https://www.linkedin.com/in/ellen-xiao/">
                    <i class="fab fa-linkedin-in"></i><span>linkedIn</span>
                </a></li>
                <li><a href="https://github.com/ellenxxiao/">
                    <i class="fab fa-github"></i><span>Github</span>
                </a></li>
                <li><a href="https://www.instagram.com/ellen_xxiao/">
                    <i class="fab fa-facebook-f"></i><span>Facebook</span>
                </a></li>
            </ul>
        </nav>
        <header class="header">
          <nav class="nav">
            <a class="nav__logo btn--show-modal" href="#">LET'S MAKE MONEY TOGETHER!</a>
            <ul class="nav__links">
                <li class="nav__item">
                    <a class="nav__link active__link" href="#">POSITION</a>
                </li>
                <li class="nav__item">
                    <a class="nav__link" href="#">PORTFOLIO</a>
                </li>
                <li class="nav__item">
                    <a class="nav__link smooth" href="#">VISION</a>
                </li>
                <li class="nav__item">
                    <a class="nav__link" href="#">CONTACT</a>
                </li>
            </ul>
        </nav>
      </header>
    `;
    let h1=document.getElementById('title');
    h1.insertAdjacentHTML("beforebegin",html_header);
    //h1.style.opacity=0;

    // Change title
    h1.innerHTML="Hey! This is my portfolio performance!";
    clearInterval(interval);
    count=1;
  }
}, 100);
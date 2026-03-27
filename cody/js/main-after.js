function create_tonk() {
    const tonk = document.createElement("img");
    tonk.classList.add("tonk");
    tonk.src = "/img/tonk.png"
    document.body.appendChild(tonk)

    let xSpeed = Math.random() / 2 + 0.5;
    let ySpeed = Math.random() / 2 + 0.5;
    let x = 0;
    let y = 0;

    const tonk_bonk = new Audio();
    tonk_bonk.src = Math.random() > .5 ? "/audio/1.wav" : "/audio/2.wav";

    function move_tonk() {
        tonk.style.left = x * 0.85 + 'vw';
        tonk.style.top = y * 0.85 + 'vh';
        x += xSpeed;
        y += ySpeed;

        if (x > 100) {
            x = 100;
            xSpeed *= -1;
            tonk_bonk.play();
        }
        if (x < 0) {
            x = 0;
            xSpeed *= -1;
            tonk_bonk.play();
        }

        if (y > 100) {
            y = 100;
            ySpeed *= -1;
            tonk_bonk.play();
        }
        if (y < 0) {
            y = 0;
            ySpeed *= -1;
            tonk_bonk.play();
        }

        requestAnimationFrame(move_tonk)
    }

    requestAnimationFrame(move_tonk)
}

for (let i = 0; i < 1; i++) {
    create_tonk();
}
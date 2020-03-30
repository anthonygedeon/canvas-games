
const canvas = document.createElement('canvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

canvas.id = 'canvas';
canvas.style.backgroundColor = "#000";
document.body.appendChild(canvas)

const ctx = canvas.getContext('2d');

const bricks = [
    new Brick(100, 140, 70, 30),
    new Brick(200, 140, 70, 30),
    new Brick(300, 140, 70, 30),
    new Brick(400, 140, 70, 30),
    new Brick(500, 140, 70, 30),
    new Brick(600, 140, 70, 30),
    new Brick(700, 140, 70, 30),
    new Brick(800, 140, 70, 30),
    new Brick(900, 140, 70, 30),
    new Brick(1000, 140, 70, 30),
    new Brick(1100, 140, 70, 30),
    new Brick(1200, 140, 70, 30),
    new Brick(1300, 140, 70, 30),
    new Brick(1400, 140, 70, 30),
    new Brick(1500, 140, 70, 30),
    new Brick(1600, 140, 70, 30),
    new Brick(1700, 140, 70, 30),

    new Brick(100, 240, 70, 30),
    new Brick(200, 240, 70, 30),
    new Brick(300, 240, 70, 30),
    new Brick(400, 240, 70, 30),
    new Brick(500, 240, 70, 30),
    new Brick(600, 240, 70, 30),
    new Brick(700, 240, 70, 30),
    new Brick(800, 240, 70, 30),
    new Brick(900, 240, 70, 30),
    new Brick(1000, 240, 70, 30),
    new Brick(1100, 240, 70, 30),
    new Brick(1200, 240, 70, 30),
    new Brick(1300, 240, 70, 30),
    new Brick(1400, 240, 70, 30),
    new Brick(1500, 240, 70, 30),
    new Brick(1600, 240, 70, 30),
    new Brick(1700, 240, 70, 30),

    new Brick(100, 340, 70, 30),
    new Brick(200, 340, 70, 30),
    new Brick(300, 340, 70, 30),
    new Brick(400, 340, 70, 30),
    new Brick(500, 340, 70, 30),
    new Brick(600, 340, 70, 30),
    new Brick(700, 340, 70, 30),
    new Brick(800, 340, 70, 30),
    new Brick(900, 340, 70, 30),
    new Brick(1000, 340, 70, 30),
    new Brick(1100, 340, 70, 30),
    new Brick(1200, 340, 70, 30),
    new Brick(1300, 340, 70, 30),
    new Brick(1400, 340, 70, 30),
    new Brick(1500, 340, 70, 30),
    new Brick(1600, 340, 70, 30),
    new Brick(1700, 340, 70, 30),

    new Brick(100, 440, 70, 30),
    new Brick(200, 440, 70, 30),
    new Brick(300, 440, 70, 30),
    new Brick(400, 440, 70, 30),
    new Brick(500, 440, 70, 30),
    new Brick(600, 440, 70, 30),
    new Brick(700, 440, 70, 30),
    new Brick(800, 440, 70, 30),
    new Brick(900, 440, 70, 30),
    new Brick(1000, 440, 70, 30),
    new Brick(1100, 440, 70, 30),
    new Brick(1200, 440, 70, 30),
    new Brick(1300, 440, 70, 30),
    new Brick(1400, 440, 70, 30),
    new Brick(1500, 440, 70, 30),
    new Brick(1600, 440, 70, 30),
    new Brick(1700, 440, 70, 30),
];

function Ball(x, y, radius) {
    this.x = x;
    this.y = y;

    this.radius = radius;

    this.velocity = { x: 5, y: 5 };

    this.draw = function() {
        ctx.fillStyle = '#ffffff';
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill()

        
    };

    this.update = function() {

        this.draw()

        collisionDetection(this, paddle, bricks)


        this.x += this.velocity.x
        this.y += this.velocity.y

        if (this.x < this.radius || this.x > canvas.width - this.radius) {
            this.velocity.x = -this.velocity.x
        } else if (this.y < this.radius || this.y > canvas.height - this.radius) {
            this.velocity.y = -this.velocity.y 
        }

    };
}

function Brick(x, y, width, height) {
    this.x = x;
    this.y = y;

    this.width = width;
    this.height = height;

    this.state = false;

    this.draw = function() {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(this.x, this.y, this.width, this.height);
    };

    this.update = function() {

        this.draw();

        
        

    };
}

function Paddle(x, y, width, height) {
    this.x = x;
    this.y = y;

    this.width = width;
    this.height = height;

    this.velocity = { x: 0, y: null };
    this.acceleration = { x: 0, y: null };

    this.draw = function() {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(this.x, this.y, this.width, this.height);

    };

    this.update = function() {

        this.draw()

        this.x += this.velocity.x

        if (this.x < 0 || this.x > canvas.width - this.width) {
            this.velocity.x = -this.velocity.x
        } 

    };
}



const ball = new Ball(canvas.width / 2, canvas.height - 100, 10);
const paddle = new Paddle(canvas.width / 2, canvas.height - 30, 80, 20);

function getDistance(circle, xHit, yHit) {

    let distX = circle.x - xHit;
    let distY = circle.y - yHit;

    let distance = Math.sqrt((distX * distX) + (distY * distY));

    if (distance <= circle.radius) {
        console.log('hit')
        return circle.velocity.y = -circle.velocity.y
    }

    return false;

}

function collisionDetection(circle, paddle, bricks) {
    /*
    If the circle is to the RIGHT of the square, check against the RIGHT edge.
    else If the circle is to the LEFT of the square, check against the LEFT edge.

    If the circle is ABOVE the square, check against the TOP edge.
    else If the circle is to the BELOW the square, check against the BOTTOM edge.
    */

    let testX = circle.x;
    let testY = circle.y;

    if (circle.x < paddle.x) {
        testX = paddle.x
    } else if (circle.x > paddle.x + paddle.width) {
        testX = paddle.x + paddle.width
    } 

    if (circle.y < paddle.y) {
        testY = paddle.y
    } else if (circle.y > paddle.y + paddle.height) {
        testY = paddle.y + paddle.height
    }

    getDistance(circle, testX, testY)
}

function animate() {
    window.requestAnimationFrame(animate);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // bounce the ball
    ball.update();

    // control the paddle
    paddle.update();

    // generate the bricks
    for (let brick of bricks) {
        brick.update();
    }
}

const [ leftArrowPressed, rightArrowPressed ] = [ 37, 39 ]
const speedOfPaddle = 8;


window.addEventListener('keydown', event => {

    switch(event.keyCode) {

        case leftArrowPressed:
            paddle.velocity.x = -speedOfPaddle
            break;

        case rightArrowPressed:
            paddle.velocity.x = speedOfPaddle;
            break;
    }

});

window.requestAnimationFrame(animate)
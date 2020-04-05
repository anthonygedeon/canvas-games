
const canvas = document.createElement('canvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

canvas.id = 'canvas';
canvas.style.backgroundColor = "#000";
document.body.appendChild(canvas)

const ctx = canvas.getContext('2d');

let keyLeft = false;
let keyRight = false;

const bricks = [];

function generateBricks() {
    let xPosition = 100;
    let yPosition = 100;

    const brickXPositionLimit = 1800

    for (let i = 0; i < 36; i++) {
        bricks.push(new Brick(xPosition, yPosition, 80, 30))
        xPosition += 200

        if (xPosition > brickXPositionLimit) {
            yPosition += 80
            xPosition = 100
        }
    }
}

generateBricks()

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

        collisionDetection(this, paddle)

        this.x += this.velocity.x
        this.y += this.velocity.y

        if (this.x < this.radius || this.x > canvas.width - this.radius) {
            this.velocity.x = -this.velocity.x
        } else if (this.y < this.radius || this.y > canvas.height - this.radius) {
            this.velocity.y = -this.velocity.y 
        }

        // reset ball when it hits bottom
        if (this.y > canvas.height - this.radius) {
            // this.y = canvas.height / 2 - 100
            // this.velocity.x = -5
            // this.velocity.y = 5
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

    this.speed = 8;
    this.perPixel = 0;
    this.force = 0;

    this.draw = function() {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(this.x, this.y, this.width, this.height);

    };

    this.update = function() {

        this.draw()

        // avoids paddle from leaving canvas
        if (this.x <= 0 || this.x >= canvas.width - this.width) {
            this.perPixel = 0

            // prevent the paddle from glitching at the bottom left/right corners
            this.x = this.x <= 0 ? 0 : canvas.width - this.width
        } 

        if (keyLeft) {
            this.force--;
        }

        if (keyRight) {
            this.force++;
        }

        if (this.force > this.speed) {
            this.force = this.speed
        }

        if (this.force < -this.speed) {
            this.force = -this.speed
        }

        if (!keyLeft && !keyRight) {
            this.perPixel = 0;
            this.force = 0;
        } else {
            this.perPixel = this.force
        }

        this.x += this.perPixel;
    };

    this.handleKeyDown = function(event) {
        if (event.keyCode === 37) {
            keyLeft = true;
        } else if (event.keyCode === 39) {
            keyRight = true;
        }
    }

    this.handleKeyUp = function(event) {
        if (event.keyCode == 37) {
            keyLeft = false;
        } else if (event.keyCode == 39) {
            keyRight = false;
        }
    }
}

const ball = new Ball(canvas.width / 2, canvas.height - 100, 10);
const paddle = new Paddle(canvas.width / 2, canvas.height - 30, 90, 20);

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

function collisionDetection(circle, paddle) {
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

    // display bricks on canvas
    for (let brick of bricks) {
        brick.update()
    }
}

window.addEventListener('keydown', event => paddle.handleKeyDown(event));
window.addEventListener('keyup', event => paddle.handleKeyUp(event));
window.requestAnimationFrame(animate)
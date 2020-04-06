
const canvas = document.createElement('canvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

canvas.id = 'canvas';
canvas.style.backgroundColor = "#000";
document.body.appendChild(canvas)

const ctx = canvas.getContext('2d');

let keyLeft = false;
let keyRight = false;

let pointEarned = 0;

let bricks = [];

const generateBricksLayout = (() => {
    let xPosition = 100;
    let yPosition = 200;

    const brickXPositionLimit = 1800

    for (let i = 0; i < 36; i++) {
        bricks.push(new Brick(xPosition, yPosition, 80, 30, false))
        xPosition += 200

        if (xPosition > brickXPositionLimit) {
            yPosition += 80
            xPosition = 100
        }
    }
})();

function Scoreboard() {

    this.draw = function() {
        ctx.fillStyle = '#ffffffff';
        ctx.font = '40px Arial';
        ctx.fillText(`Score: ${pointEarned}`, 100, 100)
    };

    this.update = function() {

        this.draw()
    };
}

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

        if (collisionDetection(this, paddle)) {
            let direction = [-5, 5];
            this.velocity.x = direction[Math.floor(Math.random() * 2)]
            this.velocity.y = -this.velocity.y;
        }

        this.x += this.velocity.x
        this.y += this.velocity.y

        if (this.x < this.radius || this.x > canvas.width - this.radius) {
            this.velocity.x = -this.velocity.x
        } else if (this.y < this.radius || this.y > canvas.height - this.radius) {
            this.velocity.y = -this.velocity.y 
        }

        // reset ball when it hits bottom
        if (this.y > canvas.height - this.radius) {
            this.y = canvas.height / 1.5;
            this.x = canvas.width / 2;
            this.velocity.x = 0
            this.velocity.y = 5
        }

    };
}

function Brick(x, y, width, height, state) {
    this.x = x;
    this.y = y;

    this.width = width;
    this.height = height;
    this.bricksTotal = 0

    this.state = state;

    this.draw = function() {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(this.x, this.y, this.width, this.height);
    };

    this.update = function() {

        this.draw();

        while (true) {

            if (collisionDetection(ball, bricks[this.bricksTotal])) {
                // change the direction of the ball
                ball.velocity.y = -ball.velocity.y;

                // if ball was hit then remove it from canvas
                bricks[this.bricksTotal].width = 0
                bricks[this.bricksTotal].height = 0
                bricks[this.bricksTotal].y = 0
                bricks[this.bricksTotal].x = 0
                

                // give player point
                pointEarned++

            }

            if (this.bricksTotal === 35) {
                this.bricksTotal = 0
                break;
            }

            this.bricksTotal++
        }

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
const score = new Scoreboard(); // does not work when i set pointEarned as a parameter

function getDistance(circle, xHit, yHit) {

    let distX = circle.x - xHit;
    let distY = circle.y - yHit;

    let distance = Math.sqrt((distX * distX) + (distY * distY));

    if (distance <= circle.radius) {
        return true
    }

    return false;

}

function collisionDetection(circle, objectToCollide) {
    /*
    If the circle is to the RIGHT of the square, check against the RIGHT edge.
    else If the circle is to the LEFT of the square, check against the LEFT edge.

    If the circle is ABOVE the square, check against the TOP edge.
    else If the circle is to the BELOW the square, check against the BOTTOM edge.
    */

    let testX = circle.x;
    let testY = circle.y;

    if (circle.x < objectToCollide.x) {
        testX = objectToCollide.x
    } else if (circle.x > objectToCollide.x + objectToCollide.width) {
        testX = objectToCollide.x + objectToCollide.width
    } 

    if (circle.y < objectToCollide.y) {
        testY = objectToCollide.y
    } else if (circle.y > objectToCollide.y + objectToCollide.height) {
        testY = objectToCollide.y + objectToCollide.height
    }

    return getDistance(circle, testX, testY)
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

    // without this, none the collision detection works for the bricks
    bricks[0].update()

    score.update();
}

window.addEventListener('keydown', event => paddle.handleKeyDown(event));
window.addEventListener('keyup', event => paddle.handleKeyUp(event));
window.requestAnimationFrame(animate)
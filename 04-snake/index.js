const canvas = document.createElement('canvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

canvas.id = 'canvas';
canvas.style.backgroundColor = "#000";
document.body.appendChild(canvas)

const ctx = canvas.getContext('2d');

function collisionDetection(object, objectToCollideWith) {
    if (object.x < objectToCollideWith.x + objectToCollideWith.width &&
        object.x + object.width > objectToCollideWith.x &&
        object.y < objectToCollideWith.y + objectToCollideWith.height &&
        object.y + object.height > objectToCollideWith.y) {
        console.log('hit')
            return true
    } 

}

function Snake(x, y, width, height) {

    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;

    this.velocity = { x: 0, y: 0 };

    this.draw = function() {
        ctx.fillStyle = '#fff';
        ctx.fillRect(this.x, this.y, this.width, this.height);

    }

    this.update = function() {

        this.draw()

        this.x += this.velocity.x;
        this.y += this.velocity.y

        if (this.x <= 0 || this.x >= canvas.width - this.width || this.y <= 0 || this.y >= canvas.height - this.height) {
            this.x = canvas.width / 2;
            this.y = canvas.height / 2;

            this.velocity.x = 0;
            this.velocity.y = 0;
        }

        

    }
}

function Apple(x, y) {
    this.x = x;
    this.y = y;

    this.width = 20;
    this.height = 20

    this.draw = function() {
        ctx.fillStyle = 'red';
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }

    this.update = function() {

        this.draw();


    }
}

const snake = new Snake(canvas.width / 2, canvas.height / 2, 20, 20);
const apple = new Apple(Math.floor(Math.random() * canvas.width), Math.floor(Math.random() * canvas.height))

function animate() {
    window.requestAnimationFrame(animate)
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    snake.update()

    if (collisionDetection(apple, snake)) {
        apple.x = Math.floor(Math.random() * canvas.width)
        apple.y = Math.floor(Math.random() * canvas.height)
    }

    apple.update()

}

window.addEventListener('keydown', event => {
    if (event.keyCode === 37) {
        snake.velocity.x = -4
        snake.velocity.y = 0;
    } else if (event.keyCode === 39) {
        snake.velocity.x = 4
        snake.velocity.y = 0;
    }

    if (event.keyCode === 40) {
        snake.velocity.y = 4
        snake.velocity.x = 0;
    } else if (event.keyCode === 38) {
        snake.velocity.y = -4
        snake.velocity.x = 0;
    }

    


})

window.requestAnimationFrame(animate)
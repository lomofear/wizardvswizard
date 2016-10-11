var Container = PIXI.Container,
    autoDetectRenderer = PIXI.autoDetectRenderer,
    loader = PIXI.loader,
    resources = PIXI.loader.resources,
    Text = PIXI.Text,
    Sprite = PIXI.Sprite;
var GAME_WIDTH = 896;
var GAME_HEIGHT = 512;
var renderer = autoDetectRenderer(GAME_WIDTH, GAME_HEIGHT); // aspect: 7/4
var logo;
var FPS = 30;

renderer.backgroundColor = 0xFFFFFF;
renderer.view.style.position = "absolute";
renderer.view.style.display = "block";
//renderer.autoResize = true;
//renderer.resize(window.innerWidth, window.innerHeight);

//Add the canvas to the HTML document
document.body.appendChild(renderer.view);

//Create a container object called the `stage`
var stage = new Container();

var loader_rect1 = new PIXI.Graphics();
loader_rect1.beginFill(0xFFFFFF);
loader_rect1.lineStyle(2, 0x000000, 1);
loader_rect1.drawRect(49, 49, 802, 22);
loader_rect1.endFill();

var loader_rect2 = new PIXI.Graphics();
loader_rect2.beginFill(0x66CCFF);
loader_rect2.lineStyle(0, 0x0000FF, 0);
loader_rect2.drawRect(0, 0, 20, 20);
loader_rect2.endFill();
loader_rect2.x = 50
loader_rect2.y = 50
stage.addChild(loader_rect1);
stage.addChild(loader_rect2);

renderer.render(stage);

var sprites = new Object();

function loadProgressHandler(loader, resource) {

    //Display the file `url` currently being loaded
    console.log("loading: " + resource.url);

    //Display the precentage of files currently loaded
    console.log("progress: " + loader.progress + "%");

    loader_rect2.width = parseInt( 50+ loader.progress * 7.5);

    renderer.render(stage);
}


loader
  .add( [
    "img/logo1.png",
    "img/button1.png",
    ""
    ]
  )
  .on("progress", loadProgressHandler)
  .load(setup);

function setup() {
    logo = new Sprite(
        loader.resources["img/logo1.png"].texture
    );
    logo.scale.set(0.25, 0.25);
    logo.anchor.set(0.5, 0.5);
    logo.x = GAME_WIDTH / 2;
    logo.y = -logo.pivot.y;
    //logo.y = GAME_HEIGHT / 2;
    //Add the cat to the stage
    stage.addChild(logo);
    stage.removeChild(loader_rect1);
    stage.removeChild(loader_rect2);
    //Render the stage
    renderer.render(stage);

    //Start the game loop
    gameLoop();
}

var game_state = play_intro1;


function gameLoop(){

    //Loop this function 60 times per second
    //requestAnimationFrame(gameLoop);
    setTimeout(gameLoop, 1000 / FPS);

    game_state();

    //Render the stage
    renderer.render(stage);
}


function play_intro1() {

          /*  setup_intro2();
            game_state = play_intro2;
*/
    if (logo.scale.x < 1) {
        logo.scale.x *= 1.015;
        logo.scale.y *= 1.015;
    } else {
        logo.scale.x = 1;
        logo.scale.y = 1;
    }
    if (logo.y < GAME_HEIGHT / 2) {
        logo.rotation += 3.0/60.0;
        logo.y += 2 + logo.scale.x;
    } else {
        logo.y = GAME_HEIGHT / 2;
        while (logo.rotation > 0.1) logo.rotation -= Math.PI * 2;
        if (logo.rotation < 0) {
            logo.rotation += 4.0/60.0;
        } else {
            logo.rotation = 0;
            setup_intro2();
            game_state = play_intro2;
        }
    }

}

function create_button(text, onDown) {
    var bg = new Sprite(
        loader.resources["img/button1.png"].texture
    );
    var btext = new PIXI.Text(
      text,
      {    fontFamily : 'Arial',
    fontSize : '36px',
    fontStyle : 'italic',
    fontWeight : 'bold',
    fill : '#F7EDCA'}
    );
    bg.anchor.set(0.5, 0.5);
    bg.x = 0;
    bg.y = 0;

    btext.emit = function(x,y,z) {};
    btext.anchor.set(0.5, 0.5);
    btext.x = 0;
    btext.y = -2;

    var button = new PIXI.Container();
    button.addChild(bg);
    button.addChild(btext);
    button.bg = bg;
    button.btext = btext;
    if (onDown) {
        bg.interactive = true;
        bg.on('mousedown', onDown);
        bg.on('touchstart', onDown);
        button.onDown = onDown;
    }

    return button;

}

function menu_button1_onDown() {
    sprites.menu_button1.alpha = 0.5;
}

function setup_intro2() {
    logo.y = GAME_HEIGHT / 2;
    logo.rotation = 0;
    logo.scale.set(1,1);

    sprites.menu_button1 = create_button("Start Game", menu_button1_onDown);
    //sprites.menu_button1.anchor.set(0.5, 0.5);
    sprites.menu_button1.x = GAME_WIDTH / 2;
    sprites.menu_button1.y = GAME_HEIGHT / 2 + 32;
    sprites.menu_button1.alpha = 0;
    stage.addChild(sprites.menu_button1);
}

function play_intro2() {
    if (logo.y > GAME_HEIGHT / 4) {
        logo.y -= 2;
    } else {
        logo.y = GAME_HEIGHT / 4;
    }
    if (sprites.menu_button1.alpha < 1 ) {
        sprites.menu_button1.alpha += 0.02;
        if (sprites.menu_button1.alpha > 0.99 ) sprites.menu_button1.alpha = 1;
    }

}


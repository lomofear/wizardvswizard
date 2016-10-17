"use strict";
var Container = PIXI.Container,
    autoDetectRenderer = PIXI.autoDetectRenderer,
    loader = PIXI.loader,
    Rectangle = PIXI.Rectangle,
    resources = PIXI.loader.resources,
    Text = PIXI.Text,
    Sprite = PIXI.Sprite;
var TextureCache = PIXI.utils.TextureCache;

var GAME_WIDTH = 896;
var GAME_HEIGHT = 512;
var renderer = autoDetectRenderer(GAME_WIDTH, GAME_HEIGHT); // aspect: 7/4
var logo;
var FPS = 30;

window.onpopstate = function(event) {
  console.log("location: " + document.location + ", state: " + JSON.stringify(event.state));
    setup_intro1();
    game_state = play_intro1;

};

PIXI.SCALE_MODES.DEFAULT = PIXI.SCALE_MODES.NEAREST;

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

    "img/creatures.json",
    "img/magic_spheres_lq.json",
    "img/background1.jpg",

    "fnt/LatoMediumBold24.fnt",
    "fnt/LatoMediumBold32.fnt",

    ""
    ]
  )
  .on("progress", loadProgressHandler)
  .load(setup);

function setup() {
    stage.removeChild(loader_rect1);
    stage.removeChild(loader_rect2);
    setup_intro1();
    game_state = play_intro1;
    //Render the stage
    renderer.render(stage);

    //Start the game loop
    gameLoop();
}

var game_state = play_intro1;

function launchIntoFullscreen(element) {
  if(element.requestFullscreen) {
    element.requestFullscreen();
  } else if(element.mozRequestFullScreen) {
    element.mozRequestFullScreen();
  } else if(element.webkitRequestFullscreen) {
    element.webkitRequestFullscreen();
  } else if(element.msRequestFullscreen) {
    element.msRequestFullscreen();
  }
}
function gameLoop(){

    //Loop this function 60 times per second
    //requestAnimationFrame(gameLoop);
    setTimeout(gameLoop, 1000 / FPS);

    game_state();

    //Render the stage
    renderer.render(stage);
}

function setup_intro1() {
    stage.removeChildren();
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

    logo.interactive = true;
    logo.onDown = function () {
        //if (game_state != play_intro1) return;
        setup_intro2();
        game_state = play_intro2;


    }
    logo.on('mousedown', logo.onDown);
    logo.on('touchstart', logo.onDown);


    history.pushState({page: "title"}, "Wizard VS Wizard - Title", "#title");

}

function unsetup_intro1() {
    stage.removeChild(logo);
}

function play_intro1() {

    //setup_intro2();
    //game_state = play_intro2;

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
        bg.hitArea = new Rectangle(-150, -28, 300, 58);
    }
    button.clicked = false;
    return button;

}

function setup_intro2() {
    logo.y = GAME_HEIGHT / 2;
    logo.rotation = 0;
    logo.scale.set(1,1);

    sprites.menu_button1 = create_button("Start Game", menu_button1_onDown);
    sprites.menu_button1.x = GAME_WIDTH / 2;
    sprites.menu_button1.y = GAME_HEIGHT / 2 + 32;
    sprites.menu_button1.alpha = 0;
    sprites.menu_button1.afterClick = menu_button1_afterClick;
    stage.addChild(sprites.menu_button1);

    sprites.menu_button2 = create_button("FullScreen", function () {launchIntoFullscreen(document.getElementsByTagName("canvas")[0]);});
    sprites.menu_button2.x = GAME_WIDTH / 2;
    sprites.menu_button2.y = GAME_HEIGHT / 2 + 96;
    sprites.menu_button2.alpha = 0;
    sprites.menu_button2.afterClick = function() {};
    stage.addChild(sprites.menu_button2);
}

function unsetup_intro2() {
    stage.removeChild(sprites.menu_button1);
    stage.removeChild(sprites.menu_button2);
}

function play_intro2() {
    if (logo.y > GAME_HEIGHT / 4) {
        logo.y -= 2;
    } else {
        logo.y = GAME_HEIGHT / 4;
    }
    if (sprites.menu_button1.alpha < 1 ) {
        sprites.menu_button1.alpha += 0.02;
        if (sprites.menu_button1.alpha > 0.99 ) {
            sprites.menu_button1.alpha = 1;
            if (sprites.menu_button1.clicked == true) {
                sprites.menu_button1.clicked = false;
                sprites.menu_button1.afterClick();
            }

        }
    }

    if (sprites.menu_button2.alpha < 1 ) {
        sprites.menu_button2.alpha += 0.02;
        if (sprites.menu_button2.alpha > 0.99 ) {
            sprites.menu_button2.alpha = 1;
        }
    }

}

function menu_button1_onDown() {
    if (sprites.menu_button1.clicked) {
        sprites.menu_button1.afterClick();
        sprites.menu_button1.clicked = false;
        return;
    }
    sprites.menu_button1.alpha = 0.5;
    sprites.menu_button1.clicked = true;
    //launchIntoFullscreen(document.documentElement); // Whole page
    //launchIntoFullscreen(document.getElementsByTagName("canvas")[0]); // Canvas

}

function menu_button1_afterClick() {
    console.log("INIT Start Game.");
    unsetup_intro1();
    unsetup_intro2();
    setup_startgame();
    game_state = play_startgame;
}

function getCreatureSprite(spritename) {
    // OLD VERSION. IT DOESNT WORK FOR MULTIPLE SPRITES!
    var locations = {
        "mage" : [2,108, 36,50],
        "goblin" : [148,287, 20, 41],
        "imp" : [48,272, 24, 56],

        "" : ""
    };

    //var texture = loader.resources["img/creatures.png"].texture;
    var texture = TextureCache["img/creatures.png"];

    var pos = locations[spritename];
    var x = pos[0];
    var y = pos[1];
    var w = pos[2];
    var h = pos[3];
    console.log("creature Sprite " + spritename + " x:" + x + " y:" + y + " w:" + w + " h:" + h);
    texture.frame = new Rectangle(x,y,w,h);
    var sprite = new Sprite(texture);
    sprite.scale.set(2.0, 2.0)
    sprite.anchor.set(0.5, 0.9);
    return sprite;
}

function getCreatureSprite(spritename) {
    var texture = TextureCache[spritename + ".png"];

    var sprite = new Sprite(texture);
    sprite.scale.set(2.0, 2.0)
    sprite.anchor.set(0.5, 0.9);
    return sprite;
}

function getSphereSprite(spritename) {
    var texture = TextureCache[spritename + "sphere.png"];

    var sprite = new Sprite(texture);
    sprite.scale.set(1.0, 1.0)
    sprite.anchor.set(0.5, 0.5);
    return sprite;
}


function setup_startgame() {

    stage.removeChildren();

    history.pushState({page: "game"}, "Wizard VS Wizard - Game", "#game");

    sprites.background1 = new Sprite(loader.resources["img/background1.jpg"].texture);
    sprites.background1.scale.x = GAME_WIDTH / 1200.0;
    sprites.background1.scale.y = GAME_WIDTH / 1200.0;
    stage.addChild(sprites.background1);


    sprites.player = getCreatureSprite("mage");
    stage.addChild(sprites.player);
    sprites.player.x = GAME_WIDTH * 0.8;
    sprites.player.y = GAME_HEIGHT * 0.7;
    sprites.player.dx = -1;


    sprites.enemies = []
    sprites.enemies[0] = getCreatureSprite("goblin");
    sprites.enemies[1] = getCreatureSprite("imp");

    sprites.enemies[0].x = GAME_WIDTH * 0.2;
    sprites.enemies[0].y = GAME_HEIGHT * 0.65;
    sprites.enemies[1].x = GAME_WIDTH * 0.3;
    sprites.enemies[1].y = GAME_HEIGHT * 0.75;
    stage.addChild(sprites.enemies[0]);
    stage.addChild(sprites.enemies[1]);

    sprites.sphere1 = getSphereSprite("red");
    sprites.sphere1.x = GAME_WIDTH * 0.4;
    sprites.sphere1.y = GAME_HEIGHT * 0.9;

    sprites.sphere2 = getSphereSprite("green");
    sprites.sphere2.x = GAME_WIDTH * 0.5;
    sprites.sphere2.y = GAME_HEIGHT * 0.9;

    sprites.sphere3 = getSphereSprite("purple");
    sprites.sphere3.x = GAME_WIDTH * 0.6;
    sprites.sphere3.y = GAME_HEIGHT * 0.9;

    sprites.sphere4 = getSphereSprite("blue");
    sprites.sphere4.x = GAME_WIDTH * 0.7;
    sprites.sphere4.y = GAME_HEIGHT * 0.9;

    sprites.sphere5 = getSphereSprite("yellow");
    sprites.sphere5.x = GAME_WIDTH * 0.8;
    sprites.sphere5.y = GAME_HEIGHT * 0.9;

    sprites.sphere6 = getSphereSprite("grey");
    sprites.sphere6.x = GAME_WIDTH * 0.9;
    sprites.sphere6.y = GAME_HEIGHT * 0.9;

    stage.addChild(sprites.sphere1);
    stage.addChild(sprites.sphere2);
    stage.addChild(sprites.sphere3);
    stage.addChild(sprites.sphere4);
    stage.addChild(sprites.sphere5);
    stage.addChild(sprites.sphere6);

    sprites.bitmapText = new PIXI.extras.BitmapText("text using a fancy font!", {font: "24px LatoMediumBold24", align: "center"});
    sprites.bitmapText.x = 100;
    sprites.bitmapText.y = 250;

    stage.addChild(sprites.bitmapText);

}

function play_startgame() {
    sprites.player.x += sprites.player.dx;
    if (sprites.player.x  < GAME_WIDTH * 0.7) sprites.player.dx = +1;
    if (sprites.player.x  > GAME_WIDTH * 0.8) sprites.player.dx = -1;
    sprites.bitmapText.text = parseInt(sprites.player.x).toString();
    sprites.bitmapText.x = sprites.player.x - 0;
    sprites.bitmapText.y = sprites.player.y + 20;
}

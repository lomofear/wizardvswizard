"use strict";
var Container = PIXI.Container,
    autoDetectRenderer = PIXI.autoDetectRenderer,
    loader = PIXI.loader,
    Rectangle = PIXI.Rectangle,
    resources = PIXI.loader.resources,
    Text = PIXI.Text,
    Sprite = PIXI.Sprite;
var TextureCache = PIXI.utils.TextureCache;

var GAME_WIDTH = 720 / 2;
var GAME_HEIGHT = 1280 / 2;
var renderer = autoDetectRenderer(GAME_WIDTH, GAME_HEIGHT);

//var EARN_SPEED = 1;
var sprites = new Object();

var game = new Object();

renderer.backgroundColor = 0x100040;

document.body.appendChild(renderer.view);
//Create a container object called the `stage`
var stage = new Container();
var game_state = null;

function init_game() {
    sprites.title_text = new PIXI.Text(
      "Clicker_1\n!!!!1!1!\n\n",
      {    fontFamily : 'Arial',
    fontSize : '64px',
    fontStyle : 'italic',
    fontWeight : 'bold',
    stroke : '#EF4800',
    strokeThickness : 6,
    dropShadow : true,
    dropShadowColor : '#000000',
    dropShadowAngle : Math.PI / 6,
    dropShadowDistance : 10,
    align : "center",
    fill : '#F7EDCA'}
    );
    sprites.title_text.anchor.set(0.5, 0.5);
    sprites.title_text.x = GAME_WIDTH / 2;
    sprites.title_text.y = GAME_HEIGHT / 2;

    stage.addChild(sprites.title_text);

    sprites.loader_rect1 = new PIXI.Graphics();
    sprites.loader_rect1.beginFill(0x000000);
    sprites.loader_rect1.lineStyle(2, 0xFFFFFF, 1);
    sprites.loader_rect1.drawRect(48, 548, 252, 23);
    sprites.loader_rect1.endFill();

    sprites.loader_rect2 = new PIXI.Graphics();
    sprites.loader_rect2.beginFill(0x66CCFF);
    sprites.loader_rect2.lineStyle(0, 0x0000FF, 0);
    sprites.loader_rect2.drawRect(0, 0, 20, 20);
    sprites.loader_rect2.endFill();
    sprites.loader_rect2.x = 50
    sprites.loader_rect2.y = 550
    stage.addChild(sprites.loader_rect1);
    stage.addChild(sprites.loader_rect2);

    renderFrame();
    loader.reset();
    loader
      .add( [

        //"img/logo1.png",
        "img/frame1.png",
        "img/button1.png",

        "img/creatures.json",
        "img/magic_spheres.json",
        "img/background1.jpg",
        "examples/images/treasure.png",

        "fnt/LatoMediumBold24.fnt",
        "fnt/LatoMediumBold32.fnt",

        ""
        ]
      )
      .on("progress", loadProgressHandler)
      .load(setup);
}

function renderFrame() {
    renderer.render(stage);
}

function loadProgressHandler(loader, resource) {
    //Display the precentage of files currently loaded
    console.log("progress: " + parseInt(loader.progress) + "% ; " + resource.url);

    sprites.loader_rect2.width = parseInt( 20+ loader.progress * 2);
    renderFrame();
}

function setup() {
    stage.removeChild(sprites.loader_rect1);
    stage.removeChild(sprites.loader_rect2);

    sprites.title_text.interactive = true;
    sprites.title_text.onDown = title_text_clicked;
    sprites.title_text.on('mousedown', sprites.title_text.onDown);
    sprites.title_text.on('touchstart', sprites.title_text.onDown);

    renderFrame();
}

function getCreatureSprite(spritename, onDown) {
    //var texture = TextureCache[spritename + ".png"];
    var texture = loader.resources[spritename].texture;
    var sprite = new Sprite(texture);
    sprite.scale.set(2.0, 2.0);
    sprite.anchor.set(0.5, 0.9);

    if(onDown) {
        sprite.interactive = true;
        sprite.onDown = onDown;
        sprite.on('mousedown', sprite.onDown);
        sprite.on('touchstart', sprite.onDown);

    }
    return sprite;
}


// Los sprites se dibujan en el orden el que se han añadido con el addChild.
function title_text_clicked() {
    stage.removeChildren();

    game.mana0 = 0;
    game.mage_power_mana0 = 5;

    sprites.player = getCreatureSprite("examples/images/treasure.png",
        function() {
            if (sprites.barravida.scale.x > 0) {
                sprites.barravida.scale.x -= 0.1;
            }
            if (sprites.barravida.scale.x < 0) {
                sprites.barravida.scale.x = 0;
            }
    });
    sprites.player.x = GAME_WIDTH/2;
    sprites.player.y = GAME_HEIGHT/2;
    stage.addChild(sprites.player);

    sprites.barravida = new PIXI.Graphics();
    sprites.barravida.beginFill(0xFF0000);
    sprites.barravida.lineStyle(2, 0xFFFFFF, 1);
    sprites.barravida.drawRect(0,0, 50, 10);
    sprites.barravida.endFill();

    sprites.barravida.x = -sprites.barravida.width/2;

    sprites.cntbarravida = new PIXI.Container();
    sprites.cntbarravida.addChild(sprites.barravida);

    sprites.cntbarravida.x = GAME_WIDTH/2;
    sprites.cntbarravida.y = (GAME_HEIGHT/2)+10;



    /*sprites.loader_rect2 = new PIXI.Graphics();
    sprites.loader_rect2.beginFill(0x66CCFF);
    sprites.loader_rect2.lineStyle(0, 0x0000FF, 0);
    sprites.loader_rect2.drawRect(0, 0, 20, 20);
    sprites.loader_rect2.endFill();
    sprites.loader_rect2.x = 50
    sprites.loader_rect2.y = 550*/
    stage.addChild(sprites.cntbarravida);
    //stage.addChild(sprites.loader_rect2);


/*


    sprites.sphere0 = getSphereSprite("grey");
    sprites.sphere0.x = GAME_WIDTH * 0.9;
    sprites.sphere0.y = GAME_HEIGHT * 0.9;

    sprites.sphere0text = new PIXI.extras.BitmapText("Lvl\n0.00", {font: "32px LatoMediumBold32", align: "center"});
    sprites.sphere0text.anchor.set(0.5, 0.5);
    sprites.sphere0text.x = 0;
    sprites.sphere0text.y = 0;

    sprites.sphere0.addChild(sprites.sphere0text);

    stage.addChild(sprites.sphere0);
*/

    sprites.txtvida = new PIXI.Text(
      "300",
      {    fontFamily : 'Arial',
    fontSize : '24px',
    fontStyle : 'italic',
    fontWeight : 'bold',
    align : "center",
    fill : '#F7EDCA'}
    );
    sprites.txtvida.anchor.set(0.5, 0.5);
    sprites.txtvida.x = GAME_WIDTH / 2;
    sprites.txtvida.y = GAME_HEIGHT / 2 + 100;

    stage.addChild(sprites.txtvida);

    game_state = play_game;
    gameLoop();
}

function gameLoop(){

    //Loop this function 60 times per second
    requestAnimationFrame(gameLoop);

    if (game_state) {
        game_state();
    }

    //Render the stage
    renderFrame();
}


function play_game() {
    //sprites.barravida.rotation += 2/1000.0;
    if (sprites.barravida.scale.x >= 1) {
        sprites.barravida.scale.x = 1;
    } if (sprites.barravida.scale.x == 0) {
        sprites.barravida.scale.x = 0;
    }else {
        sprites.barravida.scale.x += 1/2000.0;
    }
    sprites.txtvida.text = parseInt(sprites.barravida.scale.x * 300).toString();
}

init_game();

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

var EARN_SPEED = 5;
var sprites = new Object();

var game = new Object();

//PIXI.SCALE_MODES.DEFAULT = PIXI.SCALE_MODES.NEAREST;

renderer.backgroundColor = 0x100040;

document.body.appendChild(renderer.view);

//Create a container object called the `stage`
var stage = new Container();

var final_stage = new Container(); // To manage Zoom.

final_stage.addChild(stage);

var game_state = null;

function init_game() {
    sprites.title_text = new PIXI.Text(
      "Wizard\nClicker!\n!!!!1!1!\n\n",
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

    renderer.render(final_stage);
    loader.reset();
    loader
      .add( [

        //"img/logo1.png",
        "img/frame1.png",
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
}

function renderFrame() {
    renderer.render(final_stage);
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


window.onpopstate = function(event) {
    console.log("location: " + document.location + ", state: " + JSON.stringify(event.state));
    stage.removeChildren();
    init_game();

};

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

function title_text_clicked() {
    launchIntoFullscreen(document.getElementsByTagName("canvas")[0]);
    stage.removeChildren();
    history.pushState({page: "game"}, "Wizard Clicker - Game", "#game");

    game.mana0 = 0;
    game.mana1 = 0;
    game.mana2 = 0;
    game.mage_power_mana0 = 1;
    game.mage_power_mana1 = 0;
    game.mage_power_mana2 = 0;

    sprites.player = getCreatureSprite("mage", mage_clicked);
    stage.addChild(sprites.player);
    sprites.player.x = 50 + 30;
    sprites.player.y = 70 + 30;


    sprites.sphere0 = getSphereSprite("grey");
    sprites.sphere0.x = GAME_WIDTH * 0.9;
    sprites.sphere0.y = GAME_HEIGHT * 0.9;

    sprites.sphere0text = new PIXI.extras.BitmapText("Lvl\n0.00", {font: "16px LatoMediumBold32", align: "center"});
    sprites.sphere0text.anchor.set(0.5, 0.5);
    sprites.sphere0text.x = 0;
    sprites.sphere0text.y = 0;

    sprites.sphere0.addChild(sprites.sphere0text);

    sprites.sphere1 = getSphereSprite("red");
    sprites.sphere1.x = GAME_WIDTH * 0.7;
    sprites.sphere1.y = GAME_HEIGHT * 0.9;

    sprites.sphere1text = new PIXI.extras.BitmapText("Lvl\n0.00", {font: "16px LatoMediumBold32", align: "center"});
    sprites.sphere1text.anchor.set(0.5, 0.5);
    sprites.sphere1text.x = 0;
    sprites.sphere1text.y = 0;

    sprites.sphere1.addChild(sprites.sphere1text);

    sprites.sphere2 = getSphereSprite("blue");
    sprites.sphere2.x = GAME_WIDTH * 0.5;
    sprites.sphere2.y = GAME_HEIGHT * 0.9;

    sprites.sphere2text = new PIXI.extras.BitmapText("Lvl\n0.00", {font: "16px LatoMediumBold32", align: "center"});
    sprites.sphere2text.anchor.set(0.5, 0.5);
    sprites.sphere2text.x = 0;
    sprites.sphere2text.y = 0;

    sprites.sphere2.addChild(sprites.sphere2text);


    update_mana_levels();

    stage.addChild(sprites.sphere0);
    stage.addChild(sprites.sphere1);
    stage.addChild(sprites.sphere2);

    game_state = play_game;
    gameLoop();
}

function update_mana_levels() {
    function f(x,q) {
        x /= 10.0;
        var l = Math.log(x+1);
        var n = 0;
        if (l >= q) n = l - q + 1;
        else n = x / Math.exp(q);
        return Math.max(n,0).toFixed(2);
    }
    function f(x,q) {
        var p1 = Math.pow(20 * q + x / q, 1.0/q) - Math.pow(20 * q, 1.0/q) ;
        var p2 = 15 * p1 / Math.pow(Math.log(x * q + 10),2) + 10;
        return (Math.min(p1,p2)).toFixed(2);
    }
    //console.log(game.mana0 + " " + Math.log(game.mana0+1).toFixed(2));
    game.lvmana0 = f(game.mana0, 2);
    game.lvmana1 = f(game.mana1, 4);
    game.lvmana2 = f(game.mana2, 6);

    sprites.sphere0text.text = "Lvl\n" + game.lvmana0;
    sprites.sphere1text.text = "Lvl\n" + game.lvmana1;
    sprites.sphere2text.text = "Lvl\n" + game.lvmana2;
}

function getCreatureSprite(spritename, onDown) {
    var texture = TextureCache[spritename + ".png"];
    var cntsprite = new Container();
    var frame = new Sprite(loader.resources["img/frame1.png"].texture);
    var sprite = new Sprite(texture);
    frame.scale.set(0.4, 0.4);
    frame.anchor.set(0.5, 0.5);
    sprite.scale.set(1.0, 1.0)
    sprite.anchor.set(0.5, 0.9);
    sprite.x = 0;
    sprite.y = 20;
    cntsprite.addChild(frame);
    cntsprite.addChild(sprite);
    cntsprite._frame = frame
    cntsprite._sprite = sprite

    if(onDown) {
        frame.interactive = true;
        cntsprite.onDown = onDown;
        frame.on('mousedown', cntsprite.onDown);
        frame.on('touchstart', cntsprite.onDown);

    }
    return cntsprite;
}

function getSphereSprite(spritename) {
    var texture = TextureCache[spritename + "sphere.png"];

    var sprite = new Sprite(texture);
    sprite.scale.set(1.0, 1.0)
    sprite.anchor.set(0.5, 0.5);
    return sprite;
}

function mage_clicked() {
    var i;
    for (i=0; i < EARN_SPEED; i++) {
        game.mana0 += game.mage_power_mana0 ;
        game.mana1 += game.mage_power_mana1 + parseInt(game.lvmana0) / 5.0;
        game.mana2 += game.mage_power_mana2 + parseInt(game.lvmana1) / 5.0;
    }
    update_mana_levels();

}

function play_game() {
    var i;
    for (i=0; i < EARN_SPEED; i++) {
        game.mana0 += parseFloat(game.lvmana0) / 100.0;
        game.mana1 += parseFloat(game.lvmana1) / 20.0 + parseFloat(game.lvmana0) / 100.0;
        game.mana2 += parseFloat(game.lvmana2) / 5.0 + parseFloat(game.lvmana1) / 20.0;
    }
    update_mana_levels();

}


function gameLoop(){

    //Loop this function 60 times per second
    requestAnimationFrame(gameLoop);

    if (game_state) {
        game_state();
    }

    //Render the stage
    renderer.render(stage);
}

init_game();



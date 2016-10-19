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

var sprites = new Object();

//PIXI.SCALE_MODES.DEFAULT = PIXI.SCALE_MODES.NEAREST;

renderer.backgroundColor = 0x100040;

document.body.appendChild(renderer.view);

//Create a container object called the `stage`
var stage = new Container();

var final_stage = new Container(); // To manage Zoom.

final_stage.addChild(stage);



function init_game() {

    sprites.loader_rect1 = new PIXI.Graphics();
    sprites.loader_rect1.beginFill(0x000000);
    sprites.loader_rect1.lineStyle(2, 0xFFFFFF, 1);
    sprites.loader_rect1.drawRect(48, 148, 602, 23);
    sprites.loader_rect1.endFill();

    sprites.loader_rect2 = new PIXI.Graphics();
    sprites.loader_rect2.beginFill(0x66CCFF);
    sprites.loader_rect2.lineStyle(0, 0x0000FF, 0);
    sprites.loader_rect2.drawRect(0, 0, 20, 20);
    sprites.loader_rect2.endFill();
    sprites.loader_rect2.x = 50
    sprites.loader_rect2.y = 150
    stage.addChild(sprites.loader_rect1);
    stage.addChild(sprites.loader_rect2);

    renderer.render(final_stage);

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
}

function renderFrame() {
    renderer.render(final_stage);
}

function loadProgressHandler(loader, resource) {
    //Display the precentage of files currently loaded
    console.log("progress: " + parseInt(loader.progress) + "% ; " + resource.url);

    sprites.loader_rect2.width = parseInt( 50+ loader.progress * 4);
    renderFrame();
}

function setup() {
    stage.removeChildren();
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
    sprites.title_text.interactive = true;
    sprites.title_text.onDown = title_text_clicked;
    sprites.title_text.on('mousedown', sprites.title_text.onDown);
    sprites.title_text.on('touchstart', sprites.title_text.onDown);

    stage.addChild(sprites.title_text);

    renderFrame();
}

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
}

init_game();



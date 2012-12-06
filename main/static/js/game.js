(function() {
    TILE_SIZE = 32;
    MAP_SIZE = MAP_W = MAP_H = 16;
    Crafty.sprite(TILE_SIZE, "/static/official/players/default.png", {
        player: [0, 0]
    });
    
    Crafty.c("SliderMovementControls", {
        move: {
            left: false,
            right: false,
            up: false,
            down: false
        },
        
        lastArrowId: -1,
        detectArrow: function() {
            _this = this;
            ArrowComponents = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "ArrowNone"];
            ArrowComponents.forEach(function(component, index, array) {
                arrows = Crafty(component);
                arrows.toArray().forEach(function(id, index, array) {
                    arrow = Crafty(id);
                    arrow_id = arrow[0];
                    if (arrow.x == _this.x && arrow.y == _this.y) {
                        if (_this.lastArrowId != arrow_id) {
                            _this.lastArrowId = arrow_id
                            _this.StopSlide();
                            switch (component) {
                                case "ArrowUp":
                                    _this.move.up = true;
                                    break;
                                case "ArrowDown":
                                    _this.move.down = true;
                                    break;
                                case "ArrowLeft":
                                    _this.move.left = true;
                                    break;
                                case "ArrowRight":
                                    _this.move.right = true;
                                    break;
                                case "ArrowNone":
                                    _this.trigger('EndMove');
                                    break;
                            }
                        } else {
                            
                        }
                        return;
                    } else {
                        if (_this.lastArrowId == arrow_id) {
                            _this.lastArrowId = -1;
                        }
                    }
                });
            });
        },
        
        detectExit: function() {
            exit = Crafty("Exit");
            if (exit.x == this.x && exit.y == this.y) {
                this.StopSlide();
                Crafty.scene("victory");
            }
        },
        
        StopSlide: function() {
            this.move.right = this.move.left = this.move.up = this.move.down = false;
        },
        
        SliderMovementControls: function(speed) {
            if (speed == null) {
                speed = 8;
            }
            
            this.bind('EnterFrame', function() {
                this.detectExit();
                this.detectArrow();
                if (this.move.right) {
                    return this.attr({x: this.x + speed});
                } else if (this.move.left) {
                    return this.attr({x: this.x - speed});
                } else if (this.move.up) {
                    return this.attr({y: this.y - speed});
                } else if (this.move.down) {
                    return this.attr({y: this.y + speed});
                }
            });
            
            this.bind('KeyDown', function(e) {
                if (!(this.move.right || this.move.left || this.move.up || this.move.down)) {
                    if (e.keyCode === Crafty.keys.RIGHT_ARROW || e.keyCode === Crafty.keys.D) {
                        this.move.right = true;
                    } else if (e.keyCode === Crafty.keys.LEFT_ARROW || e.keyCode === Crafty.keys.A) {
                        this.move.left = true;
                    } else if (e.keyCode === Crafty.keys.UP_ARROW || e.keyCode === Crafty.keys.W) {
                        this.move.up = true;
                    } else if (e.keyCode === Crafty.keys.DOWN_ARROW || e.keyCode === Crafty.keys.S) {
                        this.move.down = true;
                    }
                }
                if (this.move.right || this.move.left || this.move.up || this.move.down) {
                    this.trigger('StartMove');
                }
            });
            
            this.onHit("Solid", function() {
                if (this.move.right) {
                    this.attr({x: this.x - speed});
                } else if (this.move.left) {
                    this.attr({x: this.x + speed});
                } else if (this.move.up) {
                    this.attr({y: this.y + speed});
                } else if (this.move.down) {
                    this.attr({y: this.y - speed});
                }
                this.StopSlide();
                this.trigger('EndMove');
            });
        }
    });
    
    Crafty.c("Player", {
        Player: function() {
            this.onHit("Trap", function() {
                this.StopSlide();
                Crafty.scene("level");
            });
            
            this.onHit("Key", function() {
                Crafty("Door").destroy();
                Crafty("Key").destroy();
            });
            
            this.animate("move", 0, 0, 9);
            this.animate("stop", 0, 0, 0);
            
            this.bind("StartMove", function() {
                if (!this.isPlaying("move")) {
                    this.animate("move", 0, -1);
                }
            });
            
            this.bind("EndMove", function() {
                this.animate("stop", 0, -1);
            });
        }
    });
    
    
    Crafty.bind('KeyUp', function(e) {
        if (e.keyCode === Crafty.keys.R) {
            restartLevel();
        } else if (e.keyCode === Crafty.keys.Z) {
            Crafty.audio.muted ? Crafty.audio.unmute() : Crafty.audio.mute();
        }
    });
        
    Crafty.scene("level", function() {
        player = generateWorld();
        player.StopSlide();
    });
    
    Crafty.scene("victory", function() {
        victory_text = Crafty.e("2D, DOM, Text");
        victory_text.attr({
            w: TILE_SIZE * MAP_SIZE,
            h: 20,
            x: 0,
            y: (TILE_SIZE * MAP_SIZE) / 2 - 10
        });
        victory_text.text("To be continued...");
        victory_text.css({
            "text-align": "center",
            "color": "#FFF"
        });
    });
    
    generateWorld = function() {
        generateboundaries();
        
        floor_layer = getLayer("floor");
        soild_layer = getLayer("soild");
        item_layer = getLayer("item");
        
        for (row = 0; row < MAP_SIZE; row++) {
            for (column = 0; column < MAP_SIZE; column++) {
                index = row * MAP_SIZE + column;
                
                e = ["2D", "DOM"];
                floor_cell = floor_layer.data[index];
                switch (floor_cell) {
                    case 0:
                        floor_cell = 1;
                        e.push("Trap");
                        break;
                    case 1:
                        e.push("Trap");
                        break;
                    case 2:
                        e.push("Exit");
                        break;
                    case 17:
                        e.push("ArrowDown");
                        break;
                    case 18:
                        e.push("ArrowUp");
                        break;
                    case 19:
                        e.push("ArrowLeft");
                        break;
                    case 20:
                        e.push("ArrowRight");
                        break;
                    case 21:
                        e.push("ArrowNone");
                        break;
                }
                e.push("cell" + floor_cell);
                floor_tile = Crafty.e(e.join());
                floor_tile.attr({"x": column * TILE_SIZE, "y": row * TILE_SIZE});
                
                e = ["2D", "DOM"];
                item_cell = item_layer.data[index];
                switch (item_cell) {
                    case 49:
                        e.push("Key");
                        break;
                    case 50:
                        e.push("Door");
                        e.push("Solid");
                        break;
                }
                e.push("cell" + item_cell);
                item_tile = Crafty.e(e.join());
                item_tile.attr({"x": column * TILE_SIZE, "y": row * TILE_SIZE});
                
                soild_cell = soild_layer.data[index];
                switch (soild_cell) {
                    case 0:
                        break;
                    default:
                        soild_tile = Crafty.e("2D, DOM, Solid, cell" + soild_cell);
                        soild_tile.attr({"x": column * TILE_SIZE, "y": row * TILE_SIZE});
                }
            }
        }
        
        player = Crafty.e("2D, DOM, player, Collision, SliderMovementControls, Tween, SpriteAnimation, Player");
        player.SliderMovementControls();
        player.Player();
        
        object_layer = getLayer("object");
        player_attr = object_layer.objects[0];
        player.attr({"x": player_attr.x, "y": player_attr.y});
        return player;
    }
    
    generateSprites = function(image) {
        for (row = 1; row <= MAP_SIZE; row++) {
            for (column = 1; column <= MAP_SIZE; column++) {
                map = {}
                cell = (row - 1) * MAP_SIZE + column;
                name = "cell" + cell;
                map[name] = [column - 1, row - 1];
                Crafty.sprite(TILE_SIZE, image, map);
            }
        }
    }
    
    getLayer = function(name) {
        for (i = 0; i < level.layers.length; i++) {
            layer = level.layers[i];
            if (layer.name == name) {
                return layer;
            }
        }
    }
    
    
    generateboundaries = function() {
        for (row = -1; row <= MAP_SIZE; row++) {
            for (column = -1; column <= MAP_SIZE; column++) {
                if (row == -1 || column == -1 || row == MAP_SIZE || column == MAP_SIZE) {
                    trap = Crafty.e("2D", "DOM", "Trap", "cell1");
                    trap.attr({"x": column * TILE_SIZE, "y": row * TILE_SIZE});
                }
            }
        }
    }
    
    main = function() {
        generateSprites("/static/official/sprites/default.png");
        Crafty.audio.add("normal", "/static/official/sounds/normal.mp3");
        Crafty.audio.play("normal", -1);
        Crafty.init(TILE_SIZE * MAP_W, TILE_SIZE * MAP_H);
        
        Crafty.scene("loading");
    };
    
    restartLevel = function() {
        Crafty.scene("level");
    }
    
    Crafty.scene("loading", function() {
        loading_text = Crafty.e("2D, DOM, Text");
        loading_text.attr({
            w: TILE_SIZE * MAP_W,
            h: 20,
            x: 0,
            y: (TILE_SIZE * MAP_H) / 2 - 10
        });
        loading_text.text("Loading...");
        loading_text.css({
            "text-align": "center",
            "color": "#FFF"
        });
        
        Crafty.scene("level");
    });
    
    window.onload = main;
}).call(this);

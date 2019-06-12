
function MySocket(arg) {
    var url = arg.url;
    var ws = undefined;
    if ("WebSocket" in window) {
        ws = new WebSocket(url);
    }
    else if("MozWebSocket" in window) {
        ws = new MozWebSocket(url);
    }
    this.socket = ws;
    this.cbRegister = {};
    var self = this;
    function WSonOpen() {
        console.log("连接已经建立。OK");
        self.fire('connect', '');
    };
    
    function WSonMessage(event) {
        //console.log(event.data);
        //var tmpArg = event.data.split('\n');
        //var obj = JSON.parse(tmpArg[1]);
        var obj = JSON.parse(event.data);
        self.fire(obj.n, obj.d);
    };

    function WSonClose() {
        self.fire('close', 'onclose');
        console.log("WSonClose远程连接中断。");
    };

    function WSonError() {
        self.fire('error', 'onerror');
        console.log("WSonError远程连接中断。");
    };
    ws.onopen    = WSonOpen;
    ws.onmessage = WSonMessage;
    ws.onclose   = WSonClose;
    ws.onerror   = WSonError;
}
MySocket.prototype.on = function(name, func){
    if (typeof  this.cbRegister[name] == 'undefined'){
        this.cbRegister[name] = [func];
    }
    else{
        this.cbRegister[name].push(func);
    }
}
MySocket.prototype.fire = function(name, data){
    //console.log("fire:"+name+data);
    if(this.cbRegister[name] instanceof Array){
        const handlers = this.cbRegister[name];
        handlers.forEach((handler)=>{
            handler(data);
        })
    }
}
MySocket.prototype.send = function(name, data){
    var dataReq = JSON.stringify({
        n: name,
        d: data
    });
    //var cmdReq = 1;
    //var reqMsg   = 'cmd:' + cmdReq + '\n'+dataReq;
    //console.log(dataReq);
    this.socket.send(dataReq);
}

pc.script.create('client', function (context) {
    // If `?gamepad=2` is passed we will use `navigator.getGamepads[1]`.
    // Otherwise, we will assume `navigator.getGamepads[0]`, if connected.
    var uri = new pc.URI(window.location.href);
    var query = uri.getQuery();
    var gamepadNum = query.gamepad;

    var Client = function (entity) {
        this.entity = entity;
        this.id = null;
        this.movement = [ 0, 0 ];
        context.keyboard = new pc.input.Keyboard(document.body);
        
        document.body.style.cursor = 'none';
    };

    Client.prototype = {
        initialize: function () {
            this.link = context.root.findByName('camera').script.link;
            this.tanks = context.root.getChildren()[0].script.tanks;
            this.bullets = context.root.getChildren()[0].script.bullets;
            this.pickables = context.root.getChildren()[0].script.pickables;
            this.teams = context.root.getChildren()[0].script.teams;
            this.minimap = context.root.getChildren()[0].script.minimap;
            
            var self = this;

            // Get query-string parameters (à la `URLSearchParams`).
            var uri = new pc.URI(window.location.href);
            var query = uri.getQuery();
            var socketPort = 'wsport' in query ? query.wsport : 44000;
            var socketIP = 'wsip' in query ? query.wsip : '47.101.179.174';

            var socketUrl = (window.location.protocol + '//' +
                             window.location.hostname + ':' + socketPort + '/socket');
            var socketUrl2 = 'ws://'+socketIP+':'+socketPort+'/socket';
            console.log(socketUrl2);
            if (socketPort != 30043){
                var socket = this.socket = new MySocket({ url: socketUrl2 });
            }
            else{
                var socket = this.socket = new Socket({ url: socketUrl });
            }
            
            
            this.connected = false;

            socket.on('connect', function() {
                console.log("on.connect");
                var qs_player = /[\?&]player=([\w\-]+)/i.exec(window.location.search);
                socket.send('register.game', qs_player && qs_player[1]);
            });

            socket.on('error', function(err) {
                console.error('WS error:', err);
            });
            
            socket.on('init', function(data) {
                self.id = data.id;
                self.connected = true;
                
                self.minimap.state(true);
                console.log('init......')
            });
            
            socket.on('tank.new', function(data) {
                self.tanks.new(data);
            });
            
            socket.on('tank.delete', function(data) {
                self.tanks.delete(data);
            });
            
            socket.on('update', function(data) {
                // bullets add
                if (data.bullets) {
                    for(var i = 0; i < data.bullets.length; i++)
                        self.bullets.new(data.bullets[i]);
                }
                
                // bullets delete
                if (data.bulletsDelete) {
                    for(var i = 0; i < data.bulletsDelete.length; i++)
                        self.bullets.delete(data.bulletsDelete[i]);
                }
                
                // pickables add
                if (data.pickable) {
                    for(var i = 0; i < data.pickable.length; i++)
                        self.pickables.new(data.pickable[i]);
                }
                
                // pickable delete
                if (data.pickableDelete) {
                    for(var i = 0; i < data.pickableDelete.length; i++)
                        self.pickables.delete(data.pickableDelete[i]);
                }
                
                // tanks update
                if (data.tanks)
                    self.tanks.updateData(data.tanks);

                // tanks respawn
                if (data.tanksRespawn) {
                    for(var i = 0; i < data.tanksRespawn.length; i++)
                        self.tanks.respawn(data.tanksRespawn[i]);
                }
                
                // teams score
                if (data.teams) {
                    for(var i = 0; i < data.teams.length; i++) {
                        self.teams.teamScore(i, data.teams[i]);
                    }
                }
                
                // winner
                if (data.winner) {
                    self.shoot(false);
                    self.teams.teamWin(data.winner);
                }
            });

            context.mouse.on('mousedown', this.onMouseDown, this);
            context.mouse.on('mouseup', this.onMouseUp, this);

            this.gamepadConnected = false;
            this.gamepadActive = false;

            window.addEventListener('gamepadconnected', function () {
                this.gamepadConnected = true;
            }.bind(this));
            window.addEventListener('gamepaddisconnected', function () {
                this.gamepadConnected = false;
            }.bind(this));

            // Chrome doesn't have the gamepad events, and we can't
            // feature detect them in Firefox unfortunately.
            if ('chrome' in window) {
                // This is a lie, but it lets us begin polling.
                this.gamepadConnected = true;
            }
        },

        update: function (dt) {
            if (! this.connected)
                return;
                
            // collect keyboard input
            var movement = [
                context.keyboard.isPressed(pc.input.KEY_D) - context.keyboard.isPressed(pc.input.KEY_A),
                context.keyboard.isPressed(pc.input.KEY_S) - context.keyboard.isPressed(pc.input.KEY_W)
            ];
            
            movement[0] += context.keyboard.isPressed(pc.input.KEY_RIGHT) - context.keyboard.isPressed(pc.input.KEY_LEFT);
            movement[1] += context.keyboard.isPressed(pc.input.KEY_DOWN) - context.keyboard.isPressed(pc.input.KEY_UP);

            // Gamepad controls.
            // AUTHORS: Potch and cvan
            if (context.gamepads.gamepadsSupported && this.gamepadConnected) {
                var gamepadIdx = gamepadNum - 1;

                if (!context.gamepads.poll()[gamepadIdx]) {
                    // If it was active at one point, reset things.
                    if (self.gamepadActive && self.link && self.link.mouse) {
                        self.link.mouse.move = true;
                        this.gamepadActive = false;
                    }
                } else {
                    // Gamepad movement axes.
                    var x = context.gamepads.getAxis(gamepadIdx, pc.PAD_L_STICK_X);
                    var y = context.gamepads.getAxis(gamepadIdx, pc.PAD_L_STICK_Y);
                    if ((x * x + y * y) > .25) {
                        movement[0] += x;
                        movement[1] += y;
                    }

                    // Gamepad firing axes.
                    var gpx = context.gamepads.getAxis(gamepadIdx, pc.PAD_R_STICK_X);
                    var gpy = context.gamepads.getAxis(gamepadIdx, pc.PAD_R_STICK_Y);

                    if (x || y || gpx || gpy) {
                        this.gamepadActive = true;

                        if (this.link && this.link.mouse) {
                            this.link.mouse.move = false;

                            // TODO: Figure out how to hide cursor without destroying
                            // (so we can show the cursor again if gamepad is disconnected).
                            var target = context.root.findByName('target');
                            if (target) {
                                target.destroy();
                            }
                        }
                    }

                    // Gamepad shooting.
                    if (gpx * gpx + gpy * gpy > .25) {
                        this.shoot(true);

                        if (this.link) {
                            this.link.mPos = [
                                gpx / 2 * (context.graphicsDevice.width / 2),
                                gpy / 2 * (context.graphicsDevice.height / 2)
                            ];

                            this.link.angle = Math.floor(Math.atan2(gpx, gpy) / (Math.PI / 180) + 45);
                            if (this.link.link) {
                                this.link.link.targeting(this.link.angle);
                            }
                        }
                    } else {
                        this.shoot(false);
                    }
                }
            }

            // rotate vector
            var t =       movement[0] * Math.sin(Math.PI * 0.75) - movement[1] * Math.cos(Math.PI * 0.75);
            movement[1] = movement[1] * Math.sin(Math.PI * 0.75) + movement[0] * Math.cos(Math.PI * 0.75);
            movement[0] = t;
            
            // check if it is changed
            if (movement[0] !== this.movement[0] || movement[1] != this.movement[1]) {
                this.movement = movement;
                this.socket.send('move', this.movement);
            }
        },
        
        onMouseDown: function() {
            this.shoot(true);
        },
        
        onMouseUp: function() {
            this.shoot(false);
        },
        
        shoot: function(state) {
            if (! this.connected)
                return;
                
            if (this.shootingState !== state) {
                this.shootingState = state;
                
                this.socket.send('shoot', this.shootingState);
            }
        }
    };

    return Client;
});
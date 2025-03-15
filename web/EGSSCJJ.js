import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Comfy.EGSSCJJ",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "EGSSCJJ") {
            nodeType.prototype.randomNumber = "000000";
            nodeType.prototype.isAnimating = false;
            nodeType.prototype.animationInterval = null;

            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const ret = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                this.addWidget("button", "开始抽奖", "start", () => {
                    this.startAnimation();
                });
                this.addWidget("button", "停止抽奖", "stop", () => {
                    this.stopAnimation();
                });

                // 设置节点可调整大小
                this.resizable = true;

                return ret;
            };

            nodeType.prototype.startAnimation = function() {
                if (this.isAnimating) return;
                this.isAnimating = true;
                const min = parseInt(this.widgets.find(w => w.name === "起始抽奖号").value);
                const max = parseInt(this.widgets.find(w => w.name === "结束抽奖号").value);
                
                if (isNaN(min) || isNaN(max) || min > max) {
                    this.randomNumber = "无效范围";
                    this.setDirtyCanvas(true);
                    return;
                }
                
                this.animationInterval = setInterval(() => {
                    this.randomNumber = Math.floor(Math.random() * (max - min + 1) + min).toString().padStart(6, '0');
                    this.setDirtyCanvas(true);
                }, 50);
            };

            nodeType.prototype.stopAnimation = function() {
                if (!this.isAnimating) return;
                clearInterval(this.animationInterval);
                this.isAnimating = false;
                this.setDirtyCanvas(true);
            };

            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
                const newNumber = message?.output?.output?.[0];
                if (newNumber !== undefined) {
                    this.randomNumber = newNumber.toString().padStart(6, '0');
                    this.setDirtyCanvas(true);
                }
            };

            const onDrawForeground = nodeType.prototype.onDrawForeground;
            nodeType.prototype.onDrawForeground = function (ctx) {
                if (onDrawForeground) {
                    onDrawForeground.apply(this, arguments);
                }

                ctx.save();
                ctx.fillStyle = "black";  // 背景设为黑色
                ctx.fillRect(0, 0, this.size[0], this.size[1]);
                ctx.fillStyle = !this.isAnimating && this.randomNumber !== "000000" ? "red" : "white";  // 修改这里
                ctx.font = `bold ${Math.min(this.size[0] / 6, this.size[1] / 2)}px Arial`;
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                ctx.fillText(this.randomNumber, this.size[0] / 2, this.size[1] / 2);
                ctx.restore();
            };

            const onPropertyChanged = nodeType.prototype.onPropertyChanged;
            nodeType.prototype.onPropertyChanged = function(property, value) {
                if (onPropertyChanged) {
                    onPropertyChanged.apply(this, arguments);
                }
                if (property === "起始抽奖号" || property === "结束抽奖号") {
                    if (this.isAnimating) {
                        this.stopAnimation();
                        this.startAnimation();
                    }
                }
            };

            // 添加大小变化处理
            const onResize = nodeType.prototype.onResize;
            nodeType.prototype.onResize = function(size) {
                if (onResize) {
                    onResize.apply(this, arguments);
                }
                this.setDirtyCanvas(true);
            };
        }
    }
});

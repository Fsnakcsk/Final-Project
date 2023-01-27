ctx.putImageData(convasData, 0, 0, 0, 0, canvas.offsetWidth, canvas.offsetHeight);
ctx.getImageData(convasData, 0, 0, 0, 0, canvas.offsetWidth, canvas.offsetHeight);

var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var drawdown = false;
var startPointX, startPointY;
var toolcontrol = {
    pencil: false,
    line: false,
}
var convasData = null;
var drawcolor = "#000";
var curtool;
var textvalue;
function setUsingTool(tool) {
    for (const key in toolcontrol) {
        toolcontrol[key] = false;
    }
    toolcontrol[tool] = true;
    curtool = tool;
    // curtool=='line'?
    //     ctx=canvas2.getContext('2d'):
    // ctx=canvas.getContext('2d');
}
//function clearCanvas() {
//  ctx.clearRect(0, 0, 1000, 1000)
//}
function drawToolHandler(tool) {
    canvas.addEventListener('mousedown', handleMouseDown);
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mouseup', handleMouseUp);
}

var handleMouseDown = (e) => {
    switch (curtool) {
        case 'pencil':
            drawdown = true;
            ctx.beginPath();
            ctx.moveTo(e.offsetX, e.offsetY);
            break;
        case 'line':
        case 'rect':
        case 'ring':
        case 'text':
            drawdown = true;
            startPointX = e.offsetX;
            startPointY = e.offsetY;
            break;
        case 'eraser':
            drawdown = true;
            break;
        default: return;
    }
}
var handleMouseMove = (e) => {
    switch (curtool) {
        case 'pencil':
            if (drawdown) {
                ctx.lineTo(e.offsetX, e.offsetY)
                ctx.strokeStyle = drawcolor.toString();
                ctx.stroke();
            }
            break;
        case 'line':
            if (drawdown) {
                ctx.beginPath();
                ctx.clearRect(0, 0, 1000, 1000);
                if (convasData != null) {
                    ctx.putImageData(convasData, 0, 0, 0, 0, canvas.offsetWidth, canvas.offsetHeight);
                }
                ctx.moveTo(startPointX, startPointY);
                ctx.lineTo(e.offsetX, e.offsetY);
                ctx.closePath();
                ctx.strokeStyle = drawcolor;
                ctx.stroke();
            }
            break;
        case 'rect':
            if (drawdown) {
                ctx.beginPath();
                ctx.clearRect(0, 0, 1000, 1000);
                if (convasData != null) {
                    ctx.putImageData(convasData, 0, 0, 0, 0, canvas.offsetWidth, canvas.offsetHeight);
                }
                ctx.strokeStyle = drawcolor;
                ctx.strokeRect(startPointX, startPointY, e.offsetX - startPointX, e.offsetY - startPointY);
                ctx.closePath();
            }
            break;
        case 'ring':
            if (drawdown) {
                ctx.beginPath();
                ctx.clearRect(0, 0, 1000, 1000);
                if (convasData != null) {
                    ctx.putImageData(convasData, 0, 0, 0, 0, canvas.offsetWidth, canvas.offsetHeight);
                }
                ctx.strokeStyle = drawcolor;
                ctx.arc(startPointX, startPointY, (e.offsetY - startPointY) / 2, 0, 2 * Math.PI, false);
                ctx.stroke()
                ctx.closePath();
            }
            break;
        case 'text':
            if (drawdown) {
                ctx.beginPath();
                ctx.clearRect(0, 0, 1000, 1000);
                if (convasData != null) {
                    ctx.putImageData(convasData, 0, 0, 0, 0, canvas.offsetWidth, canvas.offsetHeight);
                }
                ctx.strokeStyle = '#000';
                ctx.strokeRect(startPointX, startPointY, e.offsetX - startPointX, e.offsetY - startPointY);
                ctx.closePath();
            }
        case 'eraser':
            if (drawdown) {
                ctx.beginPath();
                ctx.moveTo(startPointX, startPointY);
                ctx.clearRect(e.offsetX, e.offsetY, 50, 50);
            }
            break;
        default: return;
    }
}
var handleMouseUp = (e) => {
    if (curtool == 'text' && e.offsetX - startPointX >= 10 && e.offsetY - startPointY >= 10) {
        // ctx.clearRect(0, 0, 1000, 1000);
        let input = document.createElement('input');
        let canvasArea = document.getElementsByClassName('canvas-area')[0];
        canvasArea.appendChild(input);
        input.style.position = "absolute";
        input.style.left = `${startPointX}px`;
        input.style.top = `${startPointY}px`;
        input.style.width = `${e.offsetX - startPointX}px`;
        input.style.height = `${e.offsetY - startPointY}px`;
        input.style.fontSize = `${parseInt(input.style.height) / 2}px`;
        input.style.border = "2px dashed #ccc";
        input.style.outline = 'none'
        input.addEventListener('input', (e) => {
            textvalue = e.target.value
        })
        input.addEventListener('blur', () => {
            ctx.clearRect(0, 0, 1000, 1000);
            if (convasData != null) {
                ctx.putImageData(convasData, 0, 0, 0, 0, canvas.offsetWidth, canvas.offsetHeight);
            }
            ctx.font = `${parseInt(input.style.height) / 2}px sans-serif`;
            ctx.fillText(textvalue, parseInt(input.style.left) + 20, parseInt(input.style.top) + 0.6 * parseInt(input.style.height));
            canvasArea.removeChild(input);
            convasData = ctx.getImageData(0, 0, canvas.offsetWidth, canvas.offsetHeight);

        })

        drawdown = false;
    } else {
        convasData = ctx.getImageData(0, 0, canvas.offsetWidth, canvas.offsetHeight);
        drawdown = false;
    }

}
function restoreMouse() {
    canvas.removeEventListener('mousedown', handleMouseDown);
    canvas.removeEventListener('mousemove', handleMouseMove);
    canvas.removeEventListener('mouseup', handleMouseUp);
}
function pencilDraw() {
    setUsingTool('pencil');
    drawToolHandler('pencil');
}
function lineDraw() {
    setUsingTool('line');
    drawToolHandler('line');
}
function useEraser() {
    setUsingTool('eraser');
    drawToolHandler('eraser');
}
function RectDraw() {
    setUsingTool('rect');
    drawToolHandler('rect');
}
function circleDraw() {
    setUsingTool('ring');
    drawToolHandler('ring');
}
function insertText() {
    setUsingTool('text');
    drawToolHandler('text');
}
function handleColorChange(e) {
    console.log(e.value);
    drawcolor = e.value
}

function saveCanvas() {
    var a = document.createElement("a");
    a.href = canvas.toDataURL();
    var fileName = prompt("命名你的图画");
    a.download = fileName || "canvaspic"
    a.click();
}
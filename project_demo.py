from cmu_112_graphics import*
import math
def appStarted(app):
    app.scale = 3
    app.angle = 3
def redrawAll(app, canvas):
    canvas.create_polygon(0,app.height//app.scale,
    600,app.height//app.scale,
    600+app.height//app.scale*math.tan(math.pi/app.angle),0,
    0+app.height//app.scale*math.tan(math.pi/app.angle),0,fill="green")
    canvas.create_oval(300+math.tan(math.pi/app.angle)-10,300-10,
    300+math.tan(math.pi/app.angle)+1,300+10,fill="red")
def keyPressed(app, event):
    if event.key == 'Up':
        app.scale+=1
    elif event.key == 'Down':
        app.scale -=1 
    if event.key =="Left":
        app.angle-=1
    elif event.key == 'Right':
        app.angle+=1

runApp(width=1440, height=500)
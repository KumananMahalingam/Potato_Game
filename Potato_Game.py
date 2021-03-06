from tkinter import *
import random, sys
import os
from tkinter import Tk, Button

window = Tk()
window.title('The Potato Game')

canvas = Canvas(window, width=400, height=400, bg='black')
canvas.pack()

title = canvas.create_text(200,200, text='The Potato Game', fill='white', font=('Helvetica', 30))
directions = canvas.create_text(200,300, text='Collect food but avoid the green ones', fill='white', font=('Helvetica', 10))

score = 0
scoreDisplay = Label(window, text='Score:'+str(score))
scoreDisplay.pack()

level = 0
levelDisplay = Label(window, text='Level:'+str(level))
levelDisplay.pack()

playerImage = PhotoImage(file='Danny_Devito.png')

myDevito = canvas.create_image(200, 360, image=playerImage)

potatoList = []
badpotatoList = []
potatoSpeed = 2
potatoColorList = ['green', 'yellow', 'brown']

def makePotato():
  xposition = random.randint(1,400)
  potatoColor = random.choice(potatoColorList)
  potato = canvas.create_oval(xposition, 0, xposition + 30, 30, fill=potatoColor)
  potatoList.append(potato)
  if potatoColor=='green':
    badpotatoList.append(potato)
  window.after(2000, makePotato)

def movePotato():
  for potato in potatoList:
    canvas.move(potato, 0, potatoSpeed)
    if canvas.coords(potato)[1]>400:
      xposition = random.randint(1,400)
      canvas.coords(potato, xposition, 0, xposition + 30, 30)
  window.after(50, movePotato)

def updateScoreLevel():
  global score, level, potatoSpeed
  score = score+1
  scoreDisplay.config(text="Score:" + str(score))

  if score>5 and score<=10:
    potatoSpeed= potatoSpeed + 1
    level=2
    levelDisplay.config(text="Level:"+ str(level))

  if score>10 and score<=20:
    potatoSpeed = potatoSpeed + 1
    level=3
    levelDisplay.config(text="Level: "+ str(level))

  if score>20 and score<=25:
    potatoSpeed = potatoSpeed + 1
    level=4
    levelDisplay.config(text="Level: "+ str(level))

  if score>25:
    potatoSpeed = potatoSpeed + 5
    level=5
    levelDisplay.config(text="Level: "+ str(level))

def restart():
  window.destroy()
  os.system('python "Potato_Game.py"')

def endGame():
    window.destroy()
    sys.exit()

def endGameOver():
  Button(window, text="Restart", command=restart).pack()
  Button(window,text= "Quit", command=endGame).pack()

def endTitle():
  canvas.delete(title)
  canvas.delete(directions)

def collision(item1, item2, distance):
  xdistance=abs(canvas.coords(item1)[0]-canvas.coords(item2)[0])
  ydistance=abs(canvas.coords(item1)[1]-canvas.coords(item2)[1])
  overlap = xdistance < distance and ydistance < distance
  return overlap

def checkHits():
  for potato in badpotatoList:
    if collision(myDevito, potato, 30):
      gameOver = canvas.create_text(200,200, text='Game Over', fill='red', font=('Helvetica', 30))
      window.after(2000, endGameOver)
      return

  for potato in potatoList:
    if collision(myDevito, potato, 30):
      canvas.delete(potato)
      potatoList.remove(potato)
      updateScoreLevel()
  window.after(100,checkHits)

moveDirection = 0
def checkInput(event):
  global moveDirection
  key = event.keysym
  if key == 'Right':
    moveDirection = 'Right'
  elif key == 'Left':
    moveDirection = 'Left'



def endInput(event):
  global moveDirection
  moveDirection = 'None'

def moveCharacter():
  if moveDirection == "Right" and canvas.coords(myDevito)[0] <400:
    canvas.move(myDevito, 10, 0)
  if moveDirection == "Left" and canvas.coords(myDevito)[0] > 0:
    canvas.move(myDevito, -10, 0)
  window.after(16, moveCharacter)

canvas.bind_all('<KeyPress>', checkInput)
canvas.bind_all('<KeyRelease>', endInput)

window.after(1000, endTitle)
window.after(1000, makePotato)
window.after(1000, movePotato)
window.after(1000, checkHits)
window.after(1000, moveCharacter)

window.mainloop()
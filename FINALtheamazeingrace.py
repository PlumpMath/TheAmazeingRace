#!/usr/bin/env python

from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerPusher, CollisionSphere, CollisionTube
from panda3d.core import CollisionHandlerQueue, CollisionRay, CollisionBox
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import PandaNode, NodePath, Camera, TextNode
from panda3d.core import CollideMask, LPoint3, PointLight, LVector3, CardMaker, Vec3
from direct.stdpy import threading
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from panda3d.core import *
from panda3d.core import TextNode
#from direct.task import Task

#import direct.directbase.DirectStart
from direct.actor.Actor import Actor
import random
import sys
import os
import math
import utils

class RoamingRalphDemo(ShowBase):
    def __init__(self):
        # Set up the window, camera, etc.
        ShowBase.__init__(self)
        self.orbCollisionHandler = CollisionHandlerQueue()
        self.cTrav = CollisionTraverser()
        self.cTrav.setRespectPrevTransform(True)
        self.startgame = False
        self.sound=loader.loadSfx("models/0614.ogg")
        self.sound2=loader.loadSfx("models/01-main-theme.mp3")
        self.sound2.play()
        status=self.sound2.status()
        #hbPath = NodePath()
    
        utils.setUpKeys(self)
        utils.loadModels(self)
        utils.setUpLighting(self)
        #utils.setUpFloatingSpheres(self)
        utils.setUpRalphsShot(self)
        utils.setUpCamera(self)
        utils.setUpCollisionSpheres(self)
        self.healthTxt = utils.addInstructions(.06,"Health: 100")
        self.orbTxt = utils.addInstructions(.18,"Orbs: 0")
        self.hitsTxt = utils.addInstructions(.28,"Enemy Hits: 0")
        self.strHealthStatus = str(self.healthTxt)
        # Create a frame
        frame = DirectFrame(text = "main", scale = 0.001)
        # Add button
        self.flagstartbutton = 0        

        self.imageObject = OnscreenImage(image = 'models/instapage.jpg', pos = (0, 0, 0), scale=1.1)    
        self.imageObject2 = OnscreenImage(image = 'models/gap.jpg', pos = (-2.15, 0, 0), scale=1.1)
        self.imageObject3 = OnscreenImage(image = 'models/gap.jpg', pos = (2.15, 0, 0), scale=1.1)
        self.helpOn = DirectButton(text = ("Start", "on/off", "Start", "disabled"), scale=.10, pos=(-1.1,0,-.9), command=utils.buttonClickedOn, extraArgs=[self, self.imageObject,self.imageObject2,self.imageObject3, self.flagstartbutton])
        #helpOff = DirectButton(text = ("helpOff", "on/off", "helpOff", "disabled"), scale=.10, pos=(-0.5,0,-1), command=utils.buttonClickedOff, extraArgs=[self, self.imageObject, self.buttonflag])
      #  mytimer = DirectLabel()
      #  mytimer.reparentTo(render)
      #  mytimer.setY(7)        
        #Create 4 buttons       
        #print self.strHealthStatus
        #incBar(100)
    
        self.vec = LVector3(0,1,0)#vector for pawns shot

        # Create a frame
        #frame = DirectFrame(text = "main", scale = 0.001)
        # Add button
        #bar = DirectWaitBar(text = "", value = 50, pos = (0,.4,.4))
        #bar.reparent(render)

        # Game state variables
        self.isMoving = False
        self.jumping = False
        self.vz = 0
        self.numOrbs = 0
        self.healthCount = 100
        self.enemyhits = 0
    
        
        

        #self.shotList = []
        #self.sphere = CollisionBox((self.ralph.getX() + -10,self.ralph.getY(),self.ralph.getZ()),10,10,10)
        self.ralphBox1 = CollisionBox((0,2.5,3.5),1.5,0.5,1.5)
        cnodepath = self.ralph.attachNewNode((CollisionNode("ralphColNode")))
        cnodepath.node().addSolid(self.ralphBox1)
        cnodepath.node().addSolid(CollisionBox((0,-2.5,3.5),1.5,0.5,1.5))

        cnodepath.node().addSolid(CollisionBox((2.5,0,3.5),0.5,1.5,1.5))
        cnodepath.node().addSolid(CollisionBox((-2.5,0,3.5),0.5,1.5,1.5))

        #cnodepath.show()
        #self.cTrav.addCollider(cnodepath, self.orbCollisionHandler)

        self.sphere = CollisionSphere(0,-5,4,3)
        self.sphere3 = CollisionSphere(0,5,5,3)
        self.sphere4 = CollisionSphere(-4,0,5,2)
        self.sphere5 = CollisionSphere(4,0,5,2)
        self.sphere2 = CollisionSphere(0,0,3,2)
        self.cnodePath = self.ralph.attachNewNode((CollisionNode("ralphColNode")))
        self.cnodePath2 = self.ralph.attachNewNode((CollisionNode("ralphWallCheck")))
        self.cnodePath3 = self.ralph.attachNewNode((CollisionNode("ralphWallCheck2")))
        self.cnodePath4 = self.ralph.attachNewNode((CollisionNode("ralphWallCheck3")))
        self.cnodePath5 = self.ralph.attachNewNode((CollisionNode("ralphWallCheck4")))
        self.cnodePath.node().addSolid(self.sphere2)
        self.cnodePath2.node().addSolid(self.sphere)
        self.cnodePath3.node().addSolid(self.sphere3)
        self.cnodePath4.node().addSolid(self.sphere4)
        self.cnodePath5.node().addSolid(self.sphere5)
        #self.cnodePath.node().addSolid(self.sphere2)

        #self.cnodePath.show()#ralph pusher

        #self.cnodePath2.show()
        #self.cnodePath3.show()
        #self.cnodePath4.show()
        #self.cnodePath5.show()
        self.cTrav.addCollider(self.cnodePath2, self.orbCollisionHandler)
        self.cTrav.addCollider(self.cnodePath3, self.orbCollisionHandler)
        self.cTrav.addCollider(self.cnodePath4, self.orbCollisionHandler)
        self.cTrav.addCollider(self.cnodePath5, self.orbCollisionHandler)


        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.cnodePath, self.ralph)

        #self.cTrav.addCollider(self.cnodePath, self.ralphCollisionHandler)
        self.cTrav.addCollider(self.cnodePath, self.pusher)


        self.chrisLastShotTime = globalClock.getFrameTime()
        self.chrisTimer = globalClock.getDt()

        #def __init__(self, pos,showbase, colPathName, dir, length):
        self.chrisList = [utils.cheken((-249,419,0),self,"chrisColPath0","X",5), #earthroom
                            utils.chris((-404,343,2),self,"chrisColPath1","X",5), #yellowroom
                            utils.fetus((-141,-69,1),self,"chrisColPath2","X",5), #lightblueroom

                            utils.cheken((-277,356,0),self,"chrisColPath3","Y",5), #between earth and y
                            utils.rose((-102,-5,1),self,"chrisColPath4","Y",5), #between r and lb

                            utils.cheken((-133,83,0),self,"chrisColPath5","Y",5), #blue hall
                            utils.fetus((-246,280,1),self,"chrisColPath6","X",5), #earth hall

                            utils.cheken((-330,241,0),self,"chrisColPath7","X",5), #yellow hall
                            utils.chris((-60,110,2),self,"chrisColPath8","Y",5), #red hall cheken z 0

                            utils.fetus((-75,52,1),self, "chrisColPath9", "X", 5),
                            utils.cheken((-75,141,0),self, "chrisColPath10", "X", 5),

                          utils.rose((-302,202,1),self,"chrisColPath11","X",5),
                          utils.chris((-303,304,2),self,"chrisColPath12","Y",5)

                              
                         ]
        #rose z = 1
        #cheken z = 0
        #chris z = 2
        #fetus z = 1

        #def _init_(self,showbase,pos,color,speed,radius):
        self.orbList = [utils.orb(self,( 18, 29,2.5),(1,0,0,1),20,2.5), #first red
                        utils.orb(self,( -249, 419,2.5),(1,1,1,1),20,2.5),#earthroom
                        utils.orb(self,( -404, 343,2.5),(1,1,0,1),20,2.5), #yellowroom
                        utils.orb(self,( -141, -69,2.5),(0,0,1,1),20,2.5),#light blue room

                        utils.orb(self,( -277, 356,2.5),(1,1,0,1),20,2.5), #between y and earth
                        utils.orb(self,( -102, -5,2.5),(0,0,1,1),20,2.5),   #between red and lb

                        utils.orb(self,( -135, 22,2.5),(0,0,1,1),20,2.5), #lb hall
                        utils.orb(self,( -248, 329,2.5),(1,1,1,1),20,2.5), #earthhall

                        utils.orb(self,( -330, 241,2.5),(1,1,0,1),20,2.5), #yellow hall
                        utils.orb(self,( -60, 110,2.5),(1,0,0,1),20,2.5) #red hall
                         ]
        self.donutList = [utils.donut(self, (0,0,1),20, 2.5),
                          utils.donut(self,( -330, 250,2.5),20,2.5), #yellow hall
                          utils.donut(self,( -141, -80,2.5),20,2.5),#light blue room
                          utils.donut(self,( -249, 430,2.5),20,2.5),#earthroom
                          utils.donut(self,( -102, -10,2.5),20,2.5),   #between red and lb

                          ]

        self.cameraCollided = False
        self.ralphSpeed = 60
        self.ralphHit = False
        self.ralphRedTime = 0

        self.textTime = -1
        self.textTime2 = -1
        self.textTime3 = -1
        self.mTextPath = utils.addInstructions2(.44,"")
        self.mTextPath2 = utils.addInstructions2(.55,"")
        self.winText2 = utils.addInstructions2(.55, "")
        self.timerText = utils.addInstructions4(.26,"0:00")
        self.introText = utils.addInstructions2(.55,"")

        self.minutes = 4
        self.seconds = 0
        self.timerTime = globalClock.getFrameTime()

        taskMgr.add(self.move, "moveTask")
        taskMgr.add(self.moveChris,"moveChrisTask")
        taskMgr.add(self.timerTask,"timerTask")
        #taskMgr.add(self.timerTask, "timerTask")
        

    # Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value
    def clickResponse():
        pass
        #startgame=1;
        
        
    def timerTask(self,task):
        if self.startgame == False:
            return task.cont
        dt = globalClock.getFrameTime()
        if dt - self.timerTime > 1:
            self.seconds -= 1
            if self.seconds == -1:
                self.seconds = 59
                self.minutes -=1
            self.timerText.destroy()

            if self.seconds < 10:
                str1 = "0" + str(self.minutes) + ":0" + str(self.seconds)
            else:
                str1 = "0" + str(self.minutes) + ":" + str(self.seconds)
            self.timerText = utils.addInstructions4(.26,str1)
            self.timerTime = globalClock.getFrameTime() - ((dt - self.timerTime) - 1)
        if self.minutes == 0 and self.seconds == 0:
            self.startgame = False
            #utils.addInstructions3(.45,"You Lose")
            self.imageObject2 = OnscreenImage(image = 'models/gameover.jpg', pos = (0, 0, 0), scale=1.1)
            self.imageObject2 = OnscreenImage(image = 'models/gap.jpg', pos = (-2.15, 0, 0), scale=1.1)
            self.imageObject3 = OnscreenImage(image = 'models/gap.jpg', pos = (2.15, 0, 0), scale=1.1)
        return task.cont

    def moveChris(self,task):
        if self.startgame == False:
            return task.cont
        else:
            dt = globalClock.getDt()
            self.gianteye.setH(self.gianteye.getH() + 100 * dt)
            for chris in self.chrisList:
                chris.moveChris(dt,self,self.chrisList)
            return task.cont
    

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):

        if self.sound2.status() != self.sound2.PLAYING:
            self.sound2.play()

        if self.startgame == False:
            return task.cont
        else:
        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
            dt = globalClock.getDt()
            dt2 = globalClock.getFrameTime()
            #utils.moveChris(self,dt)
            #self.chris2.moveChris(dt,self)
            #self.startEnemyThread()

            if dt2 - self.textTime > 2 and self.textTime != -1:
                self.textTime = -1;
                self.mTextPath.destroy()

            if dt2 - self.textTime2 > 2 and self.textTime2 != -1:
                self.textTime2 = -1;
                self.mTextPath2.destroy()

            if dt2 - self.textTime3 > 5 and self.textTime3 != -1:
                self.textTime3 = -1;
                self.introText.destroy()



            if globalClock.getFrameTime()- self.ralphRedTime > .3 and self.ralphHit == True:
                    self.ralph.clearColor()
                    self.ralphHit = False

            # If the camera-left key is pressed, move camera left.
            # If the camera-right key is pressed, move camera right.

            if self.keyMap["cam-left"]:
                self.camera.setZ(self.camera, -20 * dt)
            if self.keyMap["cam-right"]:
                self.camera.setZ(self.camera, +20 * dt)

            # save ralph's initial position so that we can restore it,
            # in case he falls off the map or runs into something.

            startpos = self.ralph.getPos()

            # If a move-key is pressed, move ralph in the specified direction.

            if self.keyMap["left"]:
                self.ralph.setH(self.ralph.getH() + 75 * dt)
                #self.camera.setX(self.camera, +15.5 * dt)
            if self.keyMap["right"]:
                self.ralph.setH(self.ralph.getH() - 75 * dt)
                #self.camera.setX(self.camera, -15.5 * dt)
            if self.keyMap["forward"]:#-1
                self.ralph.setFluidY(self.ralph, -1*self.ralphSpeed * dt)
                #self.camera.setY(self.camera, -35 * dt)
            if self.keyMap["back"]:
                self.ralph.setFluidY(self.ralph, self.ralphSpeed * dt)
                #self.camera.setY(self.camera, 35 * dt)
            if self.keyMap["space"]:
                if self.jumping is False:
                #self.ralph.setZ(self.ralph.getZ() + 100 * dt)
                    self.jumping = True
                    self.vz = 8

            if self.keyMap["enter"]:
                self.keyMap["enter"] = False
                self.sound.play()
                self.shotList[self.shotCount].lpivot.setPos(self.ralph.getPos())
                self.shotList[self.shotCount].lpivot.setZ(self.ralph.getZ() + .5)
                self.shotList[self.shotCount].lpivot.setX(self.ralph.getX() - .25)
                print self.ralph.getPos()
                

                #self.shotList.append(rShot)
                #self.lightpivot3.setPos(self.ralph.getPos())
                #self.lightpivot3.setZ(self.ralph.getZ() + .5)
                #self.lightpivot3.setX(self.ralph.getX() - .25)
                #self.myShot.setHpr(self.ralph.getHpr())
                #parent to ralph
                #node = NodePath("tmp")
                #node.setHpr(self.ralph.getHpr())
                #vec = render.getRelativeVector(node,(0,-1,0))
                #self.myShotVec = vec

                node = NodePath("tmp")
                node.setHpr(self.ralph.getHpr())
                vec = render.getRelativeVector(node,(0,-1,0))
                self.shotList[self.shotCount].vec = vec
                self.shotCount = (self.shotCount + 1) % 10
            else:
                self.sound.stop()

            for rs in self.shotList:
                rs.lpivot.setPos(rs.lpivot.getPos() + rs.vec * dt * 25 )
                #if shot is too far stop updating


            
            if self.jumping is True:
                self.vz = self.vz - 16* dt
                self.ralph.setZ(self.ralph.getZ() + self.vz * dt )
                if self.ralph.getZ() < 0:
                    self.ralph.setZ(0)
                    self.jumping = False
            else:
                if self.ralph.getZ() < 0.25:
                    self.ralph.setZ(0.25)
                elif self.ralph.getZ() > 0.25:
                    self.ralph.setZ(self.ralph.getZ() -7 * dt)

            # If ralph is moving, loop the run animation.
            # If he is standing still, stop the animation.
            if self.keyMap["forward"] or self.keyMap["left"] or self.keyMap["right"] or self.keyMap["space"] or self.keyMap["forward"] or self.keyMap["back"]:
                if self.isMoving is False:
                    self.ralph.loop("run")
                    self.isMoving = True

            else:
                if self.isMoving:
                    self.ralph.stop()
                    self.ralph.pose("walk", 5)
                    self.isMoving = False

            # update pawns shot or set up new shot after it reaches a certain distance
            node = NodePath("tmp")
            node.setHpr(self.pawn.getHpr())
            vec = render.getRelativeVector(node,(random.random() * -0.8,random.random() + 1,0))
            self.shot.setPos(self.shot.getPos() + self.vec * dt * 10 )
            if self.shot.getY() < -15 or self.shot.getY() > 30 or self.shot.getX() < 5 or self.shot.getX() > 15:
                self.shot.setPos(self.pawn.getPos() + (0,0,0))
                self.vec = render.getRelativeVector(node,(random.random() * -0.8,random.random() + 1,0))
                self.vec = render.getRelativeVector(node,(random.random() * random.randrange(-1,2),random.random() + 1,0))

            # If the camera is too far from ralph, move it closer.
            # If the camera is too close to ralph, move it farther.
            #self.camera.lookAt(self.floater)
            camvec = self.ralph.getPos() - self.camera.getPos()
            #camvec = Vec3(0,camvec.getY(),0)
            camdist = camvec.length()
            x = self.camera.getZ()
            camvec.normalize()
            #if camdist > 6.0:
            #    self.camera.setPos(self.camera.getPos() + camvec * (camdist - 6))
            #if camdist < 6.0:
            #    self.camera.setPos(self.camera.getPos() - camvec * (6 - camdist))

            # Normally, we would have to call traverse() to check for collisions.
            # However, the class ShowBase that we inherit from has a task to do
            # this for us, if we assign a CollisionTraverser to self.cTrav.
            #self.cTrav.traverse(render)

            # Adjust camera so it stays at same height
            if self.cameraCollided == False:
                if self.camera.getZ() < self.ralph.getZ() + 1 or self.camera.getZ() > self.ralph.getZ() + 1:
                    self.camera.setZ(self.ralph.getZ() + 1)

            # The camera should look in ralph's direction,
            # but it should also try to stay horizontal, so look at
            # a floater which hovers above ralph's head.
            self.camera.lookAt(self.floater)


            entries = list(self.orbCollisionHandler.getEntries())
            if(len(entries) > 0):
                #self.lightpivot.reparentTo(NodePath())
                orbCollected = False
                self.cameraCollided = False
                self.ralphSpeed = 85
                ralphHit = False
                for entry in self.orbCollisionHandler.getEntries():
                    #print(entry)
                    fromColNp = entry.getFromNodePath()
                    toColNp = entry.getIntoNodePath()
                    if fromColNp.getName() == "orbColPath" and toColNp.getName() == "ralphColNode":
                        if orbCollected == False:
                            fromColNp.getParent().reparentTo(NodePath())
                            self.orbTxt.destroy()
                            self.numOrbs += 1
                            str1 = "Orbs: " + str(self.numOrbs)
                            self.orbTxt = utils.addInstructions(.18, str1)
                            orbCollected = True
                    elif toColNp.getName() == "orbColPath" and fromColNp.getName() == "ralphColNode":
                        if orbCollected == False:
                            toColNp.getParent().reparentTo(NodePath())
                            self.orbTxt.destroy()
                            self.numOrbs += 1
                            str1 = "Orbs: " + str(self.numOrbs)
                            self.orbTxt = utils.addInstructions(.18, str1)
                            orbCollected = True

                    elif fromColNp.getName() == "donutCollisionNode" and toColNp.getName() == "ralphColNode":
                        fromColNp.getParent().reparentTo(NodePath())
                        self.healthCount += 15
                        if(self.healthCount > 100):
                            self.healthCount = 100
                        self.healthTxt.destroy()
                        str1 = "Health: " + str(self.healthCount)
                        self.healthTxt = utils.addInstructions(.06, str1)
                    elif toColNp.getName() == "donutCollisionNode" and fromColNp.getName() == "ralphColNode":
                        toColNp.getParent().reparentTo(NodePath())
                        self.healthCount += 15
                        if(self.healthCount > 100):
                            self.healthCount = 100
                        self.healthTxt.destroy()
                        str1 = "Health: " + str(self.healthCount)
                        self.healthTxt = utils.addInstructions(.06, str1)
                    elif toColNp.getName() == "ralphOrbColPath" and (fromColNp.getName()[:-1] == "chrisColPath" or fromColNp.getName()[:-2] == "chrisColPath"):
                        toColNp.getParent().setZ(20)
                        for chriss in self.chrisList:
                            if chriss.chrisColName == fromColNp.getName():
                                chris = chriss
                                break

                        chris.chrisHealth = chris.chrisHealth - 1
                        chris.chris.setColor(1,0,0,1)
                        chris.chrisHit = True
                        chris.chrisRedTime = globalClock.getFrameTime()
                        #print chris.chrisRedTime
                        if chris.chrisHealth < 0 and chris.chrisAlive == True:
                            fromColNp.getParent().removeNode()
                            chris.chrisAlive = False
                            self.hitsTxt.destroy()
                            self.enemyhits += 1
                            str1 = "Enemy Hits: " + str(self.enemyhits)
                            self.hitsTxt = utils.addInstructions(.28, str1)
                            chris.chrisShot.setZ(26)
                    elif (toColNp.getName()[:-1] == "chrisColPath" or toColNp.getName()[:-2] == "chrisColPath") and fromColNp.getName() == "ralphOrbColPath":
                        fromColNp.getParent().setZ(20)
                        for chriss in self.chrisList:
                            if chriss.chrisColName == toColNp.getName():
                                chris = chriss
                                break

                        chris.chrisHealth = chris.chrisHealth - 1
                        chris.chris.setColor(1,0,0,1)
                        chris.chrisHit = True
                        chris.chrisRedTime = globalClock.getFrameTime()
                        #print chris.chrisRedTime
                        if chris.chrisHealth < 0 and chris.chrisAlive == True:
                            toColNp.getParent().removeNode()
                            chris.chrisAlive = False
                            self.hitsTxt.destroy()
                            self.enemyhits += 1
                            str1 = "Enemy Hits: " + str(self.enemyhits)
                            self.hitsTxt = utils.addInstructions(.28, str1)
                            chris.chrisShot.setZ(26)
                    elif toColNp.getName() == "enemyOrbColPath" and fromColNp.getName() == "ralphColNode":
                        if ralphHit == False:
                            toColNp.getParent().setZ(26)
                            self.healthTxt.destroy()
                            self.healthCount -= 5
                            str1 = "Health: " + str(self.healthCount)
                            self.healthTxt = utils.addInstructions(.06, str1)
                            self.ralphHit = True
                            self.ralph.setColor((1,0,0,1))
                            self.ralphRedTime = globalClock.getFrameTime()

                        if self.healthCount <= 0:
                            self.startgame = False
                            #utils.addInstructions3(.45,"You Lose")
                            self.imageObject2 = OnscreenImage(image = 'models/gameover.jpg', pos = (0, 0, 0), scale=1.1)
                            self.imageObject2 = OnscreenImage(image = 'models/gap.jpg', pos = (-2.15, 0, 0), scale=1.1)
                            self.imageObject3 = OnscreenImage(image = 'models/gap.jpg', pos = (2.15, 0, 0), scale=1.1)
                    elif toColNp.getName() == "ralphColNode" and fromColNp.getName() == "enemyOrbColPath":
                        fromColNp.getParent().setZ(26)
                        if ralphHit == False:
                            self.healthTxt.destroy()
                            self.healthCount -= 5
                            str1 = "Health: " + str(self.healthCount)
                            self.healthTxt = utils.addInstructions(.06, str1)
                            self.ralphHit = True
                            self.ralph.setColor((1,0,0,1))
                            self.ralphRedTime = globalClock.getFrameTime()
                            ralphHit = True

                        if self.healthCount <= 0:
                            self.startgame = False
                            #utils.addInstructions3(.45,"You Lose")
                            self.imageObject2 = OnscreenImage(image = 'models/gameover.jpg', pos = (0, 0, 0), scale=1.1)
                            self.imageObject2 = OnscreenImage(image = 'models/gap.jpg', pos = (-2.15, 0, 0), scale=1.1)
                            self.imageObject3 = OnscreenImage(image = 'models/gap.jpg', pos = (2.15, 0, 0), scale=1.1)
                    elif toColNp.getName() == "ralphColNode" and fromColNp.getName() == "portalColPath":
                        if self.numOrbs < 3 and self.enemyhits < 4:
                            self.mTextPath.destroy()
                            self.mTextPath = utils.addInstructions2(.30, "Not enough orbs.")
                            self.textTime = globalClock.getFrameTime()
                            self.mTextPath2.destroy()
                            self.mTextPath2 = utils.addInstructions2(.45, "Not enough kills.")
                            self.textTime2 = globalClock.getFrameTime()
                        elif self.numOrbs < 3:
                            self.mTextPath.destroy()
                            self.mTextPath = utils.addInstructions2(.30, "Not enough orbs.")
                            self.textTime = globalClock.getFrameTime()
                        elif self.enemyhits < 4:
                            self.mTextPath2.destroy()
                            self.mTextPath2 = utils.addInstructions2(.45, "Not enough kills.")
                            self.textTime2 = globalClock.getFrameTime()
                        else:
                            self.winText = utils.addInstructions3(.45, "You Win")
                            self.startgame = False
                            #self.ralph.setPos(-196, 177, 3)
                            if self.isMoving == True:
                                self.ralph.stop()
                                self.ralph.pose("walk", 5)
                                self.isMoving = False



                    elif fromColNp.getName() == "ralphOrbColPath" and toColNp.getName() == "allinclusive":
                        fromColNp.getParent().setZ(50)
                    elif toColNp.getName() == "ralphOrbColPath" and fromColNp.getName() == "allinclusive":
                        toColNp.getParent().setZ(50)
                    elif fromColNp.getName() == "enemyOrbWallCheck" and toColNp.getName() == "allinclusive":
                        fromColNp.getParent().setZ(50)
                        #print toColNp.getName()
                    elif toColNp.getName() == "enemyOrbWallCheck" and fromColNp.getName() == "allinclusive":
                        toColNp.getParent().setZ(50)
                        #print fromColNp.getName()

                    elif fromColNp.getName() == "ralphWallCheck" and toColNp.getName() == "allinclusive":
                        #node = NodePath("tmp")
                        #node.setHpr(self.ralph.getHpr())
                        #vec = render.getRelativeVector(node,(0,-1,0))
                        #self.ralph.setPos(self.ralph.getPos()-vec)
                        #fromColNp.getParent().setZ(26)
                        self.ralphSpeed = 60
                    elif toColNp.getName() == "ralphWallCheck" and fromColNp.getName() == "allinclusive":
                        #node = NodePath("tmp")
                        #node.setHpr(self.ralph.getHpr())
                        #vec = render.getRelativeVector(node,(0,-1,0))
                        #self.ralph.setPos(self.ralph.getPos()-vec)
                        #print "wtf"
                        #toColNp.getParent().setZ(26)
                        self.ralphSpeed = 60
                    elif fromColNp.getName() == "ralphWallCheck2" and toColNp.getName() == "allinclusive":
                        #node = NodePath("tmp")
                        #node.setHpr(self.ralph.getHpr())
                        #vec = render.getRelativeVector(node,(0,1,0))
                        #self.ralph.setPos(self.ralph.getPos()-vec)
                        #fromColNp.getParent().setZ(26)
                        self.ralphSpeed = 60
                    elif toColNp.getName() == "ralphWallCheck2" and fromColNp.getName() == "allinclusive":
                        #node = NodePath("tmp")
                        #node.setHpr(self.ralph.getHpr())
                        #vec = render.getRelativeVector(node,(0,1,0))
                        #self.ralph.setPos(self.ralph.getPos()-vec)
                        #self.camera.setPos(self.ralph.getPos())
                        #self.cameraCollided = True
                        self.ralphSpeed = 60
                    elif fromColNp.getName() == "ralphWallCheck3" and toColNp.getName() == "allinclusive":
                        #node = NodePath("tmp")
                        #node.setHpr(self.ralph.getHpr())
                        #vec = render.getRelativeVector(node,(-1,0,0))
                        #self.ralph.setPos(self.ralph.getPos()-vec)
                        #fromColNp.getParent().setZ(26)
                        self.ralphSpeed = 60
                        
                    elif toColNp.getName() == "ralphWallCheck3" and fromColNp.getName() == "allinclusive":
                        #node = NodePath("tmp")
                        #node.setHpr(self.ralph.getHpr())
                        #vec = render.getRelativeVector(node,(-1,0,0))
                        #self.ralph.setPos(self.ralph.getPos()-vec)
                        #self.camera.setPos(self.ralph.getPos())
                        #self.cameraCollided = True
                        self.ralphSpeed = 60
                        
                    elif fromColNp.getName() == "ralphWallCheck4" and toColNp.getName() == "allinclusive":
                        #node = NodePath("tmp")
                        #node.setHpr(self.ralph.getHpr())
                        #vec = render.getRelativeVector(node,(1,0,0))
                        #self.ralph.setPos(self.ralph.getPos()-vec)
                        #fromColNp.getParent().setZ(26)
                        self.ralphSpeed = 60
                        
                    elif toColNp.getName() == "ralphWallCheck4" and fromColNp.getName() == "allinclusive":
                        #node = NodePath("tmp")
                        #node.setHpr(self.ralph.getHpr())
                        #vec = render.getRelativeVector(node,(1,0,0))
                        #self.ralph.setPos(self.ralph.getPos()-vec)
                        #self.camera.setPos(self.ralph.getPos())
                        #self.cameraCollided = True
                        self.ralphSpeed = 60
                        

            utils.updateHealthBar(self.healthCount, self.bar)
            #utils.turnofstartbutton(self.flagstartbutton)
            #if self.flagstartbutton ==1:
            #    self.helpOn.destory()
            return task.cont
demo = RoamingRalphDemo()
demo.run()


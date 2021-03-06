#!/usr/bin/env python

from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerPusher, CollisionSphere, CollisionTube
from panda3d.core import CollisionHandlerQueue, CollisionRay, CollisionBox
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import PandaNode, NodePath, Camera, TextNode
from panda3d.core import CollideMask, LPoint3, PointLight, LVector3, CardMaker, Vec3
from direct.stdpy import threading



from direct.actor.Actor import Actor
import random
import sys
import os
import math
import utilsKristina2

class RoamingRalphDemo(ShowBase):
    def __init__(self):
        # Set up the window, camera, etc.
        ShowBase.__init__(self)
        self.orbCollisionHandler = CollisionHandlerQueue()
        self.cTrav = CollisionTraverser()
        self.cTrav.setRespectPrevTransform(True)

        #hbPath = NodePath()

        utilsKristina2.setUpKeys(self)
        utilsKristina2.loadModels(self)
        utilsKristina2.setUpLighting(self)
        utilsKristina2.setUpFloatingSpheres(self)
        utilsKristina2.setUpRalphsShot(self)
        utilsKristina2.setUpCamera(self)
        utilsKristina2.setUpCollisionSpheres(self)
        self.healthTxt = utilsKristina2.addInstructions(.06,"Health: 100")
        self.orbTxt = utilsKristina2.addInstructions(.18,"Orbs: 0")

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

        #self.shotList = []




        #self.sphere = CollisionBox((self.ralph.getX() + -10,self.ralph.getY(),self.ralph.getZ()),10,10,10)
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
        self.cnodePath.show()
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
        self.chrisList = [utilsKristina2.chris((15,0,0.5),self,"chrisColPath0","X",6), utilsKristina2.chris((18,29,0.5),self,"chrisColPath1","X",6),
                          utilsKristina2.chris((-6,67,0.5),self,"chrisColPath2","X",6), utilsKristina2.chris((-41,72,0.5),self,"chrisColPath7","X",6)]
                          #,utilsKristina2.chris((-42,106,0.5),self,"chrisColPath3","X",6)]#, utilsKristina2.chris((-62,108,0.5),self,"chrisColPath4","X",6),
                          #utilsKristina2.chris((-74,70,0.5),self,"chrisColPath5","y",6)]
        #def _init_(self,showbase,pos,color,speed,radius):
        self.orbList = [utilsKristina2.orb(self,(0,0,2),(0,0,1,1),20,4)]

        self.donutList = [utilsKristina2.donut(self,(0,0,2),40,3)]

        self.cameraCollided = False
        self.ralphSpeed = 60
        self.ralphHit = False
        self.ralphRedTime = 0
        self.ralphLife=True

        taskMgr.add(self.move, "moveTask")
        taskMgr.add(self.moveChris,"moveChrisTask")

    # Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value


    def startEnemyThread(self):
        showbase = self
        class enemyThread(threading.Thread):
            def run(self):
                dt = globalClock.getDt()
                for chris in showbase.chrisList:
                    chris.moveChris(dt,showbase,showbase.chrisList)

    def moveChris(self,task):
        dt = globalClock.getDt()
        for chris in self.chrisList:
            chris.moveChris(dt,self,self.chrisList)
        return task.cont

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):



        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
        dt = globalClock.getDt()
        #utilsKristina2.moveChris(self,dt)
        #self.chris2.moveChris(dt,self)
        #self.startEnemyThread()


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
        if self.keyMap["forward"]:
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

        if self.keyMap["c"] or self.keyMap["enter"]:
            if self.keyMap["c"]:
                self.keyMap["c"]=False
            if self.keyMap["enter"]:
                self.keyMap["enter"] = False
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
            self.ralphSpeed = 65
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
                        self.orbTxt = utilsKristina2.addInstructions(.18, str1)
                        orbCollected = True
                elif toColNp.getName() == "orbColPath" and fromColNp.getName() == "ralphColNode":
                    if orbCollected == False:
                        toColNp.getParent().reparentTo(NodePath())
                        self.orbTxt.destroy()
                        self.numOrbs += 1
                        str1 = "Orbs: " + str(self.numOrbs)
                        self.orbTxt = utilsKristina2.addInstructions(.18, str1)
                        orbCollected = True
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
                    if chris.chrisHealth < 0:
                        fromColNp.getParent().removeNode()
                        chris.chrisAlive = False
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
                    if chris.chrisHealth < 0:
                        toColNp.getParent().removeNode()
                        chris.chrisAlive = False
                        chris.chrisShot.setZ(26)
                elif toColNp.getName() == "enemyOrbColPath" and fromColNp.getName() == "ralphColNode":
                    toColNp.getParent().setZ(26)
                    self.healthTxt.destroy()
                    self.healthCount -= 3
                    str1 = "Health: " + str(self.healthCount)
                    self.healthTxt = utilsKristina2.addInstructions(.06, str1)
                    self.ralphHit = True
                    self.ralph.setColor((1,0,0,1))
                    self.ralphRedTime = globalClock.getFrameTime()
                    if self.healthCount <=0:
                        sys.exit()
                elif toColNp.getName() == "ralphColNode" and fromColNp.getName() == "enemyOrbColPath":
                    fromColNp.getParent().setZ(26)
                    self.healthTxt.destroy()
                    self.healthCount -= 3
                    str1 = "Health: " + str(self.healthCount)
                    self.healthTxt = utilsKristina2.addInstructions(.06, str1)
                    self.ralphHit = True
                    self.ralph.setColor((1,0,0,1))
                    self.ralphRedTime = globalClock.getFrameTime()
                    if self.healthCount <=0:
                        sys.exit()
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
                    self.ralphSpeed = 25
                elif toColNp.getName() == "ralphWallCheck" and fromColNp.getName() == "allinclusive":
                    #node = NodePath("tmp")
                    #node.setHpr(self.ralph.getHpr())
                    #vec = render.getRelativeVector(node,(0,-1,0))
                    #self.ralph.setPos(self.ralph.getPos()-vec)
                    #print "wtf"
                    #toColNp.getParent().setZ(26)
                    self.ralphSpeed = 25
                elif fromColNp.getName() == "ralphWallCheck2" and toColNp.getName() == "allinclusive":
                    #node = NodePath("tmp")
                    #node.setHpr(self.ralph.getHpr())
                    #vec = render.getRelativeVector(node,(0,1,0))
                    #self.ralph.setPos(self.ralph.getPos()-vec)
                    #fromColNp.getParent().setZ(26)
                    self.ralphSpeed = 25
                elif toColNp.getName() == "ralphWallCheck2" and fromColNp.getName() == "allinclusive":
                    #node = NodePath("tmp")
                    #node.setHpr(self.ralph.getHpr())
                    #vec = render.getRelativeVector(node,(0,1,0))
                    #self.ralph.setPos(self.ralph.getPos()-vec)
                    #self.camera.setPos(self.ralph.getPos())
                    #self.cameraCollided = True
                    self.ralphSpeed = 25
                elif fromColNp.getName() == "ralphWallCheck3" and toColNp.getName() == "allinclusive":
                    #node = NodePath("tmp")
                    #node.setHpr(self.ralph.getHpr())
                    #vec = render.getRelativeVector(node,(-1,0,0))
                    #self.ralph.setPos(self.ralph.getPos()-vec)
                    #fromColNp.getParent().setZ(26)
                    self.ralphSpeed = 25
                    print "3"
                elif toColNp.getName() == "ralphWallCheck3" and fromColNp.getName() == "allinclusive":
                    #node = NodePath("tmp")
                    #node.setHpr(self.ralph.getHpr())
                    #vec = render.getRelativeVector(node,(-1,0,0))
                    #self.ralph.setPos(self.ralph.getPos()-vec)
                    #self.camera.setPos(self.ralph.getPos())
                    #self.cameraCollided = True
                    self.ralphSpeed = 25
                    print "3"
                elif fromColNp.getName() == "ralphWallCheck4" and toColNp.getName() == "allinclusive":
                    #node = NodePath("tmp")
                    #node.setHpr(self.ralph.getHpr())
                    #vec = render.getRelativeVector(node,(1,0,0))
                    #self.ralph.setPos(self.ralph.getPos()-vec)
                    #fromColNp.getParent().setZ(26)
                    self.ralphSpeed = 25
                    print "4"
                elif toColNp.getName() == "ralphWallCheck4" and fromColNp.getName() == "allinclusive":
                    #node = NodePath("tmp")
                    #node.setHpr(self.ralph.getHpr())
                    #vec = render.getRelativeVector(node,(1,0,0))
                    #self.ralph.setPos(self.ralph.getPos()-vec)
                    #self.camera.setPos(self.ralph.getPos())
                    #self.cameraCollided = True
                    self.ralphSpeed = 25
                    print "4"





        return task.cont




demo = RoamingRalphDemo()
demo.run()


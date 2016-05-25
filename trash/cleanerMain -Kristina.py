#!/usr/bin/env python

from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerPusher, CollisionSphere, CollisionTube
from panda3d.core import CollisionHandlerQueue, CollisionRay, CollisionBox
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import PandaNode, NodePath, Camera, TextNode
from panda3d.core import CollideMask, LPoint3, PointLight, LVector3, CardMaker, Vec3



from direct.actor.Actor import Actor
import random
import sys
import os   
import math
import utilsKristina

class RoamingRalphDemo(ShowBase):
    def __init__(self):
        # Set up the window, camera, etc.
        ShowBase.__init__(self)
        self.orbCollisionHandler = CollisionHandlerQueue()
        self.cTrav = CollisionTraverser()

        #hbPath = NodePath()

        utilsKristina.HealthBar()
        utilsKristina.setUpKeys(self)
        utilsKristina.loadModels(self)
        utilsKristina.setUpLighting(self)
        utilsKristina.setUpFloatingSpheres(self)
        utilsKristina.setUpRalphsShot(self)
        utilsKristina.setUpCamera(self)
        utilsKristina.setUpCollisionSpheres(self)
        self.healthTxt = utilsKristina.addInstructions(.06,"Health: 100")
        self.orbTxt = utilsKristina.addInstructions(.18,"Orbs: 0")

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
        taskMgr.add(self.move, "moveTask")
        #taskMgr.add(utils2.moveChris,"moveChrisTask")
        
        self.sphere = CollisionSphere(0,0,4,2)
        self.sphere2 = CollisionSphere(0,0,2,2)
        self.cnodePath = self.ralph.attachNewNode((CollisionNode('ralphColNode')))
        self.cnodePath.node().addSolid(self.sphere)
        self.cnodePath.node().addSolid(self.sphere2)
        #self.cnodePath.show()
        
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.cnodePath, self.ralph)

        #self.cTrav.addCollider(self.cnodePath, self.ralphCollisionHandler)
        self.cTrav.addCollider(self.cnodePath, self.pusher)

        # Uncomment this line to show a visual representation of the
        # collisions occuring
        self.cTrav.showCollisions(render)

        self.chrisLastShotTime = globalClock.getFrameTime()
        self.chrisTimer = globalClock.getDt()

    # Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):


        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        temp=utilsKristina.HealthBar()
        # in order to achieve that desired speed.
        dt = globalClock.getDt()
        utilsKristina.moveChris(self,dt)

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
            self.ralph.setH(self.ralph.getH() + 150 * dt)
            #self.camera.setX(self.camera, +15.5 * dt)
        if self.keyMap["right"]:
            self.ralph.setH(self.ralph.getH() - 150 * dt)
            #self.camera.setX(self.camera, -15.5 * dt)
        if self.keyMap["forward"]:
            self.ralph.setY(self.ralph, -35 * dt)
            #self.camera.setY(self.camera, -35 * dt)
        if self.keyMap["back"]:
            self.ralph.setY(self.ralph, +35 * dt)
            #self.camera.setY(self.camera, 35 * dt)
        if self.keyMap["space"]:
            if self.jumping is False:
            #self.ralph.setZ(self.ralph.getZ() + 100 * dt)
                self.jumping = True
                self.vz = 7

        if self.keyMap["enter"]:
            self.keyMap["enter"] = False
            self.shotList[self.shotCount].lpivot.setPos(self.ralph.getPos())
            self.shotList[self.shotCount].lpivot.setZ(self.ralph.getZ() + .5)
            self.shotList[self.shotCount].lpivot.setX(self.ralph.getX() - .25)

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
            self.shotCount = (self.shotCount + 1) % 5


        for rs in self.shotList:
            rs.lpivot.setPos(rs.lpivot.getPos() + rs.vec * dt * 15 )
            #if shot is too far stop updating



        if self.jumping is True:
            self.vz = self.vz - 16* dt
            self.ralph.setZ(self.ralph.getZ() + self.vz * dt )
            if self.ralph.getZ() < 0:
                self.ralph.setZ(0)
                self.jumping = False
        else:
            if self.ralph.getZ() < 0:
                self.ralph.setZ(0)
            elif self.ralph.getZ() > 0:
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
        if self.camera.getZ() < self.ralph.getZ() + 1 or self.camera.getZ() > self.ralph.getZ() + 1:
            self.camera.setZ(self.ralph.getZ() + 1)

        # The camera should look in ralph's direction,
        # but it should also try to stay horizontal, so look at
        # a floater which hovers above ralph's head.
        self.camera.lookAt(self.floater)


        entries = list(self.orbCollisionHandler.getEntries())
        if(len(entries) > 0):
            #self.lightpivot.reparentTo(NodePath())
            for entry in self.orbCollisionHandler.getEntries():
                #print(entry)
                fromColNp = entry.getFromNodePath()
                toColNp = entry.getIntoNodePath()
                if fromColNp.getName() == "orbColPath" and toColNp.getName() == "ralphColNode":
                    fromColNp.getParent().reparentTo(NodePath())
                    self.orbTxt.destroy()
                    self.numOrbs += 1
                    str1 = "Orbs: " + str(self.numOrbs)
                    self.orbTxt = utilsKristina.addInstructions(.18, str1)
                elif toColNp.getName() == "orbColPath" and fromColNp.getName() == "ralphColNode":
                    toColNp.getParent().reparentTo(NodePath())
                    self.orbTxt.destroy()
                    self.numOrbs += 1
                    str1 = "Orbs: " + str(self.numOrbs)
                    self.orbTxt = utilsKristina.addInstructions(.18, str1)
                elif fromColNp.getName() == "donutCollisionNode" and toColNp.getName() == "ralphColNode":
                    fromColNp.getParent().reparentTo(NodePath())
                    #self.healthTxt.destroy()
                    #self.healthCount += 3
                    #str1 = "Health: " + str(self.healthCount)
                    #self.healthTxt = utilsKristina.addInstructions(.06, str1)
                elif toColNp.getName() == "donutCollisionNode" and fromColNp.getName() == "ralphColNode":
                    toColNp.getParent().reparentTo(NodePath())
                    #self.healthTxt.destroy()
                    #self.healthCount += 3
                    #str1 = "Health: " + str(self.healthCount)
                    #self.healthTxt = utilsKristina.addInstructions(.06, str1)
                elif toColNp.getName() == "ralphOrbColPath" and fromColNp.getName() == "chrisColPath":
                    toColNp.getParent().setPos(-50,0,2)
                    self.chrisHealth = self.chrisHealth - 1
                    self.chris.setColor(1,0,0,1)
                    self.chrisHit = True
                    self.chrisRedTime = globalClock.getFrameTime()
                    #print self.chrisRedTime
                    if self.chrisHealth < 0:
                        fromColNp.getParent().removeNode()
                        self.chrisAlive = False
                elif toColNp.getName() == "chrisColPath" and fromColNp.getName() == "ralphOrbColPath":
                    fromColNp.getParent().setPos(-50,0,2)
                    self.chrisHealth = self.chrisHealth - 1
                    self.chris.setColor(1,0,0,1)
                    self.chrisHit = True
                    self.chrisRedTime = globalClock.getFrameTime()
                    #print self.chrisRedTime
                    if self.chrisHealth < 0:
                        fromColNp.getParent().removeNode()
                        self.chrisAlive = False
                        self.chrisShot.setZ(26)
                elif toColNp.getName() == "enemyOrbColPath" and fromColNp.getName() == "ralphColNode":
                    toColNp.getParent().setZ(26)
                    self.healthTxt.destroy()
                    self.healthCount -= 3
                    temp.setHealth(100)
                    str1 = "Health: " + str(self.healthCount)
                    self.healthTxt = utilsKristina.addInstructions(.06, str1)
                elif toColNp.getName() == "ralphColNode" and fromColNp.getName() == "enemyOrbColPath":
                    fromColNp.getParent().setZ(26)
                    self.healthTxt.destroy()
                    self.healthCount -= 3
                    temp.setHealth(100)
                    str1 = "Health: " + str(self.healthCount)
                    self.healthTxt = utilsKristina.addInstructions(.06, str1)



        return task.cont




demo = RoamingRalphDemo()
demo.run()

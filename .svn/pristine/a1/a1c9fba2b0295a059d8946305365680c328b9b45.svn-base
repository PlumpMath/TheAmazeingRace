#!/usr/bin/env python

# Author: Ryan Myers
# Models: Jeff Styers, Reagan Heller
#
# Last Updated: 2015-03-13
#
# This tutorial provides an example of creating a character
# and having it walk around on uneven terrain, as well
# as implementing a fully rotatable camera.

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerPusher, CollisionSphere, CollisionTube
from panda3d.core import CollisionHandlerQueue, CollisionRay,CollisionSegment
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import PandaNode, NodePath, Camera, TextNode
from panda3d.core import Point3,Vec3,Vec4,BitMask32
from panda3d.core import CollideMask, LPoint3, PointLight, LVector3
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
import random
import sys
import os
import math

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1, 1, 1, 1), scale=.07,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        pos=(-0.1, 0.09), shadow=(0, 0, 0, 1))


class RoamingRalphDemo(ShowBase):
    def __init__(self):
        # Set up the window, camera, etc.
        ShowBase.__init__(self)

        # Set the background color to black
        self.win.setClearColor((0.6, 0.6, 1.0, 1.0))

        # This is used to store which keys are currently pressed.
        self.keyMap = {
            "left": 0, "right": 0, "forward": 0,"cam-left":0,"cam-right":0, "zoom-in":0, "zoom-out":0, "wheel-in":0,"wheel-out":0,
            "c":0, "back":0, "space":0}
        self.mousebtn = [0,0,0];

        # Post the instructions
        #self.title = addTitle(
        #   "Panda3D Tutorial: Roaming Ralph (Walking on Uneven Terrain)")
        self.inst1 = addInstructions(0.06, "[ESC]: Quit")
        self.inst2 = addInstructions(0.12, "[Left Arrow]: Rotate Ralph Left")
        self.inst3 = addInstructions(0.18, "[Right Arrow]: Rotate Ralph Right")
        self.inst4 = addInstructions(0.24, "[Up Arrow]: Run Ralph Forward")
        #self.inst6 = addInstructions(0.30, "[A]: Rotate Camera Left")
        #self.inst7 = addInstructions(0.36, "[S]: Rotate Camera Right")


        # Set up the environment
        #
        # This environment model contains collision meshes.  If you look
        # in the egg file, you will see the following:
        #
        #    <Collide> { Polyset keep descend }
        #
        # This tag causes the following mesh to be converted to a collision
        # mesh -- a mesh which is optimized for collision, not rendering.
        # It also keeps the original mesh, so there are now two copies ---
        # one optimized for rendering, one for collisions.

        #self.environ = loader.loadModel("models/world")
        #self.environ.reparentTo(render)

        self.room = loader.loadModel("models/room2.egg")
        self.room.reparentTo(render)
        #self.room.setScale(.1)
        self.room.setPos(0,0,-5)
        self.room.setShaderAuto()
        #self.room.writeBamFile("myRoom1.bam")
        #self.room.setColor(1,.3,.3,1)

        self.room2 = loader.loadModel("models/abstractroom2")
        self.room2.reparentTo(render)
        self.room2.setScale(.1)
        self.room2.setPos(-12,0,0)

        # Create the main character, Ralph

        #ralphStartPos = LVecBase3F(0,0,0) #self.room.find("**/start_point").getPos()

        self.ralph = Actor("models/chik"
                          )
        self.ralph.reparentTo(render)
        self.ralph.setScale(.2)
        self.ralph.setPos(0,0,0)
    
        self.gianteye = loader.loadModel("models/gianteye")
        self.gianteye.reparentTo(render)
        self.gianteye.setScale(.1)
        self.gianteye.setPos(10,10,0)   
    
    #self.blue = loader.loadModel("models/blue1")
    #self.blue.reparentTo(render)
    #self.blue.setScale(.1)
    #self.blue.setPos(10,5,0)
    
        self.chik = loader.loadModel("models/chik")
        self.chik.reparentTo(render)
        self.chik.setScale(.1)
        self.chik.setPos(3,13,0)    

        self.pawn = loader.loadModel("pawn")
        self.pawn.reparentTo(render)
        self.pawn.setPos(0,0,0)

        self.shot = loader.loadModel("models/icosphere.egg")
        self.shot.reparentTo(render)
        self.shot.setScale(.5)
        self.shot.setPos(0,0,1)
        self.shot.setColor(1,.3,.3,1)

        self.myShot = loader.loadModel("models/icosphere.egg")
        #self.myShot.reparentTo(render)
        self.myShot.setScale(.1)
        self.myShot.setPos(0,0,1)
        self.myShotVec = LVector3(0,0,0)

        self.lightpivot3 = render.attachNewNode("lightpivot3")
        self.lightpivot3.setPos(0, 0, 0)
        self.lightpivot3.hprInterval(10, LPoint3(0, 0, 0)).loop()
        plight3 = PointLight('plight2')
        plight3.setColor((0, .3,0, 1))
        plight3.setAttenuation(LVector3(0.7, 0.05, 0))
        plnp3 = self.lightpivot3.attachNewNode(plight3)
        plnp3.setPos(0, 0, 0)
        self.room2.setLight(plnp3)
        self.room.setLight(plnp3)
        sphere3 = loader.loadModel("models/icosphere")
        sphere3.reparentTo(plnp3)
        sphere3.setScale(0.1)
        sphere3.setColor((0,1,0,1))

        # Create a floater object, which floats 2 units above ralph.  We
        # use this as a target for the camera to look at.

        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(self.ralph)
        self.floater.setZ(8.0)

        # Accept the control keys for movement and rotation

        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.setKey, ["left", 1])
        self.accept("arrow_right", self.setKey, ["right", 1])
        self.accept("arrow_up", self.setKey, ["forward", 1])
        self.accept("arrow_down", self.setKey, ["back", 1])
        self.accept("a", self.setKey, ["cam-left", True])
        self.accept("s", self.setKey, ["cam-right", True])
        self.accept("arrow_left-up", self.setKey, ["left", 0])
        self.accept("arrow_right-up", self.setKey, ["right", 0])
        self.accept("arrow_up-up", self.setKey, ["forward", 0])
        self.accept("arrow_down-up", self.setKey, ["back", 0])
        self.accept("a-up", self.setKey, ["cam-left", False])
        self.accept("s-up", self.setKey, ["cam-right", False])
        self.accept("wheel_up", self.setKey, ["wheel-in", 1])
        self.accept("wheel_down", self.setKey, ["wheel-out", 1])
        #self.accept("page_up", self.setKey, ["zoom-in", 1])
        #self.accept("page_up-up", self.setKey, ["zoom-in", 0])
        #self.accept("page_down", self.setKey, ["zoom-out", 1])
        #self.accept("page_down-up", self.setKey, ["zoom-out", 0])
    

        self.accept("space", self.setKey, ["space", True])
        self.accept("space-up", self.setKey, ["space", False])

        self.accept("c",self.setKey,["c",True])
        self.accept("c-up",self.setKey,["c",False])

        taskMgr.add(self.move, "moveTask")

        # Game state variables
        self.isMoving = False
        self.jumping = False
        self.vz = 0

        # Set up the camera
        base.camera.reparentTo(self.ralph)
        self.cameraTargetHeight = 6.0
        # How far should the camera be from Ralph
        self.cameraDistance = 30
        # Initialize the pitch of the camera
        self.cameraPitch = 10
        self.disableMouse()
        self.camera.setPos(self.ralph.getX(), self.ralph.getY() + 7, 3)
        self.camLens.setFov(60)
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        # We will detect the height of the terrain by creating a collision
        # ray and casting it downward toward the terrain.  One ray will
        # start above ralph's head, and the other will start above the camera.
        # A ray may hit the terrain, or it may hit a rock or a tree.  If it
        # hits the terrain, we can detect the height.  If it hits anything
        # else, we rule that the move is illegal.

        #def setupCollision(self):
        #cs = CollisionSphere(0,0,2,1)
        #cnodePath = self.ralph.attachNewNode(CollisionNode('cnode'))
        #cnodePath.node().addSolid(cs)
        #cnodePath.show()

        #for o in self.OBS:
        #   ct = CollisionTube(0,0,0, 0,0,1, 0.5)
        #   cn = o.attachNewNode(CollisionNode('ocnode'))
        #   cn.node().addSolid(ct)
        #   cn.show()

        #pusher = CollisionHandlerPusher()
        #pusher.addCollider(cnodePath, self.player)
        #self.cTrav = CollisionTraverser()
        #self.cTrav.add_collider(cnodePath,pusher)
        #self.cTrav.showCollisions(render)


        self.cTrav = CollisionTraverser()



        self.ralphGroundRay = CollisionRay()
        self.ralphGroundRay.setOrigin(0, 0, 9)
        self.ralphGroundRay.setDirection(0, 0, -1)
        self.ralphGroundCol = CollisionNode('ralphRay')
        self.ralphGroundCol.addSolid(self.ralphGroundRay)
        self.ralphGroundCol.setFromCollideMask(CollideMask.bit(0))
        self.ralphGroundCol.setIntoCollideMask(CollideMask.allOff())
        self.ralphGroundColNp = self.ralph.attachNewNode(self.ralphGroundCol)
        self.ralphGroundHandler = CollisionHandlerQueue()

        self.cTrav.addCollider(self.ralphGroundColNp, self.ralphGroundHandler)

        self.camGroundRay = CollisionRay()
        self.camGroundRay.setOrigin(0, 0, 9)
        self.camGroundRay.setDirection(0, 0, -1)
        self.camGroundCol = CollisionNode('camRay')
        self.camGroundCol.addSolid(self.camGroundRay)
        self.camGroundCol.setFromCollideMask(CollideMask.bit(0))
        self.camGroundCol.setIntoCollideMask(CollideMask.allOff())
        self.camGroundColNp = self.camera.attachNewNode(self.camGroundCol)
        self.camGroundHandler = CollisionHandlerQueue()

        self.cTrav.addCollider(self.camGroundColNp, self.camGroundHandler)

        self.sphere = CollisionSphere(0,0,4,2)
        self.sphere2 = CollisionSphere(0,0,2,2)
        self.cnodePath = self.ralph.attachNewNode((CollisionNode('cnode')))
        self.cnodePath.node().addSolid(self.sphere)
        self.cnodePath.node().addSolid(self.sphere2)
        self.cnodePath.show()
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.cnodePath, self.ralph)
        self.cTrav.add_collider(self.cnodePath, self.pusher)

        
        self.cameraRay = CollisionSegment((0,0,self.cameraTargetHeight),(0,5,5))
        self.cameraCol = CollisionNode('cameraRay')
        self.cameraCol.addSolid(self.cameraRay)
        self.cameraCol.setFromCollideMask(BitMask32.bit(0))
        self.cameraCol.setIntoCollideMask(BitMask32.allOff())
        self.cameraColNp = self.ralph.attachNewNode(self.cameraCol)
        self.cameraColHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.cameraColNp, self.cameraColHandler)


        # Uncomment this line to see the collision rays
        self.ralphGroundColNp.show()
        self.camGroundColNp.show()

        # Uncomment this line to show a visual representation of the
        # collisions occuring
        #self.cTrav.showCollisions(render)

        # Create some lighting
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.3, .3, .3, .4))
        ambientLight2 = AmbientLight("ambientLight2")
        ambientLight2.setColor((1, 1, 1, 10))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection((0, 0, -2))
        directionalLight.setColor((1, 1, 1, 1))
        directionalLight.setSpecularColor((1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        #self.environ.setLight(self.environ.attachNewNode(ambientLight2))
        render.setLight(render.attachNewNode(directionalLight))

        # Add a light to the scene.
        self.lightpivot = render.attachNewNode("lightpivot")
        self.lightpivot.setPos(0, 0, 1.6)
        self.lightpivot.hprInterval(20, LPoint3(360, 0, 0)).loop()
        plight = PointLight('plight')
        plight.setColor((.7, .3, 0, 1))
        plight.setAttenuation(LVector3(0.7, 0.05, 0))
        plnp = self.lightpivot.attachNewNode(plight)
        plnp.setPos(5, 0, 0)
        self.room.setLight(plnp)
        sphere = loader.loadModel("models/icosphere")
        sphere.reparentTo(plnp)
        sphere.setScale(0.1)
        sphere.setColor((1,1,0,1))

        self.lightpivot2 = render.attachNewNode("lightpivot")
        self.lightpivot2.setPos(-16, 0, 1.6)
        self.lightpivot2.hprInterval(20, LPoint3(360, 0, 0)).loop()
        plight2 = PointLight('plight2')
        plight2.setColor((0, .4,.8, 1))
        plight2.setAttenuation(LVector3(0.7, 0.05, 0))
        plnp2 = self.lightpivot2.attachNewNode(plight2)
        plnp2.setPos(5, 0, 0)
        self.room2.setLight(plnp2)
        sphere2 = loader.loadModel("models/icosphere")
        sphere2.reparentTo(plnp2)
        sphere2.setScale(0.2)
        sphere2.setColor((0,0,1,1))

        self.vec = LVector3(0,1,0)

    # Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):

        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
        dt = globalClock.getDt()

        # If the camera-left key is pressed, move camera left.
        # If the camera-right key is pressed, move camera right.

        #if self.keyMap["cam-left"]:
            #self.camera.setZ(self.camera, -20 * dt)
        #if self.keyMap["cam-right"]:
            #self.camera.setZ(self.camera, +20 * dt)

        # save ralph's initial position so that we can restore it,
        # in case he falls off the map or runs into something.

        startpos = self.ralph.getPos()

        # If a move-key is pressed, move ralph in the specified direction.

        if (self.keyMap["forward"]!=0):
            self.ralph.setY(self.ralph, -25 * globalClock.getDt())
        if (self.keyMap["back"]!=0):
            self.ralph.setY(self.ralph, 25 * globalClock.getDt())
        if (self.keyMap["left"]!=0):
            self.ralph.setX(self.ralph, 25 * globalClock.getDt())
        if (self.keyMap["right"]!=0):
            self.ralph.setX(self.ralph, -25 * globalClock.getDt())
        if self.keyMap["c"]:
            if self.jumping is False:
            #self.ralph.setH(self.ralph.getH() + 300 * dt)
            #self.ralph.setZ(self.ralph.getZ() + 100 * dt)
                self.jumping = True
                self.vz = 7

        if self.keyMap["space"]:
            self.lightpivot3.setPos(self.ralph.getPos())
            self.lightpivot3.setZ(self.ralph.getZ() + .5)
            self.lightpivot3.setX(self.ralph.getX() - .25)
            #self.myShot.setHpr(self.ralph.getHpr())
            #parent
            node = NodePath("tmp")
            node.setHpr(self.ralph.getHpr())
            vec = render.getRelativeVector(node,(0,-1,0))
            self.myShotVec = vec

        self.lightpivot3.setPos(self.lightpivot3.getPos() + self.myShotVec * dt * 15 )

        
        # If a zoom button is pressed, zoom in or out
        if (self.keyMap["wheel-in"]!=0):
            self.cameraDistance -= 0.1 * self.cameraDistance;
            if (self.cameraDistance < 5):
                self.cameraDistance = 5
            self.keyMap["wheel-in"] = 0
        elif (self.keyMap["wheel-out"]!=0):
            self.cameraDistance += 0.1 * self.cameraDistance;
            if (self.cameraDistance > 250):
                self.cameraDistance = 250
            self.keyMap["wheel-out"] = 0
        #if (self.keyMap["zoom-in"]!=0):
            #self.cameraDistance -= globalClock.getDt() * self.cameraDistance;
            #if (self.cameraDistance < 5):
                #self.cameraDistance = 5
        #elif (self.keyMap["zoom-out"]!=0):
            #self.cameraDistance += globalClock.getDt() * self.cameraDistance;
            #if (self.cameraDistance > 250):
                #self.cameraDistance = 250
        # point the camera at the view target

        
        if base.mouseWatcherNode.hasMouse():
            # get changes in mouse position
            md = base.win.getPointer(0)
            x = md.getX()
            y = md.getY()
            deltaX = md.getX() - 200
            deltaY = md.getY() - 200
            # reset mouse cursor position
            base.win.movePointer(0, 200, 200)
            # alter ralph's yaw by an amount proportionate to deltaX
            self.ralph.setH(self.ralph.getH() - 0.3* deltaX)
            # find the new camera pitch and clamp it to a reasonable range
            self.cameraPitch = self.cameraPitch + 0.1 * deltaY
            if (self.cameraPitch < -60): self.cameraPitch = -60
            if (self.cameraPitch >  80): self.cameraPitch =  80
            base.camera.setHpr(0,self.cameraPitch,0)
            # set the camera at around ralph's middle
            # We should pivot around here instead of the view target which is noticebly higher
            base.camera.setPos(0,0,self.cameraTargetHeight/2)
            # back the camera out to its proper distance
            base.camera.setY(base.camera,self.cameraDistance)
            
        viewTarget = Point3(0,0,self.cameraTargetHeight)
        base.camera.lookAt(viewTarget)
        # reposition the end of the  camera's obstruction ray trace
        self.cameraRay.setPointB(base.camera.getPos())
        # Use mouse input to turn both Ralph and the Camera
            

        if self.jumping is True:
            self.vz = self.vz - 16* dt
            self.ralph.setZ(self.ralph.getZ() + self.vz * dt )
            entries = list(self.ralphGroundHandler.getEntries())
            entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())
            if len(entries) > 0 :
                if self.ralph.getZ() < 0:#entries[0].getSurfacePoint(render).getZ():
                    #self.ralph.setZ(entries[0].getSurfacePoint(render).getZ())
                    self.ralph.setZ(0)
                    self.jumping = False
        # If ralph is moving, loop the run animation.
        # If he is standing still, stop the animation.

        #if self.keyMap["forward"] or self.keyMap["left"] or self.keyMap["right"] or self.keyMap["c"] or self.keyMap["forward"] or self.keyMap["back"]:
            #if self.isMoving is False:
                #self.ralph.loop("run")
                #self.isMoving = True


       # else:
            #if self.isMoving:
               # self.ralph.stop()
                #self.ralph.pose("walk", 5)
                #self.isMoving = False

        #node = NodePath("tmp")
        #node.setHpr(self.ralph.getHpr())
        #vec = render.getRelativeVector(node,(1,0,0))

        #self.ralph.setPos(self.ralph.getPos() + vec * dt * 20)

        node = NodePath("tmp")
        #self.pawn.getH()
        node.setHpr(self.pawn.getHpr())
        vec = render.getRelativeVector(node,(random.random() * -0.8,random.random() + 1,0))
        self.shot.setPos(self.shot.getPos() + self.vec * dt * 10 )
        if self.shot.getY() < -15 or self.shot.getY() > 15 or self.shot.getX() < -15 or self.shot.getX() > 15:
            self.shot.setPos(self.pawn.getPos() + (0,0,0))
            self.vec = render.getRelativeVector(node,(random.random() * -0.8,random.random() + 1,0))
            self.vec = render.getRelativeVector(node,(random.random() * -0.8,random.random() + 1,0))

        # If the camera is too far from ralph, move it closer.
        # If the camera is too close to ralph, move it farther.

        camvec = self.ralph.getPos() - self.camera.getPos()
        #camvec.setZ(self.camera.getZ())
        camdist = camvec.length()
        x = self.camera.getZ()
        camvec.normalize()
        if camdist > 6.0:
            self.camera.setPos(self.camera.getPos() + camvec * (camdist - 6))
            camdist = 10.0
            #self.camera.setZ(self.camera, x)
        if camdist < 6.0:
            self.camera.setPos(self.camera.getPos() - camvec * (6 - camdist))
            camdist = 5.0
            #self.camera.setZ(self.camera, x)

        # Normally, we would have to call traverse() to check for collisions.
        # However, the class ShowBase that we inherit from has a task to do
        # this for us, if we assign a CollisionTraverser to self.cTrav.
        #self.cTrav.traverse(render)

        # Adjust ralph's Z coordinate.  If ralph's ray hit terrain,
        # update his Z. If it hit anything else, or didn't hit anything, put
        # him back where he was last frame.

        entries = list(self.ralphGroundHandler.getEntries())
        entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())
        if self.jumping == False:
            if len(entries) > 0:# and entries[0].getIntoNode().getName() == "terrain":
                #self.ralph.setZ(entries[0].getSurfacePoint(render).getZ())
                pass
            else:
                self.ralph.setPos(startpos)

        # Keep the camera at one foot above the terrain,
        # or two feet above ralph, whichever is greater.

        entries = list(self.camGroundHandler.getEntries())
        entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())

        #if len(entries) > 0 and entries[0].getIntoNode().getName() == "ground":
            #self.camera.setZ(entries[0].getSurfacePoint(render).getZ() + 1.5)
        if self.camera.getZ() < self.ralph.getZ() + 1 or self.camera.getZ() > self.ralph.getZ() + 1:
            self.camera.setZ(self.ralph.getZ() + 1)

        #self.camera.setZ(self.ralph.getZ() + 1.5)
        #self.camera.setP(self.camera, 130)

        # The camera should look in ralph's direction,
        # but it should also try to stay horizontal, so look at
        # a floater which hovers above ralph's head.
        self.camera.lookAt(self.floater)

        return task.cont


demo = RoamingRalphDemo()
demo.run()

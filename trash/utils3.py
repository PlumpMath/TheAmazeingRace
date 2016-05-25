import sys
from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerPusher, CollisionSphere, CollisionTube
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import PandaNode, NodePath, Camera, TextNode
from panda3d.core import CollideMask, LPoint3, PointLight, LVector3, CardMaker, LVector3f, Vec3
from direct.gui.OnscreenText import OnscreenText
import math

def moveChris(self,dt):
    if self.chrisAlive == True:
        if self.chris.getX() > 35:
            self.chrisMoveDir = -1
        elif self.chris.getX() < 20:
            self.chrisMoveDir = 1

        chrisV = Vec3(self.chris.getX(),self.chris.getY(),self.chris.getZ())
        shotV = Vec3(self.chrisShot.getX(),self.chrisShot.getY(),self.chrisShot.getZ())
        self.chris.lookAt(self.ralph)
        self.chris.setH( self.chris.getH() - 90)
        self.chris.setR(self.chris.getR() -90)

        if globalClock.getFrameTime()- self.chrisRedTime > .1 and self.chrisHit == True:
            self.chris.clearColor()
            self.chrisHit = False

        if abs(chrisV.length() - shotV.length()) > 15:
            ralphV = Vec3(self.ralph.getX(),self.ralph.getY(),self.ralph.getZ() + .5 )
            #self.chris.setH(0)
            #self.chris.setR(0)
            #self.chris.setZ(0)
            self.chrisShot.setPos(self.chris.getPos())
            self.chrisShot.setX(self.chrisShot.getX() - 1)
            shotV = Vec3(self.chrisShot.getX(),self.chrisShot.getY(),self.chrisShot.getZ())
            chrisV = Vec3(self.chris.getX(),self.chris.getY(),self.chris.getZ())
            difVec = ralphV - shotV
            self.chrisShotVec = difVec
            x = difVec.getX()
            y = difVec.getY()
            z = difVec.getZ()
            magnitude = math.sqrt(x*x + y*y + z*z)
            difVec = Vec3(x/magnitude,y/magnitude,z/magnitude)
            #if x < 0:
            #    difVec.setX(difVec.getX() * -1)
            #if y < 0:
            #    difVec.setY(difVec.getY() * -1)
            #if z < 0:
            #    difVec.setZ(difVec.getZ() * -1)
            self.chrisShotVec = difVec


        #self.chrisShot.lookAt(self.ralph)
        self.chris.setX(self.chris.getX() + self.chrisMoveDir * 5 * dt)
        self.chrisShot.setPos(self.chrisShot.getPos() + self.chrisShotVec * dt * 20)
        #self.chrisShot.setY(self.chrisShot.getY() - .3)
def setUpKeys(self):
    # This is used to store which keys are currently pressed.
    self.keyMap = {"left": 0, "right": 0, "forward": 0, "cam-left": 0, "cam-right": 0, "c":0, "back":0, "space":0}
    # Accept the control keys for movement and rotation
    self.accept("escape", sys.exit)
    self.accept("arrow_left", self.setKey, ["left", True])
    self.accept("arrow_right", self.setKey, ["right", True])
    self.accept("arrow_up", self.setKey, ["forward", True])
    self.accept("arrow_down", self.setKey, ["back", True])
    self.accept("a", self.setKey, ["cam-left", True])
    self.accept("s", self.setKey, ["cam-right", True])
    self.accept("arrow_left-up", self.setKey, ["left", False])
    self.accept("arrow_right-up", self.setKey, ["right", False])
    self.accept("arrow_up-up", self.setKey, ["forward", False])
    self.accept("arrow_down-up", self.setKey, ["back", False])
    self.accept("a-up", self.setKey, ["cam-left", False])
    self.accept("s-up", self.setKey, ["cam-right", False])
    self.accept("space", self.setKey, ["space", True])
    self.accept("space-up", self.setKey, ["space", False])
    self.accept("c",self.setKey,["c",True])
    self.accept("c-up",self.setKey,["c",False])


def setUpLighting(self):
    self.win.setClearColor((0.2, 0.2, 0.2, 1.0))
    # Create a bit of ambient light and some directional light
    # to be able to tell objects are 3d
    ambientLight = AmbientLight("ambientLight")
    ambientLight.setColor((.3, .3, .3, .4))
    render.setLight(render.attachNewNode(ambientLight))
    #ambientLight2 = AmbientLight("ambientLight2")
    #ambientLight2.setColor((1, 1, 1, 10))
    #self.room.setLight(self.room.attachNewNode(ambientLight2))
    directionalLight = DirectionalLight("directionalLight")
    directionalLight.setDirection((0, 0, -2))
    directionalLight.setColor((1, 1, 1, .5))
    directionalLight.setSpecularColor((1, 1, 1, 1))
    render.setLight(render.attachNewNode(directionalLight))

def setUpFloatingSpheres(self):
    #set up for yellow sphere
    self.lightpivot = render.attachNewNode("lightpivot")
    self.lightpivot.setPos(8, 4, 2)
    self.lightpivot.hprInterval(9, LPoint3(360, 0, 0)).loop()#6
    plight = PointLight('plight')
    plight.setColor((.7, .3, 0, 1))#yellow
    plight.setAttenuation(LVector3(0.7, 0.05, 0))
    self.plnp = self.lightpivot.attachNewNode(plight)
    self.plnp.setPos(4, 0, 0)
    self.room.setLight(self.plnp)
    sphere = loader.loadModel("models/icosphere")
    sphere.reparentTo(self.plnp)
    sphere.setScale(0.1)
    sphere.setColor((1,1,0,1))

    self.lightpivot2 = render.attachNewNode("lightpivot2")
    self.lightpivot2.setPos(14, 42, 1.6)
    self.lightpivot2.hprInterval(5, LPoint3(360, 0, 0)).loop()
    plight2 = PointLight('plight2')
    plight2.setColor((0, .4,.8, 1))
    plight2.setAttenuation(LVector3(0.7, 0.05, 0))
    self.plnp2 = self.lightpivot2.attachNewNode(plight2)
    self.plnp2.setPos(5, 0, 0)
    self.room2.setLight(self.plnp2)#render?
    sphere2 = loader.loadModel("models/icosphere")
    sphere2.reparentTo(self.plnp2)
    sphere2.setScale(0.2)
    sphere2.setColor((0,0,1,1))

def setUpRalphsShot(self):
    #self.myShotVec = LVector3(0,0,0)#0,0,0 vector since its not moving at first
    #setup for the sphere ralph shoots out
    #self.lightpivot3 = render.attachNewNode("lightpivot3")
    #self.lightpivot3.setPos(0, 0, 2)
    #self.lightpivot3.hprInterval(10, LPoint3(0, 0, 0)).loop()
    #plight3 = PointLight('plight2')
    #plight3.setColor((0, .3,0, 1))
    #plight3.setAttenuation(LVector3(0.7, 0.05, 0))
    #plnp3 = self.lightpivot3.attachNewNode(plight3)
    #plnp3.setPos(0, 0, 0)
    #self.room2.setLight(plnp3)
    #self.room.setLight(plnp3)
    self.sphere3 = loader.loadModel("models/icosphere")
    #self.sphere3.reparentTo(plnp3)
    self.sphere3.setScale(0.1)
    self.sphere3.setColor((0,1,0,1))
    self.shotList = []
    for i in range(0,5):
        lightpivot = render.attachNewNode("lightpivot")
        lightpivot.setPos(-50 - i*3,0,-2)
        #lightpivot.setZ(self.ralph.getZ() + .5)
        #lightpivot.setX(self.ralph.getX() - .25)
        lightpivot.hprInterval(10, LPoint3(0, 0, 0)).loop()
        plight = PointLight('plight')
        plight.setColor((0, .3, 0, 1))#yellow
        plight.setAttenuation(LVector3(0.7, 0.05, 0))
        plnp = lightpivot.attachNewNode(plight)
        plnp.setPos(0, 0, 0)
        self.room.setLight(plnp)
        self.room2.setLight(plnp)
        n = plnp.attachNewNode("Obstacle")
        self.sphere3.instanceTo(n)

        vec = LVector3(0,0,0)

        rShot = ralphShot(lightpivot,vec)
        self.shotList.append(rShot)

        cs = CollisionSphere(0,0,0,.2)
        cspath = lightpivot.attachNewNode((CollisionNode('ralphOrbColPath')))
        cspath.node().addSolid(cs)
        cspath.show()

        self.cTrav.addCollider(cspath, self.orbCollisionHandler)

    self.shotCount = 1

def setUpCamera(self):
    # Create a floater object, which floats 2 units above ralph.  We
    # use this as a target for the camera to look at.
    self.floater = NodePath(PandaNode("floater"))
    self.floater.reparentTo(self.ralph)
    self.floater.setZ(9.0)
    # Set up the camera
    self.disableMouse()
    self.camLens.setFov(60)

    self.camera.setPos(self.ralph.getX() -10, self.ralph.getY() + 10, self.ralph.getZ() - 10)
    self.camera.lookAt(self.ralph)
    #self.camera.lookAt(self.floater)
    self.camera.reparentTo(self.floater)


def loadModels(self):
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
    # one optimized for rendering, one for collisions

    self.room = loader.loadModel("models/solidfloormazefinal")
    self.room.reparentTo(render)
    self.room.setScale(.25)
    self.room.setPos(0,0,0)
    #self.room.setShaderAuto()
    #self.room.writeBamFile("myRoom1.bam")
    #self.room.setColor(.3,.3,.3,1)
    self.room.setTexture(loader.loadTexture("models/fieldstone-c.jpg"))

    self.room2 = loader.loadModel("models/room1finalfinal")
    self.room2.reparentTo(render)
    self.room2.setScale(.25)
    self.room2.setPos(100,50,.025)
    self.room2.setH(90)
    self.room2.setTexture(loader.loadTexture("models/layingrock-c2.jpg"))

    self.ralph = Actor("models/ralph",{"run": "models/ralph-run","walk": "models/ralph-walk"})
    self.ralph.reparentTo(render)
    self.ralph.setScale(.2)
    self.ralph.setPos(13,24,0)

    self.gianteye = loader.loadModel("models/gianteye")
    self.gianteye.reparentTo(render)
    self.gianteye.setScale(.075)
    self.gianteye.setPos(0,0,0)
    self.gianteye.setColor(1,0,0,1)
    self.gianteye.setH(180)

    self.chik = loader.loadModel("models/chik")
    self.chik.reparentTo(render)
    self.chik.setScale(.05)
    self.chik.setPos(14,3,1)
    self.chik.setH(-95)
    self.chik.setColor(.9,.9,.1,1)

    self.pawn = loader.loadModel("models/blueidolfinal")
    self.pawn.setScale(.2)
    #self.pawn.setR(105)
    self.pawn.reparentTo(render)
    self.pawn.setPos(10,10,0)

    self.catidol = loader.loadModel("models/catidol")
    self.catidol.reparentTo(render)
    self.catidol.setScale(.5)
    self.catidol.setPos(25,40,0)
    #self.catidol.setH(-95)
    #self.catidol.setColor(.9,.9,.1,1)

    #Set up for chris
    self.chris = loader.loadModel("models/chris")
    self.chris.reparentTo(render)
    self.chris.setScale(.35)
    self.chris.setPos(50,45,0)
    self.chrisMoveDir = 1
    self.chrisShotVec = LVector3f(0,1,0)
    self.chrisHealth = 12
    self.chrisHit = False
    self.chrisRedTime = 0
    self.chrisAlive = True
    #self.chris.setH(90)
    #self.chris.setR(-90)
    #self.chris.setZ(2)

    #Set up for Chris's shot
    sphere = loader.loadModel("models/icosphere")
    sphere.setScale(0.2)
    sphere.setColor((1,0,1,1))
    self.chrisShot = render.attachNewNode("lightpivot")
    self.chrisShot.setPos(15,45,3)
    self.chrisShot.hprInterval(10, LPoint3(0, 0, 0)).loop()
    plight = PointLight('plight')
    plight.setColor((.4, 0, .4, 1))#purple
    plight.setAttenuation(LVector3(0.7, 0.05, 0))
    plnp = self.chrisShot.attachNewNode(plight)
    plnp.setPos(0, 0, 0)
    sphere.reparentTo(plnp)
    self.room.setLight(plnp)
    self.room2.setLight(plnp)
    #n = plnp.attachNewNode("Obstacle")
    #self.sphere3.instanceTo(n)

    #vec = LVector3(0,0,0)

    #rShot = ralphShot(lightpivot,vec)
    #self.shotList.append(rShot)



    self.blueidol = loader.loadModel("models/blueidolfinal")
    #self.blueidol.reparentTo(render)
    self.blueidol.setScale(.5)
    self.blueidol.setPos(19,40,0)

    self.shot = loader.loadModel("models/icosphere.egg")
    self.shot.reparentTo(render)
    self.shot.setScale(.5)
    self.shot.setPos(0,0,1)
    self.shot.setColor(1,.3,.3,1)


class ralphShot:
    def __init__(self, lp, v):
        self.lpivot = lp
        self.vec = v



# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.1,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

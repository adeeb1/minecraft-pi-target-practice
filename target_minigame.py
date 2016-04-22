from mcpi.minecraft import Minecraft
from mcpi import block
from mcpi.vec3 import Vec3
from random import randint
from utils import getCurrentTime, floatToInt
import math
from sensors import Button, LEDLight

# For most of this game, the Z coordinate is used in place of the X because
# it allows the player to play the game without manually turning very much

mc = Minecraft.create()

def sendMessage(message):
    mc.postToChat(message)

def allowDestruction(isAllowed):
    mc.setting("world_immutable", not isAllowed)

def removeBlock(x, y, z):
    mc.setBlock(x, y, z, block.AIR.id)

class Target:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.dir = Vec3(1, 0, 0)
        self.speed = 1
        self.blockType = block.WOOD.id

        # Used for setting a delay in target move speed
        self.moveTime = getCurrentTime()
        self.timeUntilMove = 1000

    def canMove(self):
        timeSinceMove = gameInfo.gameTime - self.moveTime

        return (timeSinceMove >= self.timeUntilMove)
    
    def move(self):
        removeBlock(self.x, self.y, self.z)

        self.z += self.dir.x * self.speed
        self.y += self.dir.y * self.speed

        # Keep the block within the game board bounds
        self.checkSwitchDir()

        mc.setBlock(self.x, self.y, self.z, self.blockType)

    def checkSwitchDir(self):
        if (self.y >= gameInfo.gameBoard.y):
            self.y = gameInfo.gameBoard.y
            self.dir.y *= -1
        elif (self.y <= gameInfo.gameBoard.bottom):
            self.y = gameInfo.gameBoard.bottom
            self.dir.y *= -1

        if (self.z >= gameInfo.gameBoard.right):
            self.z = gameInfo.gameBoard.right
            self.dir.x *= -1
        elif (self.z <= gameInfo.gameBoard.z):
            self.z = gameInfo.gameBoard.z
            self.dir.x *= -1

    def wasHit(self, blockPos):
        pos = Vec3(self.x, self.y, self.z)
        
        return (pos == blockPos)

    def remove(self):
        removeBlock(self.x, self.y, self.z)

class AttackBlock:
    def __init__(self, x, y , z):
        self.pos = Vec3(x, y, z)
        self.dir = Vec3(1, 0, 0)
        self.blockType = block.GOLD_ORE.id
        
        self.moveTime = getCurrentTime()
        self.timeUntilMove = 1000

    def canMove(self):
        timeSinceMove = gameInfo.gameTime - self.moveTime

        return (timeSinceMove >= self.timeUntilMove)
    
    def move(self):
        self.remove()

        self.pos.x += self.dir.x

        mc.setBlock(self.pos.x, self.pos.y, self.pos.z, self.blockType)
    
    def remove(self):
        removeBlock(self.pos.x, self.pos.y, self.pos.z)

class PlayerInfo:
    def __init__(self):
        self.player = mc.player
        self.score = 0

        self.attackTime = getCurrentTime()
        self.timeUntilAttack = 1000
        
        self.attackBlocks = []

    def getPos(self):
        x, y, z = self.player.getPos()

        x = floatToInt(x)
        y = floatToInt(y)
        z = floatToInt(z)
        
        return Vec3(x, y, z)

    def setPos(self, x, y, z):
        self.player.setPos(x, y, z)

    def canAttack(self):
        timeSinceAttack = gameInfo.gameTime - self.attackTime
        
        # Prevent attacks if the user is away from the game board
        facingGameBoard = gameInfo.gameBoard.isInside(self.getPos())
        
        return (timeSinceAttack >= self.timeUntilAttack \
                and facingGameBoard == True)

    def attack(self):
        x, y, z = self.getPos()

        x = floatToInt(x)
        y = floatToInt(y)
        z = floatToInt(z)
        
        attackBlock = AttackBlock(x, y, z)
        self.attackBlocks.append(attackBlock)

        # Reset attack timer
        self.attackTime = getCurrentTime()

class GameInfo:
    def __init__(self, winScore=None):
        if winScore is None:
            winScore = 10
            
        self.gameStarted = False
        self.gameTime = getCurrentTime()
        
        self.maxTargets = 1
        self.targets = []

        self.winScore = winScore

        self.gameBoard = Rect(0, 0, 0, 0, 0)

    def hitTarget(self, target):
        target.remove()
        self.targets.remove(target)

        player.score += 1

        sendMessage("Score: %i" % (player.score))

        # Blink the LED
        ledLight.startBlinking()

        createTarget()

    def checkPlayerWin(self):        
        if (player.score >= self.winScore):
            # Stop the game
            self.gameStarted = False

            # Send the win message
            sendMessage("You win!!")

            # Allow destruction in the game world
            allowDestruction(True)

class Rect:
    def __init__(self, x, y, z, width, height):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = 1 

    @property
    def bottom(self):
        return (self.y - self.height)

    @property
    def right(self):
        return (self.z + self.width)

    def isInside(self, pos):
        insideZ = (pos.z >= self.z and pos.z <= self.right)
        insideY = (pos.y <= self.y and pos.y >= self.bottom)
        
        return (insideZ and insideY)

    def isInsideWithX(self, pos):
        insideX = (pos.x == self.x)
        insideZ = (pos.z >= self.z and pos.z <= self.right)
        insideY = (pos.y <= self.y and pos.y >= self.bottom)
        
        return (insideX and insideZ and insideY)

gameInfo = GameInfo()
player = PlayerInfo()
ledLight = LEDLight(17, 4)
button = Button(22)

def createGameWalls():
    global gameInfo
    x, y, z = player.getPos()

    radius = 12
    wallHeight = 6

    startX = floatToInt(x) + radius
    startY = floatToInt(y)
    startZ = floatToInt(z)

    gameInfo.gameBoard.x = startX
    gameInfo.gameBoard.y = startY + wallHeight
    gameInfo.gameBoard.z = startZ - radius
    gameInfo.gameBoard.width = radius * 2
    gameInfo.gameBoard.height = wallHeight

    # range() is exclusive on the upper limit

    for i in range(0, wallHeight + 1):
        for j in range(-radius, radius + 1):
            mc.setBlock(startX, startY + i, startZ + j, block.STONE.id)

def createGameStartSwitch():
    x, y, z = player.getPos()

    switchDistance = 6
    hDistance = 2

    mc.setBlock(x + switchDistance, y, z + hDistance, block.TNT.id, 1)

def checkGameBlocksHit():
    for blockEvent in mc.events.pollBlockHits():
        x, y, z = blockEvent.pos
        blockType = mc.getBlock(x, y, z)

def initGameMode():
    global gameInfo
    gameInfo = GameInfo(3)

    # Turn off the LED if it's on
    ledLight.setLightStatus(False)
    
    allowDestruction(True)

    createGameStartSwitch()

    # Tell the user how to start playing
    sendMessage("Look for the TNT near you. Hit it to start target practice!")

    while gameInfo.gameStarted == False:
        for blockEvent in mc.events.pollBlockHits():
            x, y, z = blockEvent.pos
            blockType = mc.getBlock(x, y, z)

            if (blockType == block.TNT.id):
                removeBlock(x, y, z)              
                startGame()

def createTarget():
    global gameInfo
    
    # Get a random start position on the game board
    randX = randint(gameInfo.gameBoard.z, gameInfo.gameBoard.right)
    randY = randint(gameInfo.gameBoard.bottom, gameInfo.gameBoard.y)

    target = Target(gameInfo.gameBoard.x - 1, randY, randX)

    # Get a random direction for the target
    dirX = 0
    dirY = 0

    # Make sure the block will be moving
    while (dirX == 0 and dirY == 0):
        dirX = randint(-1, 1)
        dirY = randint(-1, 1)

    target.dir = Vec3(dirX, dirY, 0)

    mc.setBlock(target.x, target.y, target.z, target.blockType)

    gameInfo.targets.append(target)

def gameLoop():
    while gameInfo.gameStarted == True:
        gameInfo.gameTime = getCurrentTime()

        checkGameBlocksHit()

        if (len(gameInfo.targets) < gameInfo.maxTargets):
            createTarget()

        for target in gameInfo.targets:
            if (target.canMove() == True):
                target.move()
                target.moveTime = getCurrentTime()

        if (button.pressed() == True and player.canAttack() == True):
            player.attack()

        # Uncomment below two lines for auto-attack
        #if (player.canAttack() == True):
            #player.attack()

        for attackBlock in player.attackBlocks:
            attackBlock.move()

            if (gameInfo.gameBoard.isInsideWithX(attackBlock.pos) == True):
                player.attackBlocks.remove(attackBlock)
                attackBlock.remove()
                
                mc.setBlock(attackBlock.pos.x, attackBlock.pos.y, attackBlock.pos.z, block.STONE.id)

            for target in gameInfo.targets:
                if target.wasHit(attackBlock.pos) == True:
                    gameInfo.hitTarget(target)

                    gameInfo.checkPlayerWin()

                    break

        if (ledLight.canBlink(gameInfo.gameTime) == True):
            ledLight.blink()

def startGame():
    gameInfo.gameStarted = True

    # Prevent the user from destroying the game wall
    allowDestruction(False)

    # Move the player up to an "arena"
    #x, y, z = player.getPos() 
    #player.setPos(x, y, z)

    createGameWalls()
    sendMessage("Target practice has begun!")

    gameLoop()


# Start the game mode
if __name__ == "__main__":
    initGameMode()

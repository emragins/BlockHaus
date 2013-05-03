import sys
sys.path = ['','source', 'python']

from engine import *


manager.UpdateList.append(UpdateObjects)
manager.RenderList.append(RenderObjects)
#manager.UpdateList.append(effect.Update)
#manager.RenderList.append(effect.Render)

import game
game.StartScreen()
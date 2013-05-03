RenderList = [ ]
UpdateList = [ ]

def ExecuteRenderList():
    for x in RenderList:
        x()

def ExecuteUpdateList():

    for x in UpdateList:
        x()
class ImageHistory:
    
    def __init__(self, maxSteps):
        self.maxNumberOfSteps = maxSteps
        self.historyIndex = 0
        self.images = []

    # Kép hozzáadása a listához
    def AddImageToHistory(self, image):
        if len(self.images) - 1 > self.historyIndex + 1:
            for i in range(self.historyIndex + 1, len(self.images) - 1):
                self.images.pop(i)        

        self.images.append(image)
        self.historyIndex += 1
        if len(self.images) > self.maxNumberOfSteps:
            self.images.pop(0)

    # Visszavonás
    def Undo(self):
        if self.historyIndex > 0:
            self.historyIndex -= 1
        
        return self.images[self.historyIndex]

    # Újra
    def Redo(self):
        self.historyIndex += 1
        if self.historyIndex == self.maxNumberOfSteps:
            self.historyIndex -= 1

        return self.images[self.historyIndex]

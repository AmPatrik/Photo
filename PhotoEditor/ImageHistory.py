class ImageHistory:
    
    def __init__(self, maxSteps):
        self.maxNumberOfSteps = maxSteps
        self.historyIndex = -1
        self.images = []


    # Kép hozzáadása a listához
    def AddImageToHistory(self, image):
        # az aktuális kép után kiveszünk mindent a listából
        if len(self.images) - 1 > self.historyIndex:
            for i in range(self.historyIndex + 1, len(self.images)):
                self.images.pop(self.historyIndex + 1)        

        # kép hozzáfűzése a listához
        self.images.append(image)
        self.historyIndex += 1

        # ha a lista elérte a maximális hosszt
        if len(self.images) > self.maxNumberOfSteps:
            self.images.pop(0)
            self.historyIndex -= 1


    # Visszavonás
    def Undo(self):
        if self.historyIndex > 0:   # ha elérte a 0 indexet
            self.historyIndex -= 1

        print("historyIndex: ")
        print(self.historyIndex)
        return self.images[self.historyIndex]


    # Újra
    def Redo(self):
        self.historyIndex += 1
        if self.historyIndex == len(self.images):   # ha elérte a lista hosszát
            self.historyIndex -= 1
        
        print("historyIndex: ")
        print(self.historyIndex)   
        return self.images[self.historyIndex]

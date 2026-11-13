class Piece():
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.king = False
        self.direction = 1 if self.color == 'blue' else -1
    
    def make_king(self):
        self.king = True
        self.direction = self.direction * (-1)

    def get_color(self):
        return self.color
    
    def get_direction(self):
        return self.direction
    
    def get_piece_color(self, x, y):
        return self.color
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    


    

    

    
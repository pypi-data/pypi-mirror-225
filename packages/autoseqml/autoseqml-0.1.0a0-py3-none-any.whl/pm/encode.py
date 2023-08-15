class Encode:
    def __init__(self, coding):
        self.coding = coding
        with open('wordlist.txt', 'r') as f:
            self.wl = [w.strip() for w in f.readlines()]
            
    def encode(self):
        return ' '.join([self.wl[_] for _ in self.coding])
    
if __name__=='__main__':
    coding = [1,7,2,0,0,3,7,1,45,24,6,2]
    
    print(coding, Encode(coding).encode())
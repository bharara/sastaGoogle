class HashMap():
    def __init__(self):
        self.size= 6
        self.map=[None] *self.size # Map is the name of the array and none sets all to none 

    def gethash(self,key):
        hash=0
        for char in str(key):
            hash+=ord(char)
        return hash % self.size

    def add(self,key,value):
        key_hash=self.gethash(key) #index value
        key_value=[key, value] #construct a list

        if self.map[key_hash] is None:
            self.map[key_hash]=list([key_value]) #if empty add none
            return True
        else :
            for pair in self.map[key_hash]: #if non empty check existing or not
                if pair[0]==key:
                    pair[1]=value #if match return true
                    return True
            self.map[key_hash].append(key_value) #if non match append value 
            return True


    def get(self,key):
        key_hash=self.gethash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0]==key:
                    return pair[1]
        return none

    def delete(self,key):
        key_hash=self.gethash(key)

        if self.map[key_hash] is None: #check cell none
            return False
        for i in range (0,len(self.map[key_hash])): #check index
            if self.map[key_hash][i][0]==key:
                self.map[key_hash].pop(i) #when located remove
                return True
        

    

    def print(self):
        for item in self.map:
            if item is not None:
                print(str(item));


h=HashMap()
h.add('Abdul Hadi','645365')
h.add('Asaeed','03853059')
h.add('Asaeed','03853059')
h.add('Asaeed','03853059')
h.add('Asaeed','03853059')
h.add('Asaeed','03853059') 
h.print()
        
        

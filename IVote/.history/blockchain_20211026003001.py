#importing all the required for code
import hashlib
import threading
import time

#class block for creating a block
class Block:
    # block init block 
    def __init__(self, id, my_hash, prev_hash, height,time_in) :
        #set every things of the block like id and other mores
        self.id = id
        self.my_hash = my_hash
        self.prev_hash = prev_hash
        self.height = height    #for tree sturcture
        self.time_in = time_in
    
    #printing blocks in file
    def send_to_file(self):
        st1='\n id='+str(self.id)+'\n myhash='+str(self.my_hash)+'\n prevhash='+str(self.prev_hash)+'\n time='+str(self.time_in)
        return st1

    def addBlock(self,secret_code,name_of_blockchain,voter_id,vote_given,block):
        

        my_hash = hashlib.sha256(str( str(secret_code)+str(voter_id)+"vote:"+str(vote_given)).encode('utf-8')).hexdigest()
        self.tree.append(block)
        self.tree[block.id].my_hash = my_hash
        
        #print(block.send_to_file())
        #add the block in the main block chain
        f=open("blockchain/"+name_of_blockchain+".txt",'a')
        f.write("\n"+self.send_to_file())
        f.close

        return my_hash



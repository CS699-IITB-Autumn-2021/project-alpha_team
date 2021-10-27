#importing all the required for code
import hashlib
from datetime import datetime
import time

#class block for creating a block
class Block:
    # block init block 
    def __init__(self, id, my_hash, prev_hash,time_in) :
        """set every things of the block like id and other mores
        """
        #set every things of the block like id and other mores
        #id for identifin the block it is a (Voter ID)
        self.id = id
        #my block hash value 
        self.my_hash = my_hash
        #previous block hash value 
        self.prev_hash = prev_hash
        #time at which this block was created 
        self.time_in = time_in
    
    #printing blocks in file
    def send_to_file(self):
        """format in which file was stored 
        """
        #format in which file was stored 
        st1='\n id='+str(self.id)+'\n myhash='+str(self.my_hash)+'\n prevhash='+str(self.prev_hash)+'\n time='+str(self.time_in)
        #return the string 
        return st1

    #function for adding block to the block chain
    def addBlock(self,secret_code,name_of_blockchain,voter_id,vote_given):
        """function for adding block to the block chain
        """
        fle = Path("static/blockchain/"+name_of_blockchain+".txt")
        fle.touch(exist_ok=True)
        f = open(fle)
        #voters ID
        self.id=voter_id
        #calculating the second 
        seconds = time.time()
        #give me the current time
        self.time_in= time.ctime(seconds)
        #openning the required files for blockchains
        f = open("static/blockchain/"+name_of_blockchain+".txt", "r")
        #reading the file
        file_data=str(f.read())
        #finding the last (prevblock hash value)
        index=file_data.rfind("myhash=")
        if index==-1:
            self.prev_hash=0
        else:
            self.prev_hash=file_data[index+7:index+71]

        #calculating the hash value using secret_code(randomly generated) , vote: given , prev_hash
        self.my_hash = hashlib.sha256(str( str(secret_code)+str(voter_id)+'vote:'+str(vote_given)+str(self.prev_hash)).encode('utf-8')).hexdigest()

        #print(block.send_to_file())
        #add the block in the main block chain
        f=open("static/blockchain/"+name_of_blockchain+".txt",'a')
        f.write("\n"+self.send_to_file())
        f.close
        #return the hash values and secret_code
        return "my_hash:"+str(self.my_hash)+"prev_hash:"+str(self.prev_hash)



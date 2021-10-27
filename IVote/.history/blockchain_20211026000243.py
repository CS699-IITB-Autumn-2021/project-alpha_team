
import threading
import time


#class block for creating a block
class Block:
    # block init block 
    def __init__(self, id, nonce, transactions, my_hash, prev_hash, height,time_in) :
        #set every things of the block like id and other mores
        self.id = id
        self.nonce = nonce
        self.transactions = transactions
        self.my_hash = my_hash
        self.prev_hash = prev_hash
        self.height = height    #for tree sturcture
        self.time_in = time_in
    
    #printing blocks in file
    def send_to_file(self):
        st1='\n id='+str(self.id)+'\n nonce='+str(self.nonce)+'\n myhash='+str(self.my_hash)+'\n prevhash='+str(self.prev_hash)+'\n transaction='+str(self.transactions)+'\n height='+str(self.height)+'\n time='+str(self.time_in)
        return st1
# class for block chain
class Blockchain:
    #init block for block chain
    def __init__(self) :
        self.id =0
        self.d =0
        self.tree=[]
        #set this else output coming slow
        #threshold is set according to the users 
        self.threshold="0000"

    def add_block(self, transactions,listofnodes,node_number,listofblockchain,matrix):
        nonce = 0
        #if tree size is 0 then generate genesis block
        if len(self.tree) == 0:
            #calculating the hash of block
            prev_hash = "0"    #i.e. genesis block
            self.height = 0
            self.id = 0
            #transaction for adding 50 coins
            transactions = "Genesis"
            my_hash = hashlib.sha256(str(transactions).encode('utf-8')).hexdigest()
            seconds = time.time()
            local_time = time.ctime(seconds)
            block = Block(self.id, nonce, transactions, my_hash, prev_hash, self.height,local_time)
            self.tree.append(block)
            #print(block.send_to_file())
            #add the block in the main block chain
            f=open('output block chain.txt','a')
            f.write("\n"+block.send_to_file())
            f.close
            #add the block in the block chain copy
            f=open('output Node ='+str(node_number)+'.txt','a')
            f.write("\n"+block.send_to_file())
            f.close
        else:
            #calculating the hash of block
            prev_hash = self.tree[-1].my_hash
            self.height = self.tree[-1].height + 1
            self.id += 1
            my_hash = hashlib.sha256(str(transactions).encode('utf-8')).hexdigest()
            seconds = time.time()
            local_time = time.ctime(seconds)
            block = Block(self.id, nonce, transactions, my_hash, prev_hash, self.height,local_time)
            #do PoW
            self.mineBlock(block,listofnodes,node_number,listofblockchain,matrix)
            
       
        return 
        

    def printTree(self):
        dict = {}
        for i in range(len(self.tree)):
            dict[i] = self.tree[i].send_to_file()
        print(dict)   #send to file

    def mineBlock(self, block,listofnodes,node_number,listofblockchain,matrix):
        #nonce value that need to be checked
        nonce = 0
        my_hash = hashlib.sha256(str(str(nonce) + str(block.transactions)).encode('utf-8')).hexdigest()
        while my_hash[0:4] != self.threshold:
            my_hash = hashlib.sha256(str(str(nonce) + str(block.transactions)).encode('utf-8')).hexdigest()
            nonce += 1
        self.tree.append(block)
        self.tree[block.id].my_hash = my_hash
        self.tree[block.id].nonce = nonce
        listofnodes[node_number].coins=listofnodes[node_number].coins+50
        block.transactions.append("TxnID:"+str(node_number)+" mines 50 coins")
         #print(block.send_to_file())
        #add the block in the main block chain
        f=open('output block chain.txt','a')
        f.write("\n"+block.send_to_file())
        f.close
        #add the block in the block chain copy
        f=open('output Node ='+str(node_number)+'.txt','a')
        f.write("\n"+block.send_to_file())
        f.close
        b1=bf.Block_Forwarding()
        b1.Block_broadcasting(matrix,block,node_number,listofnodes,len(block.transactions),listofblockchain)

        #just validate and add the block
    def mineBlock2(self, block,listofnodes,node_number,listofblockchain,matrix):
        nonce = 0
        my_hash = hashlib.sha256(str(str(nonce) + str(block.transactions)).encode('utf-8')).hexdigest()
        while my_hash[0:4] != self.threshold:
            my_hash = hashlib.sha256(str(str(nonce) + str(block.transactions)).encode('utf-8')).hexdigest()
            nonce += 1
        self.tree.append(block)
        self.tree[block.id].my_hash = my_hash
        self.tree[block.id].nonce = nonce  
         #print(block.send_to_file())
        #add the block in the main block chain
        f=open('output block chain.txt','a')
        f.write("\n"+block.send_to_file())
        f.close
        #add the block in the block chain copy
        f=open('output Node ='+str(node_number)+'.txt','a')
        f.write("\n"+block.send_to_file())
        f.close
 
    #started mining 
    def StartMining(self,queueoftransaction,listofnodes,node_number,listofblockchain,matrix):
        while(True):
            # how many blocks to be mined 
            self.d=self.d+1
            if(self.d==100000):
                break
            time.sleep(numpy.random.exponential(5,None))
            mylist = queueoftransaction[:100]
            del queueoftransaction[:100]
            print(mylist)
            if len(mylist)>0 or self.d ==1:
                self.add_block(mylist,listofnodes,node_number,listofblockchain,matrix)
            

#class for runing the block chain simulation
class Run_Block_chain :
    # start methods for block chain simulatuion
    def StartChain(self,listofnodes,queueoftransaction,matrix):
         #list for creating n number of threads 
        list1 = []
         #list for creating n objects of Blockchain()
        list2= []
 
        for i in range(len(listofnodes)):
            list2.append(Blockchain())
        for i in range(len(listofnodes)):
            list1.append(threading.Thread(target=list2[i].StartMining,args=(queueoftransaction,listofnodes,i,list2,matrix,))) 
            list1[i].start()

    
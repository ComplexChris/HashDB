!/usr/bin/env python2.7

import os, sys, ast, time, random

sep = "\n{0}\n".format("_"*60)

def Slow_Type(s, speed=0.0030):
    ## The greater the speed, the slower it will type
    ## Smaller number for faster typing and for larger string output
    #print ( s )
    #return
    modifier = (1000*len(s))/speed
    block_mod = int(len(s)/100)+1
    #print (block_mod)
    #s = s.replace("\n", "\n\n")
    #3for letter in s:
    while len(s)!=0:
        num = random.randrange(0,20) / modifier
        time.sleep(num)
        rindex = random.randrange(1, 5*( block_mod ) )
        block = s[0: rindex ]
        print(block, end=""),
        s = s[ rindex: ]
    
class Main():
    def __init__(self):
        db_path = os.path.join( os.getcwd(), "Databases" )
        if os.path.isdir( db_path ) == False:
            os.mkdir( db_path )
        Slow_Type("\nWelcome to Hash Database creation tool.\n",0.01)
        while True:
            print(sep)
            print("\n\na. Create Database \t b. Verify Directory \nc. Verify File \t\t d. Exit ")
            choice = input(">>> ").upper()
            if len(choice)>1:
                continue
            elif "D" in choice:
                break
            else:
                if "A" in choice:
                    path = input("\nEnter path of folder to be hashed > ")
                    if os.path.isdir( path ):
                        self.CreateTable( path )
                    else:
                        print("Invalid directory")
                elif "B" in choice or "C" in choice:
                    hash_file = input("\nEnter path of hash file > ")
                    if os.path.isfile( hash_file ):
                        if "B" in choice:
                            self.VerifyStructure( hash_file )
                        elif "C" in choice:
                            ind_file = input("\nEnter path of individual file > ")
                            if os.path.isfile( ind_file ):
                                self.VerifyFile( hash_file, ind_file )
                            else:
                                Slow_Type("\nFile not found on local system", 0.1)
                    else:
                        Slow_Type("\nInvalid hash database file", 32)
                    

    def HashFile(self, path, alg="SHA1" ):
        cmd = "certutil /hashfile {0} {1} ".format(path, alg)
        raw = os.popen(cmd).read()
        if "successfully" in raw:
            return raw.split("\n")[1]
        else:
            return ""


    def CreateTable(self, path, mode="SHA1"):
        print(sep)
        ## Product should return 2 dictionary based objects
        ## {"Absolute_Path":{"FileName":"Hash", "File2":"Hash2"}
        path = path.rstrip("\\")
        if os.path.isabs( path )==False:
            ## Creates an absolute path instead of using relative
            path = os.path.abspath( path )
            
        master = {}; total = 0
        start = time.time()
        for (parent, curr, fs) in os.walk(path):
            if len(fs)==0:
                continue
            Slow_Type("\n\nProccessing: "+parent)
            Slow_Type("\nFiles: {0}".format( len(fs) ))
            ##main_dir = os.path.join(parent, curr)
            ref = master[ parent ] = {}
            for f in fs:
                total += 1
                file_path = os.path.join(parent, f)
                ref[ f ] = self.HashFile( file_path, mode )
        Slow_Type("\nUser path = "+path)
        hash_f = "{0}_{1}.HASHDB".format( os.path.basename( path ), mode )
        hash_path = os.path.join( os.getcwd(), "Databases", hash_f )
        f = open( hash_path, "w" )
        f.write( str(master) )
        f.close()
        Slow_Type(( sep+ "\nReport: \nFiles hashed: {0}".format(total) ))
        elap = time.time() - start
        Slow_Type(("\n\nElapsed time: {0}".format( time.strftime("%H:%M:%S", time.gmtime(elap) ) ) +
         "\nFile saved to: " + hash_path + "\n\n" ))
        ##return master

    def VerifyFile( self, hash_file, special_path, mode="SHA1" ):
        ##self.VerifyStructure( hash_file, True, special_path)
        if os.path.isabs( hash_file )==False:
            hash_file = os.path.abspath( hash_file )
            
        Slow_Type("\n\nParsing: "+hash_file)
        r = open(hash_file, "r").read()
        master = ast.literal_eval(r)
        neg = 0; total = 0

        sd = os.path.dirname( special_path )
        sf = os.path.basename( special_path )
        if sd in master:
            nested = master[sd]
            if sf in nested:
                old_hash = master[sd][sf]
                new_hash = self.HashFile( special_path, mode )
                if old_hash != new_hash:
                    Slow_Type("\n+---File changed: " + sf)
                else:
                    Slow_Type("\n+---File is valid and has been unaltered.")
            else:
                Slow_Type("\nFile not found in Hash Databse")
        else:
            Slow_Type("\nDirectory not found within Hash Databse")
        """
        for parent in master:
            subfol = master[parent]
            for f in subfol:
                path = os.path.join( parent, f )
                base = os.path.basename(path)
                if path == special_path:
                    old_hash = subfol[f]
                    new_hash = self.HashFile( path, mode )
                    if old_hash != new_hash:
                        print("+---File changed: " + base)
                        neg += 1
                    break
        if neg==0:
            print("\nFile not found!")

        """
                    

    def VerifyStructure(self, file_path, special=False, special_path=""):
        """Del is a poopy pants"""
        print( sep )
        if os.path.isabs( file_path )==False:
            file_path = os.path.abspath( file_path )
        Slow_Type("\nParsing: "+file_path)
        ## Print total before hand
        tmp = open(file_path, "r")
        r = tmp.read()
        tmp.close()
        master = ast.literal_eval(r)
        neg = 0; pos=0; total = 0     ## 3 variable declaration here
        altered = []
        legit = [] 
        start = time.time()
        for parent in master:
            subfol = master[parent]
            Slow_Type("\n\nProccessing: "+parent)
            Slow_Type("\n+-Files: {0}".format( len(subfol) ))
            for f in subfol:
                total += 1
                path = os.path.join( parent, f )
                base = os.path.basename(path)
                if os.path.exists(path)==False:
                    Slow_Type("\n+---File removed: " + base)
                    altered.append("Removed: "+path); neg+=1
                else:
                    old_hash = subfol[f]
                    new_hash = self.HashFile( path )
                    if old_hash != new_hash:
                        Slow_Type("\n+---File changed: " + base)
                        altered.append("Altered: "+path); neg+=1
                    else:
                        legit.append("Unmodified: "+path); pos+=1
                        
        ## Report statistics and allow user input
        Slow_Type(( sep+ "\nReport: \n\n{0} files altered out of {1}".format(neg, total ) ))
        Slow_Type(( "\n{0} files not altered out of {1}".format(pos, total ) ))
        elap = time.time() - start
        Slow_Type("\nElapsed time: {0}\n".format( time.strftime("%H:%M:%S", time.gmtime(elap) ) ))
        alt_master = ""; altered.sort()
        leg_master = ""; legit.sort()
        for i in altered:
            alt_master += "\n+---"+i
        for i in legit:
            leg_master += "\n+---"+i
        ## Write report to log file
        l = open("Log.txt", 'a')
        l.write("\n\n"+time.asctime()+alt_master+"\n"+leg_master)
        l.close()

        #prettyfy = lambda x : print( for i+"\n" in x)
        while True:
            print("\n\na. Display altered files \tb. Display unmodified files \nc. Return to Main Menu \t\td. Exit ")
            ans = input("> ").upper()
            if "A" in ans: 
                if len(alt_master)>1: Slow_Type( alt_master+"\n\n" +sep+"\n", 0.000003)
                else: Slow_Type("\nNo files to show.")
            elif "B" in ans:
                if len(leg_master)>1: Slow_Type(leg_master+"\n\n" +sep+"\n", 0.000003)
                else: Slow_Type("\nNo files to show.")
            elif "C" in ans:
                return
            else:
                sys.exit()
                
            
        ##return master


if __name__=='__main__':
    ## Start main class.
    Main()

#m = Main()
#path = "C:\Users\Chris\Documents\Archive\_Users"
#m.CreateTable( path )

class deadlock(object):
    '''
        A deadlock tuytorial has
        state:
        processes:
        resources:
        steps:
    '''
    def __init__(self, file):
        '''
        sets up the initial state of the deadlock tutorial
        '''
        self.numProcs, self.numResc, self.steps = self.readInputFile(file)
        self.state = self.makeStruct(self.numProcs)
        self.procList = [(lambda x: x)(x) for x in range(0,self.numProcs)]
        self.rescList = [(lambda x: x)(x) for x in range(self.numProcs, self.numResc+self.numProcs)]
        self.rescMap = self.mapResources()

    def mapResources(self):
        info = {}
        for item in range(0, self.numResc):
            info[item] = self.rescList[item]
        return info

    # getters
    def makeProcsLables(self):
        p = []
        for item in range(0, self.numProcs):
            p.append("P"+str(item))
        return p

    def makeRescLables(self):
        r = []
        for item in range(0, self.numResc):
            r.append("R"+str(item))
        return r

    def getListProcs(self):
        return self.procList

    def getListResc(self):
        return self.rescList

    def getNumProcs(self):
        return self.numProcs
    def getNumResc(self):
        return self.numResc
    def getSteps(self):
        return self.steps
    def getState(self):
        return self.state

    def textForStep(self, numProcs, numResc, step ):
        initial = "There are " + str(numProcs) + " processes and "+numResc+" resources in this system"\
                " This system is going to teach you about deadlock"\
                " There are four"

    def makeStruct(self, numProcs):
        '''
            how the gme knows who is requesting who
            and who owns who and who is blocking
            we track this by a dictionary of preocesses as keys to three other
            dicts of "req" , "block", "own" which are all lists of resources
            structure:
            dict<pids,
                    dict<block,list<rids>>,
                    dict<req,list<rids>>,
                    dict<own,list<rids>>
                >
        '''
        structure = {}
        for process in range(0, numProcs):
            structure[process] = {"blocking": [], "owned": [], "requested": [], "waitingFor":[]}
        return structure

    def nextStep(self):
        '''
            takes in the structure and the next state
            edits the structure based on new move
            possible states:
            1. pi requests ri
            2. pi releases ri
            3. end/nothing left
            4. deadlock check
        '''
        if (len(self.steps) > 0):
            stepToDo =  self.steps[0]
            self.steps.pop(0)
        else:
            return "END GAME"



        if "request" in stepToDo: # pi asks for ri
            # edit the states
            pid = int(stepToDo[0:stepToDo.index(" requests")].replace("p",""))
            rid = int(stepToDo[stepToDo.index(" requests ")+len(" requests "):].replace("r",""))
            self.state = self.request(pid, rid, self.state);

            return stepToDo

        if "releases" in stepToDo: # pi lets go of ri
            # edit the states
            pid = int(stepToDo[0:stepToDo.index(" releases")].replace("p",""))
            rid = int(stepToDo[stepToDo.index(" releases ")+len(" releases "):].replace("r",""))
            self.state = self.release(pid, rid, self.state)

            return stepToDo

    def request(self, pid, rid, currentStruct):
        #check if another process owns this resource
        newStruct = currentStruct
        alreadyOwnedByAnother = False
        for process in newStruct:
            if self.rescMap[rid] in newStruct[process]["owned"] and pid != process:
                # is the rid already owned, not by me
                # add rid to pids request edge
                newStruct[pid]["requested"].append(self.rescMap[rid]) #mark that we want it
                newStruct[process]["blocking"].append((pid, self.rescMap[rid]))
                newStruct[pid]["waitingFor"].append(process)
                alreadyOwnedByAnother = True

        if alreadyOwnedByAnother == False :
            # the resource is NOT owned by another process sp we can own it
            newStruct[pid]["owned"].append(self.rescMap[rid])

        return newStruct

    def release(self, pid, rid, currentStruct):
        newStruct = currentStruct
        if self.rescMap[rid] in newStruct[pid]["owned"]:
            # we own the process we want to release
            # check if any one was blokced on that who now gets to own that resource and if any other processes allso requested it after that then they are now blokced by who now owns it
            newStruct[pid]["owned"].remove(self.rescMap[rid]) # i dont own it anymore
            reqFirst = False
            for tuple in newStruct[pid]["blocking"]:
                if tuple[1] == self.rescMap[rid] and reqFirst == False:
                    newStruct = self.request(tuple[0], rid, newStruct)
                    newStruct[pid]["blocking"].remove(tuple)
                    newStruct[tuple[0]]["waitingFor"].remove(pid)
                    newStruct[tuple[0]]["requested"].remove(self.rescMap[rid])
                    reqFirst = True
                elif tuple[1] == self.rescMap[rid]:
                    # the previous process was blocking more than one process on this resources
                    # so the new process who owns the resource will need to track blocking those
                    newStruct[tuple[0]]["blocking"].append(tuple)
                    newStruct[pid]["blocking"].remove(tuple)
        return newStruct

    def readInputFile(self, file):
        ''' read the input file and place it into a list
            read resource number from that list
            read process number form that list
            return list, resource number, and process number
        '''
        # get list of steps
        with open(file) as f:
            content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            content = [x.strip() for x in content]

        # get process number
        processes = int(content[0][ 0 : content[0].index(" processes")])
        content.pop(0)

        # get resource number
        resources = int(content[0][ 0 : content[0].index(" resources")])
        content.pop(0)

        return processes, resources, content

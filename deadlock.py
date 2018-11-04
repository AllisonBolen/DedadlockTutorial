class deadlock(object):
    '''
        A deadlock tuytorial has
        state:
        processes:
        resources:
        steps:
    '''
    def __init__(self):
        '''
        sets up the initial state of the deadlock tutorial
        '''
        self.procs, self.recs, self.steps = self.readInputFile()
        self.state = self.makeStruct(self.procs)

    # getters
    def makeNodeProcs(self):
        p = []
        for item in range(0, self.procs):
            p.append("P"+str(item))
        return p

    def makeNodeRecs(self):
        r = []
        for item in range(0, self.recs):
            r.append("R"+str(item))
        return r

    def getProcs(self):
        return self.procs
    def getRecs(self):
        return self.recs
    def getSteps(self):
        return self.steps
    def getState(self):
        return self.state

    def All():
            #read in file data
            procs, recs, steps = readInputFile()

            struct = makeStruct(procs)
            print("Initial struct: " + str(struct))

            while len(steps)-1 >= 0:
                struct = nextStep(struct, steps[0])
                print("\n\nStructure at '"+str(steps[0])+"' : "+str(struct))
                #print("Steps: "+str(steps)+"\n\n")
                steps.pop(0)

            print("")

            undo()

    def textForStep(self, procs, recs, step ):
        initial = "There are " + str(procs) + " processes and "+recs+" resources in this system"\
                " This system is going to teach you about deadlock"\
                " There are four"

    def makeStruct(self, procs):
        '''
            how the gme knows who is requesting who
            and who owns who and who is blocked
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
        for process in range(0, procs):
            structure["p"+str(process)] = {"blocked": [], "owned": [], "requested": []}
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
            pid = stepToDo[0:stepToDo.index(" requests")]
            rid = stepToDo[stepToDo.index(" requests ")+len(" requests "):]
            self.state = self.request(pid, rid, self.state);

            return stepToDo

        if "releases" in stepToDo: # pi lets go of ri
            # edit the states
            pid = stepToDo[0:stepToDo.index(" releases")]
            rid = stepToDo[stepToDo.index(" releases ")+len(" releases "):]
            self.state = self.release(pid, rid, self.state)

            return stepToDo

    def request(self, pid, rid, currentStruct):
        #check if another process owns this resource
        newStruct = currentStruct
        alreadyOwnedByAnother = False
        for process in newStruct:
            if rid in newStruct[process]["owned"] and pid != process:
                # is the rid already owned, not by me
                # add rid to pids request edge
                newStruct[pid]["requested"].append(rid) #mark that we want it
                newStruct[process]["blocked"].append((pid, rid))
                alreadyOwnedByAnother = True

        if alreadyOwnedByAnother == False :
            # the resource is NOT owned by another process sp we can own it
            newStruct[pid]["owned"].append(rid)

        return newStruct

    def release(self, pid, rid, currentStruct):
        newStruct = currentStruct
        if rid in newStruct[pid]["owned"]:
            # we own the process we want to release
            # check if any one was blokced on that who now gets to own that resource and if any other processes allso requested it after that then they are now blokced by who now owns it
            newStruct[pid]["owned"].remove(rid) # i dont own it anymore
            reqFirst = False
            for tuple in newStruct[pid]["blocked"]:
                if tuple[1] == rid and reqFirst == False:
                    newStruct = self.request(tuple[0], rid, newStruct)
                    newStruct[pid]["blocked"].remove(tuple)

                    reqFirst = True
                elif tuple[1] == rid:
                    # the previous process was blocking more than one process on this resources
                    # so the new process who owns the resource will need to track blocking those
                    newStruct[tuple[0]]["blocked"].append(tuple)
                    newStruct[pid]["blocked"].remove(tuple)

        return newStruct

    def undo(self):
        print("UNDO")

    def readInputFile(self):
        ''' read the input file and place it into a list
            read resource number from that list
            read process number form that list
            return list, resource number, and process number
        '''
        # get list of steps
        with open("input3a.data") as f:
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


def main():

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

def makeStruct(procs):
    '''
        how the gme knows who is requesting who
        and who owns who and who is blocked
        we track this by a dictionary of preocesses as keys to three other
        dicts of "req" , "block", "own" which are all lists of resources
        structure:
        dict<pids,
            list<
                dict<block,list<rids>>,
                dict<req,list<rids>>,
                dict<own,list<rids>>
                >
            >
    '''
    print("STATE")
    structure = {}
    for process in range(0, procs):
        structure[process] = {"blocked": [], "owned": [], "requested": []}
    return structure

def nextStep(currentStruct, stepToDo):
    '''
        takes in the structure and the next state
        edits the structure based on new move
        possible states:
        1. pi requests ri
        2. pi releases ri
        3. end/nothing left
        4. deadlock check
    '''
    print("BEGIN NEXT")

    if "request" in stepToDo: # pi asks for ri
        print("request")
        # edit the states
        pid = int(stepToDo[0:stepToDo.index(" requests")].replace("p",""))
        rid = int(stepToDo[stepToDo.index(" requests ")+len(" requests "):].replace("r",""))
        newStruct = request(pid, rid, currentStruct);

        print("END NEXT REQUEST")
        return newStruct

    if "releases" in stepToDo: # pi lets go of ri
        print("releases")
        # edit the states
        pid = int(stepToDo[0:stepToDo.index(" releases")].replace("p",""))
        rid = int(stepToDo[stepToDo.index(" releases ")+len(" releases "):].replace("r",""))
        newStruct = release(pid, rid, currentStruct)

        print("End release")
        return newStruct

def request(pid, rid, currentStruct):
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


def release(pid, rid, currentStruct):
    newStruct = currentStruct
    if rid in newStruct[pid]["owned"]:
        # we own the process we want to release
        # check if any one was blokced on that who now gets to own that resource and if any other processes allso requested it after that then they are now blokced by who now owns it
        newStruct[pid]["owned"].remove(rid) # i dont own it anymore
        reqFirst = False
        for tuple in newStruct[pid]["blocked"]:
            if tuple[1] == rid and reqFirst == False:
                newStruct = request(tuple[0], rid, newStruct)
                newStruct[pid]["blocked"].remove(tuple)

                reqFirst = True
            elif tuple[1] == rid:
                # the previous process was blocking more than one process on this resources
                # so the new process who owns the resource will need to track blocking those
                newStruct[tuple[0]]["blocked"].append(tuple)
                newStruct[pid]["blocked"].remove(tuple)

    return newStruct

def undo():
    print("UNDO")

def readInputFile():
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

if __name__ == "__main__": main()

import deadlock
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import networkx as nx
import sys, os, shutil


def main():
    setup(sys.argv[1])
    dl = deadlock.deadlock(str(sys.argv[1]))
    steps = dl.getSteps()
    fig = plt.figure()
    names = dl.makeProcsLables() + dl.makeRescLables()
    processes = dl.getListProcs()
    resources = dl.getListResc()
    labels = createLabels(names, processes, resources)
    count = 0
    step = "Initial"

    # text bools
    dead = False
    stepText = ""
    while(step != "END GAME"):
        edges = convertStateToEdges(dl.getState(),resources, processes)
        dead, waitEdges = deadCheck(dl, processes)
        graph = run(names, processes, resources, labels, edges)
        stepText = textGen(step, count, steps, dl, stepText, dead, waitEdges)
        # plt.text(5,5,stepText)
        plt.axis('off')
        # plt.pause(1)
        # plt.draw()

        saveFile(sys.argv[1], step, count, stepText)
        stepText = ""
        print(count)
        print(step)
        print(len(steps))
        print()
        step = dl.nextStep()
        count = count + 1

    return

def deadCheck(dl, processes):
    state = dl.getState()
    waitEdgeList = []
    for process in state:
        if len(state[process]["waitingFor"]) > 0:
            for edge in state[process]["waitingFor"]:
                waitEdgeList.append((process,edge))

    graph = nx.DiGraph()
    graph.add_nodes_from(processes)
    graph.add_edges_from(waitEdgeList)
    # nx.draw(graph, with_labels=True)

    try:
        nx.find_cycle(graph, orientation='original')
        return True, waitEdgeList
    except:
        pass
    return False, waitEdgeList

def textGen( step, count, steps, dl, stepText, dead, waitEdges):
    text = ""
    if step == "Initial" :
        text = "This is a graph with "+str(dl.getNumProcs())+" processes and "+str(dl.getNumResc())+"resources."\
        "Using this graph you will see the methodology of resource allocation."\
        "Make sure to keep and eye out for deadlock conditions. Our system holds for mutual exclusion: no two processes can own the smae resource at the same time"\
        ", hold and wait: a process must be holding at least one resouce and be waiting to aquire resources that are owned by another process, no preemption: process can not steal resources from "\
        "another process before the process is finished with the resource, and circular: where there is a cycle of a process wating on a reousrce where the owner of that resource is waiting for the process who is wating for it."
        "To see states click next."
    else:

        if dead is True and len(steps) > 0:
            # we are deadlocked and its not the end of teh system yet
            text = "This is step "+str(count)+": '"+step+"'."\
            "\nIn this step we see that we are in a dead lock state along these directed edges: "+str(waitEdges)+"."

        elif dead is True and len(steps) == 0:
            # we are in a state of deadlock and it is the last steps
            text = "This is step "+str(count)+": '"+step+"'."\
            "\nIn this step we see that we are in a dead lock state along these directed edges: "+str(waitEdges)+"."\
            "\nThis is the last step and we are ending in a deadlocked state."
        elif dead is False and len(steps) > 0:
            # we are not deadlocked but we are at the end of teh GAME
            text = "This is step "+str(count)+": '"+step+"'."\

        elif dead is False and len(steps) == 0:
            # we are not dead and we are not the END
            text = "This is step "+str(count)+": '"+step+"'."\
            "\nThis is the last step."

    return text

def setup(asocFile):
    dir = asocFile[:asocFile.index(".")]
    if os.path.isdir(dir) is True:
        shutil.rmtree(dir)
    if os.path.isdir(dir) is False:
        os.mkdir(dir)
        os.makedirs(dir+"/text")
        os.makedirs(dir+"/images")

def saveFile(asocFile, step, count, text):
    # save figure
    dirname = os.path.dirname("deadlock.py")
    dir = asocFile[:asocFile.index(".")]
    filename = os.path.join("", dir+"/images/"+str(count)+".png")
    plt.axis('off')
    plt.savefig(filename)
    #save text
    with open(dir+"/text/"+str(count)+".txt", "w") as text_file:
        print(text, file=text_file)

def createLabels(names, processes, resources):
    info = {}
    for item in range(0, (resources[len(resources)-1])+1):
        info[item]= names[item]
    return info

def run(names, processes, resources, labels, edges):

    B = nx.DiGraph()
    B.add_nodes_from(processes+resources)
    pos = {}

    countP = 1
    countR = 1

    for node in processes+resources:
        if node in processes:
            B.node[node]['pos'] = (countP*10,10)
            pos[node]=(countP*10,20)
            countP = countP + 1
        if node in resources:
            B.node[node]['pos'] = (countR*10,80)
            pos[node]=(countR*10,80)
            countR = countR + 1




    nx.draw_networkx_nodes(B, pos,
                               nodelist=processes,
                               node_color='g',
                               node_size=600,
                               alpha=0.8,
                               label="Processes")

    nx.draw_networkx_nodes(B, pos,
                               nodelist=resources,
                               node_color='y',
                               node_size=600,
                               node_shape='s',
                               alpha=0.8,
                               label="Resources")

    nx.draw_networkx_edges(B, pos,
                               edgelist=edges,
                               width=2, alpha=1, arrows=True, arrowstyle='->', arrowsize=20)


    nx.draw_networkx_labels(B, pos, labels, font_size=16)


    return B

def convertStateToEdges(state, resources, processes):
    '''
    create directed edge lists out of teh state of the machine
    '''
    edgeList = []
    for process in state:
        if len(state[process]["owned"]) > -1:
            # we own something so teh dir should go from resourc to processes
            for resource in state[process]["owned"]:
                if (resource, process) not in edgeList:
                    edgeList.append((resource, process))

        if len(state[process]["requested"]) > -1:
            for resource in state[process]["requested"]:
                if (resource, process) not in edgeList:
                    edgeList.append((process, resource))

    return edgeList

if __name__ == "__main__": main()

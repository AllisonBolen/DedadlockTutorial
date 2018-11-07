import deadlock
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import networkx as nx
import sys, os, shutil


def main():
    '''
    This interprets the deadlock file as a graph and
    saves each stage to an image file for loading into a gui
    later on. It also tracks the text and saves them to a file.
    '''
    setup(sys.argv[1])
    # create an instance of the deadlock class
    dl = deadlock.deadlock(str(sys.argv[1]))
    steps = dl.getSteps()
    fig = plt.figure()
    # initial set up of the graph
    names = dl.makeProcsLables() + dl.makeRescLables()
    processes = dl.getListProcs()
    resources = dl.getListResc()
    labels = createLabels(names, processes, resources)

    stepCount = 0
    step = "Initial"

    edges = []
    while(step != "END GAME"):
        prevEdges = edges
        # get the new edges
        edges = convertStateToEdges(dl.getState(),resources, processes)
        # are we in a state of deadlock based on the new edges
        dead, waitEdges = deadCheck(dl, processes)
        # generate text description of the graph
        print()
        print(step)
        print(prevEdges)
        print(edges)
        stepText = textGen(step, stepCount, steps, dl, dead, waitEdges, set(prevEdges)==set(edges))
        # create the graph given the new state of the game
        graph = run(names, processes, resources, labels, edges)
        plt.axis('off')
        # testing purpose
        # plt.pause(1)
        # plt.draw()
        # save the graph as and image and the text description for gui use
        saveFile(sys.argv[1], step, stepCount, stepText)
        # reset text and figure
        plt.clf()
        stepText = ""
        # move to the next state of the game
        step = dl.nextStep()
        stepCount = stepCount + 1

    return

def deadCheck(dl, processes):
    '''
    We only need to check for dead lock because ME, HW and NoP are coded into
    the simulation so all we need to check for are cycles.
    The best way to do this is to use a derivative of our state graph
    called a wait for grph that shows what processes are dependent on other
    processes. If we find a cycle in that directed graph then we are in
    deadlock.
    '''
    # calculate the wait graph
    state = dl.getState()
    waitEdgeList = []
    for process in state:
        if len(state[process]["waitingFor"]) > 0:
            for edge in state[process]["waitingFor"]:
                waitEdgeList.append((process,edge))

    # make the graph
    graph = nx.DiGraph()
    graph.add_nodes_from(processes)
    graph.add_edges_from(waitEdgeList)

    try:
        # cycle is found with built in function
        nx.find_cycle(graph, orientation='original')
        return True, waitEdgeList
    except:
        pass
    return False, waitEdgeList

def textGen(step, count, steps, dl, dead, waitEdges, stateChange):
    '''
    Generates text description for each state of the game.
    '''
    print(stateChange)
    text = ""
    if step == "Initial" :
        text = "This is a graph with "+str(dl.getNumProcs())+" processes and "+str(dl.getNumResc())+" resources."\
        " This is a graphical simulation of resource allocation."\
        " Our system holds for mutual exclusion: no two processes can own the same resource at the same time,"\
        " hold and wait: a process must be holding at least one resouce and be waiting to aquire resources that are owned by another process, no preemption: process can not steal resources from "\
        " another process before a process is finished with a resource, and circular: there is a cycle of a processes dependent on other processes."
        " Use the left and right arrows to navigate between steps of the simulation."
    else:

        if len(steps) >= 0:
            text = "Step "+str(count)+": '"+step+"'."

        if len(steps) == 0:
            text = text + " This is the last step."

        if dead is True:
            # we are deadlocked
            text = text + " In this step we see that we are in a dead lock state along these directed edges: "+str(waitEdges)+". Where (x,y) x -> y."

        if stateChange is True:
            # we are the same as last step so that means we resuwsted soemthing when we cant get it.
            text  = text + " The state has not changed because of the hold and wait condition of this system"\
            " So '" + step[:step.index(" re")] + "' has already requested something in a previous step and thus can not do anything else while it is waiting."

    return text

def setup(asocFile):
    '''
    Make/clean directories that we'll need to store images in

    '''
    dir = asocFile[:asocFile.index(".")]
    if os.path.isdir(dir) is True:
        shutil.rmtree(dir)
    os.mkdir(dir)
    os.makedirs(dir+"/text")
    os.makedirs(dir+"/images")

def saveFile(asocFile, step, count, text):
    '''
    Save the graph as and image and save the text for use in the Gui
    '''
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
    '''
    Make the node labels
    '''
    info = {}
    for item in range(0, (resources[len(resources)-1])+1):
        info[item]= names[item]
    return info

def run(names, processes, resources, labels, edges):
    '''
    Make the user facing graph based on our current edge state

    '''

    B = nx.DiGraph()
    B.add_nodes_from(processes+resources)
    pos = {}

    countP = 1
    countR = 1

    # setup node location on the graph
    for node in processes+resources:
        if node in processes:
            B.node[node]['pos'] = (countP*10,10)
            pos[node]=(countP*10,20)
            countP = countP + 1
        if node in resources:
            B.node[node]['pos'] = (countR*10,80)
            pos[node]=(countR*10,80)
            countR = countR + 1

    # graph the process nodes
    nx.draw_networkx_nodes(B, pos,
                               nodelist=processes,
                               node_color='g',
                               node_size=600,
                               alpha=0.8,
                               label="Processes")
    # graph the resource nodes
    nx.draw_networkx_nodes(B, pos,
                               nodelist=resources,
                               node_color='y',
                               node_size=600,
                               node_shape='s',
                               alpha=0.8,
                               label="Resources")
    # graph the edges
    nx.draw_networkx_edges(B, pos,
                               edgelist=edges,
                               width=2, alpha=1, arrows=True, arrowstyle='->', arrowsize=20)

    # draw everything properly
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
            # we woant something do it should point the other way now
            for resource in state[process]["requested"]:
                if (resource, process) not in edgeList:
                    edgeList.append((process, resource))

    return edgeList

if __name__ == "__main__": main()

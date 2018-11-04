import deadlock
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import networkx as nx
import pylab
pylab.ion

def main():

    dl = deadlock.deadlock()
    steps = dl.getSteps()


    G = nx.DiGraph()
    # set up initial nodes
    G.add_nodes_from(dl.makeNodeRecs()+dl.makeNodeProcs())
    color = colors(G)
    step = ""
    while(step != "END GAME"):
        step = dl.nextStep()
        fig = get_fig(dl, G, color)
        txt = plt.text(50, 50, 'TESTTEST', fontsize=8)
        fig.canvas.draw()
        pylab.draw()

        plt.pause(10)
        pylab.close()


    # G.add_nodes_from([0,dl.getRecs()])
    # G.add_nodes_from([0,dl.getProcs()])
    # nx.draw(G, pos=pos)
    # plt.show()

def get_fig(dl, G, color):
    #convertStateToEdges(dl.getState())
    edges = convertStateToEdges(dl.getState())
    print(edges)
    G.add_edges_from(edges)
    fig = pylab.figure()
    nx.draw(G, with_labels=True, node_color=color)
    return fig

def convertStateToEdges( state ):
    '''
    create directed edge lists out of teh state of the machine
    '''
    edgeList = []
    for process in state:
        if len(state[process]["owned"]) > -1:
            # we own something so teh dir should go from resourc to processes
            for resource in state[process]["owned"]:
                if (resource.upper(), process.upper()) not in edgeList:
                    edgeList.append((resource.upper(), process.upper()))

        if len(state[process]["requested"]) > -1:
            for resource in state[process]["requested"]:
                if (resource.upper(), process.upper()) not in edgeList:
                    edgeList.append((process.upper(), resource.upper()))

    return edgeList

def colors(G):
    color_list = []
    for node in G:
        if "R" in node:
            color_list.append("yellow")
        else :
            color_list.append("green")

    return color_list
if __name__ == "__main__": main()

#
# hw3pr1.py
#
#  lab problem - matplotlib tutorial (and a bit of numpy besides...)
#
# this asks you to work through the first part of the tutorial at
#     www.labri.fr/perso/nrougier/teaching/matplotlib/
#   + then try the scatter plot, bar plot, and one other kind of "Other plot"
#     from that tutorial -- and create a distinctive variation of each
#
# include screenshots or saved graphics of your variations of those plots with the names
#   + plot_scatter.png, plot_bar.png, and plot_choice.png
#
# Remember to run  %matplotlib  at your ipython prompt!
#
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#
# in-class examples...
#

def inclass1():
    """
    Simple demo of a scatter plot.
    """
    import numpy as np
    import matplotlib.pyplot as plt


    N = 50
    x = np.random.rand(N)
    y = np.random.rand(N)
    colors = np.random.rand(N)
    area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses

    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.show()



#
# First example from the tutorial/walkthrough
#


#
# Feel free to replace this code as you go -- or to comment/uncomment portions of it...
#

def example1():
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    C,S = np.cos(X), np.sin(X)

    plt.plot(X,C)
    plt.plot(X,S)

    plt.show()
#
# Here is a larger example with many parameters made explicit
#

def example2():
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    # Create a new figure of size 8x6 points, using 100 dots per inch
    plt.figure(figsize=(8,6), dpi=80)

    # Create a new subplot from a grid of 1x1
    plt.subplot(111)

    X = np.linspace(-np.pi, np.pi, 256,endpoint=True)
    C,S = np.cos(X), np.sin(X)

    # Plot cosine using blue color with a continuous line of width 1 (pixels)
    plt.plot(X, C, color="blue", linewidth=1.0, linestyle="-")

    # Plot sine using green color with a continuous line of width 1 (pixels)
    plt.plot(X, S, color="green", linewidth=1.0, linestyle="-")

    # Set x limits
    plt.xlim(-4.0,4.0)

    # Set x ticks
    plt.xticks(np.linspace(-4,4,9,endpoint=True))

    # Set y limits
    plt.ylim(-1.0,1.0)

    # Set y ticks
    plt.yticks(np.linspace(-1,1,5,endpoint=True))

    # Save figure using 72 dots per inch
    # savefig("../figures/exercice_2.png",dpi=72)

    # Show result on screen
    plt.show()


#
# using style sheets:
#   # be sure to               import matplotlib
#   # list of all of them:     matplotlib.style.available
#   # example of using one:    matplotlib.style.use( 'seaborn-paper' )
#

def scatterPlot1():
    """ scatterPlot1 randomly produces a scatter plot that follows
        the online tutorial challenge.
    """
    n = 1024
    X = np.random.normal(0,1,n)
    Y = np.random.normal(0,1,n)
    T = np.arctan2(Y,X)

    plt.axes([0.025,0.025,0.95,0.95])
    plt.scatter(X,Y, s=75, c=T, alpha=.5)

    plt.xlim(-1.5,1.5), plt.xticks([])
    plt.ylim(-1.5,1.5), plt.yticks([])
    # savefig('../figures/scatter_ex.png',dpi=48)
    plt.show()

def scatterPlot2():
    """ scatterPlot2 produces a variation of scatterPlot1.
    """
    N = 100
    x = np.random.rand(N)
    y = np.random.rand(N)
    colors = np.random.rand(N)

    plt.scatter(x, y, c=colors, alpha=0.5)
    plt.show()
# scatterPlot2()

def barPlot1():
    """ barPlot produces a bar plot that follows the online tutorial challenge.
    """
    n = 12
    X = np.arange(n)
    Y1 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)
    Y2 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)

    plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
    plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')

    for x,y in zip(X,Y1):
        plt.text(x+0.2, y+0.05, '%.2f' % y, ha='center', va= 'bottom')

    for x,y in zip(X,Y2):
        plt.text(x+0.2, -y-0.1, '%.2f' % y, ha='center', va= 'bottom')

    plt.ylim(-1.25,+1.25)
    plt.show()
# barPlot()

def barPlot2():
    """ barPlot2 produces a variation of barPlot1.
    """
    n = 10
    X = np.arange(n)
    Y1 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)
    plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')

    for x,y in zip(X,Y1):
        plt.text(x+0.2, y+0.05, '%.2f' % y, ha='center', va= 'bottom')

    plt.ylim(0,1.25)
    plt.show()
barPlot2()

def pieChart1():
    """ pieChart1 produces a pie Chart that follows the online tutorial challenge.
    """
    n = 20
    Z = np.ones(n)
    Z[-1] *= 2

    plt.axes([0.025,0.025,0.95,0.95])

    plt.pie(Z, explode=Z*.05, colors = ['%f' % (i/float(n)) for i in range(n)])
    plt.gca().set_aspect('equal')
    plt.xticks([]), plt.yticks([])

    # savefig('../figures/pie_ex.png',dpi=48)
    plt.show()


def pieChart2():
    """ pieChart2 produces a pie chart with 4 variables and different colors.
    """
    n = 4
    Z = np.ones(n)
    Z[-1] *= 2

    labels = 'A', 'B', 'C', 'D'
    plt.axes([0.025,0.025,0.95,0.95])

    plt.pie(Z, explode=Z*.05, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.gca().set_aspect('equal')
    plt.xticks([]), plt.yticks([])

    # savefig('../figures/pie_ex.png',dpi=48)
    plt.show()

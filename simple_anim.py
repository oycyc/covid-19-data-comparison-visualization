
#importing libraries
import matplotlib.pyplot as plt
import matplotlib.animation as animation


fig = plt.figure()
#creating a subplot 
ax1 = fig.add_subplot(5,1,1)

xs = [1]
ys = [1]

   

def animate(i):

    xs.append(xs[-1] * 1.45)
    ys.append(ys[-1] * 10.45)
    
    ax1.clear()
    ax1.plot(xs, ys)

    plt.xlabel('Date')
    plt.ylabel('asd')
    plt.title('Live graph with matplotlib')	
	
    
ani = animation.FuncAnimation(fig, animate, interval=1000) 
plt.show()


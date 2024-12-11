import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv

class DoublePendulum:
    def __init__(self, L1=1.0, L2=1.0, M1=1.0, M2=1.0, 
                 G=9.8, th1=120.0, w1=0.0, th2=-10.0, w2=0.0, t_stop=5, dt=0.01):
        """
        Initializes the double pendulum with default or custom parameters.
        """
        # Static parameters
        self.L1 = L1  # Length of the first pendulum (m)
        self.L2 = L2  # Length of the second pendulum (m)
        self.M1 = M1  # Mass of the first pendulum (kg)
        self.M2 = M2  # Mass of the second pendulum (kg)
        self.G = G    # Gravitational acceleration (m/s^2)

        # Initial conditions
        self.th1 = th1  # Initial angle of the first pendulum (degrees)
        self.w1 = w1   # Initial angular velocity of the first pendulum (degrees/s)
        self.th2 = th2  # Initial angle of the second pendulum (degrees)
        self.w2 = w2   # Initial angular velocity of the second pendulum (degrees/s)
        
        # Time parameters
        self.t_stop = t_stop  # Total simulation time (s)
        self.dt = dt          # Time step (s)
        self.t = np.arange(0, t_stop, dt)

        # Initial state
        self.state = np.radians([self.th1, self.w1, self.th2, self.w2])

        # Simulation results
        self.y = None 

    def set_parameters(self, L1, L2, M1, M2, G):
        """Updates the static parameters of the system."""
        self.L1 = L1
        self.L2 = L2
        self.M1 = M1
        self.M2 = M2
        self.G = G
    
    def set_time_parameters(self, t_stop, dt):
        """Updates the time-related parameters of the simulation."""
        self.t_stop = t_stop
        self.dt = dt
        self.t = np.arange(0, t_stop, dt)

    def set_initial_conditions(self, th1, w1, th2, w2):
        """Updates the initial conditions of the system."""
        self.th1 = th1
        self.w1 = w1
        self.th2 = th2
        self.w2 = w2
        self.state = np.radians([self.th1, self.w1, self.th2, self.w2])

    def _derivs(self, state):
        """Differential equations of the double pendulum."""
        dydx = np.zeros_like(state)
        delta = state[2] - state[0]

        den1 = (self.M1 + self.M2) * self.L1 - self.M2 * self.L1 * np.cos(delta) ** 2
        dydx[0] = state[1]
        dydx[1] = ((self.M2 * self.L1 * state[1] ** 2 * np.sin(delta) * np.cos(delta)
                    + self.M2 * self.G * np.sin(state[2]) * np.cos(delta)
                    + self.M2 * self.L2 * state[3] ** 2 * np.sin(delta)
                    - (self.M1 + self.M2) * self.G * np.sin(state[0]))
                   / den1)

        den2 = (self.L2 / self.L1) * den1
        dydx[2] = state[3]
        dydx[3] = ((-self.M2 * self.L2 * state[3] ** 2 * np.sin(delta) * np.cos(delta)
                    + (self.M1 + self.M2) * self.G * np.sin(state[0]) * np.cos(delta)
                    - (self.M1 + self.M2) * self.L1 * state[1] ** 2 * np.sin(delta)
                    - (self.M1 + self.M2) * self.G * np.sin(state[2]))
                   / den2)

        return dydx

    def solve(self):
        """Solves the equations of the double pendulum."""
        y = np.empty((len(self.t), 4))
        y[0] = self.state
        for i in range(1, len(self.t)):
            y[i] = y[i - 1] + self._derivs(y[i - 1]) * self.dt
        self.y = y

    def animate(self):
        """Creates and displays the animation of the double pendulum."""
        if self.y is None:
            raise ValueError("You must solve the system before animating it.")
        
        x1 = self.L1 * np.sin(self.y[:, 0])
        y1 = -self.L1 * np.cos(self.y[:, 0])
        x2 = self.L2 * np.sin(self.y[:, 2]) + x1
        y2 = -self.L2 * np.cos(self.y[:, 2]) + y1

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set(xlim=(-self.L1 - self.L2 -  0.5, self.L1 + self.L2 + 0.5), ylim=(-self.L1 - self.L2 - 0.5, self.L1 + self.L2 + 0.5))
        ax.set_aspect('equal')
        ax.grid()

        ax.set_xlabel('X Position (m)') 
        ax.set_ylabel('Y Position (m)')
        ax.set_title('Double Pendulum Motion') 

        line, = ax.plot([], [], 'o-', lw=2, color='black')
        trace, = ax.plot([], [], '.-', lw=1, ms=2, color='blue')
        time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

        def _update(i):
            x_i = [0, x1[i], x2[i]]
            y_i = [0, y1[i], y2[i]]
            history_x = x2[:i]
            history_y = y2[:i]
            line.set_data(x_i, y_i)
            trace.set_data(history_x, history_y)
            time_text.set_text(f'Time = {i * self.dt:.1f} s')
            return line, trace, time_text

        ani= animation.FuncAnimation(fig, _update, frames=len(self.y), interval=self.dt * 1000, blit=True)
        #ani.save("img/double_pendulum.gif", writer=animation.PillowWriter(fps=30, loop=0))
        plt.show()

    def save(self, filename):
        """Saves the state evolution of the double pendulum to a CSV file."""
        if self.y is None:
            raise ValueError("You must solve the system before saving data.")

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            writer.writerow(['th1 (rad)', 'w1 (rad/s)', 'th2 (rad)', 'w2 (rad/s)'])
            
            for i in range(len(self.t)):
                th1, w1, th2, w2 = self.y[i]
                writer.writerow([th1, w1, th2, w2])

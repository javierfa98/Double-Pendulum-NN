import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv

class DoublePendulumOnCart:
    def __init__(self, L1=1.0, L2=1.0, M1=1.0, M2=1.0, Mc=1.0, 
                 G=9.8, x_min = -1.0, x_max = 1.0, f_min = -10, f_max = 10,
                 th1=170.0, w1=0.0, th2=0.0, w2=0.0, x=0.0, vx=0.0, t_stop=5, dt=0.01):
        """
        Initializes the double pendulum on a cart with default or custom parameters.
        """
        # Static parameters
        self.L1 = L1  # Length of the first pendulum (m)
        self.L2 = L2  # Length of the second pendulum (m)
        self.M1 = M1  # Mass of the first pendulum (kg)
        self.M2 = M2  # Mass of the second pendulum (kg)
        self.Mc = Mc  # Mass of the cart (kg)
        self.G = G    # Gravitational acceleration (m/s^2)
        self.x_min = x_min # Minimum cart position (m)
        self.x_max = x_max # Maximum cart position (m)
        self.f_min = f_min # Minimum cart force (N)
        self.f_max = f_max # Maximum cart force (N)

        # Initial conditions
        self.th1 = th1  # Initial angle of the first pendulum (degrees)
        self.w1 = w1    # Initial angular velocity of the first pendulum (degrees/s)
        self.th2 = th2  # Initial angle of the second pendulum (degrees)
        self.w2 = w2    # Initial angular velocity of the second pendulum (degrees/s)
        self.x = x      # Initial horizontal position of the cart (m)
        self.vx = vx    # Initial velocity of the cart (m/s)
        
        # Time parameters
        self.t_stop = t_stop  # Total simulation time (s)
        self.dt = dt          # Time step (s)
        self.t = np.arange(0, t_stop, dt)

        # Initial state: [th1, w1, th2, w2, x, vx]
        self.state = np.radians([self.th1, self.w1, self.th2, self.w2])
        self.state = np.append(self.state, [self.x, self.vx])

        # External input (force on cart)
        self.control_force = np.zeros(int(t_stop*1/dt))  # Default: no force

        # Simulation results
        self.y = None 

    def set_parameters(self, L1, L2, M1, M2, Mc, G, x_min, x_max, f_min, f_max):
        """Updates the static parameters of the system."""
        self.L1 = L1
        self.L2 = L2
        self.M1 = M1
        self.M2 = M2
        self.Mc = Mc
        self.G = G
        self.x_min = x_min
        self.x_max = x_max 
        self.f_min = f_min
        self.f_max = f_max 
    
    def set_time_parameters(self, t_stop, dt):
        """Updates the time-related parameters of the simulation."""
        self.t_stop = t_stop
        self.dt = dt
        self.t = np.arange(0, t_stop, dt)

    def set_initial_conditions(self, th1, w1, th2, w2, x, vx):
        """Updates the initial conditions of the system."""
        self.th1 = th1
        self.w1 = w1
        self.th2 = th2
        self.w2 = w2
        self.x = x      
        self.vx = vx    

        self.state = np.radians([self.th1, self.w1, self.th2, self.w2])
        self.state = np.append(self.state, [self.x, self.vx])

    def set_control_force(self, control_force):
        """Sets a custom control force F(t)."""
        self.control_force = control_force

    def set_random_control_force(self, f_min, f_max):
        """Sets a stair random control force F(t)."""
        self.f_min = f_min
        self.f_max = f_max
        control_force = np.random.uniform(f_min, f_max,int(self.t_stop))
        control_force = np.repeat(control_force, int(1/self.dt))
        self.control_force = control_force

    def _derivs(self, state, t):
        """Differential equations of the double pendulum on cart."""
        dydx = np.zeros_like(state)
        th1, w1, th2, w2, x, vx = state

        delta = th2 - th1
        cos_delta = np.cos(delta)
        sin_delta = np.sin(delta)
        
        M = self.M1 + self.M2 + self.Mc
        m1L1 = self.M1 * self.L1
        m2L2 = self.M2 * self.L2

        F = self.control_force[int(t*1/self.dt)]

        dydx[0] = w1
        dydx[2] = w2
        dydx[4] = vx

        den1 = M * self.L1 - self.M1 * self.L1 * np.cos(th1)**2 - self.M2 * self.L1 * cos_delta**2
        den2 = self.L2 * den1 / self.L1

        dydx[1] = ((self.M1 * self.L1 * w1**2 * np.sin(th1)
                    + self.M2 * self.L2 * w2**2 * sin_delta * cos_delta
                    + self.M2 * self.G * np.sin(th2) * cos_delta
                    + (F - self.Mc * vx) * np.cos(th1)
                    - M * self.G * np.sin(th1))
                   / den1)

        dydx[3] = ((-self.M2 * self.L2 * w2**2 * sin_delta * cos_delta
                    - (M * self.G * np.sin(th2))
                    + self.L1 * dydx[1] * cos_delta)
                   / den2)

        dydx[5] = (F + m1L1 * (dydx[1] * np.cos(th1) - w1**2 * np.sin(th1))
                   + m2L2 * (dydx[3] * cos_delta - w2**2 * sin_delta)) / M

        return dydx

    def solve(self):
        """Solves the equations of the double pendulum on a cart."""
        y = np.empty((len(self.t), len(self.state)))
        y[0] = self.state
        for i in range(1, len(self.t)):
            y[i] = y[i - 1] + self._derivs(y[i - 1], self.t[i - 1]) * self.dt
            if y[i, 4] < self.x_min:
                y[i, 4] = self.x_min
                y[i, 5] = 0
            elif y[i, 4] > self.x_max:
                y[i, 4] = self.x_max
                y[i, 5] = 0
        self.y = y

    def animate(self):
        """Creates and displays the animation of the double pendulum on cart."""
        if self.y is None:
            raise ValueError("You must solve the system before animating it.")
        
        x_cart = self.y[:, 4]
        x1 = self.L1 * np.sin(self.y[:, 0]) + x_cart
        y1 = -self.L1 * np.cos(self.y[:, 0])
        x2 = self.L2 * np.sin(self.y[:, 2]) + x1
        y2 = -self.L2 * np.cos(self.y[:, 2]) + y1

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        ax1.set(xlim=(-self.L1 - self.L2 + self.x_min - 0.5, self.L1 + self.L2 + self.x_max + 0.5), ylim=(-self.L1 - self.L2 - 0.5, self.L1 + self.L2 + 0.5))
        ax1.set_aspect('equal')
        ax1.grid()

        ax1.set_xlabel('X Position (m)')
        ax1.set_ylabel('Y Position (m)')
        ax1.set_title('Double Pendulum on Cart') 

        cart, = ax1.plot([], [], 's', markersize=15, color='gray')
        line, = ax1.plot([], [], 'o-', lw=2, color='black')
        trace, = ax1.plot([], [], '.-', lw=1, ms=2, color='blue')
        time_text = ax1.text(0.05, 0.9, '', transform=ax1.transAxes)
        ax1.plot([self.x_min, self.x_max], [0, 0], '-', lw=2, color='brown')

        ax2.plot(self.t, self.control_force, lw=2, color='red', label='Control Input')
        ax2.set_xlim(0, self.t_stop)
        ax2.set_ylim(self.f_min, self.f_max)
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Force (N)')
        ax2.set_title('Cart Control Input')
        ax2.grid()
        control_cursor, = ax2.plot([], [], 'o', color='black', label='Current Time')
        ax2.legend()

        def _update(i):
            cart.set_data([x_cart[i]], [0])
            x_i = [x_cart[i], x1[i], x2[i]]
            y_i = [0, y1[i], y2[i]]
            history_x = x2[:i]
            history_y = y2[:i]
            line.set_data(x_i, y_i)
            trace.set_data(history_x, history_y)
            time_text.set_text(f'Time = {i * self.dt:.1f} s')
            control_cursor.set_data(self.t[i], self.control_force[i])
            return cart, line, trace, time_text, control_cursor

        ani = animation.FuncAnimation(fig, _update, frames=len(self.y), interval=self.dt * 1000, blit=True)
        #ani.save("img/double_pendulum_cart.gif", writer=animation.PillowWriter(fps=30))
        plt.subplots_adjust(left=0.05, right=0.99)
        plt.show()

    def save(self, filename):
        """Saves the state evolution of the double pendulum on cart to a CSV file."""
        if self.y is None:
            raise ValueError("You must solve the system before saving data.")

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            writer.writerow(['f (N)', 'th1 (rad)', 'w1 (rad/s)', 'th2 (rad)', 'w2 (rad/s)', 'x (m)', 'vx (m/s)'])
            
            for i in range(len(self.t)):
                writer.writerow(np.append([self.control_force[i]],self.y[i]))

# Matplotlib Helper Functions

### Save Report Widget:
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib_add_ons.save_report_tool import save_report_tool

    def save_report_example_usage():
        # Generating the data
        x = np.linspace(0, 2 * np.pi, 100)  # Create an array of 100 points from 0 to 2*pi
        y = np.sin(x)  # Compute the sine of each value
    
        # Create the figure and axis objects
        fig, ax = plt.subplots()
        list_of_figures = [fig]

        # Add save report tool
        save_report_tool(list_of_figures)
    
        # Plot the sine wave
        ax.plot(x, y)
    
        # Adding labels and title
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_title('A Sine Wave')
    
        # Show the plot
        plt.show()


### Twinx Hover Usage:
    def twinx_hover_example_usage():
        import numpy as np
        from matplotlib import pyplot as plt
        from matplotlib_add_ons.twinx_hover import make_format
    
        # Sample data
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x) * 10
    
        # Create a figure and axis
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
    
        # Plot data on the primary y-axis
        ax1.plot(x, y1, 'b-')
        ax1.set_ylabel('Primary Y-axis', color='b')
        ax1.tick_params('y', colors='b')
    
        # Plot data on the secondary y-axis
        ax2.plot(x, y2, 'r-')
        ax2.set_ylabel('Secondary Y-axis', color='r')
        ax2.tick_params('y', colors='r')
    
        # Set format for coordinate display
        ax2.format_coord = make_format(ax1, ax2)
    
        # Add labels and title
        plt.xlabel('X-axis')
        plt.title('Plot with Twin Axis')
    
        # Show the plot
        plt.show()
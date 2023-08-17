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


if __name__ == '__main__':
    save_report_example_usage()

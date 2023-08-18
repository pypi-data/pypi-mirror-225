from matplotlib import pyplot as plt


def check_stop(event, stop_event, animation_to_stop, figure_to_close):
    """
    Checks if the stop event is set and if so, stops the animation and closes the plot.

    :param event: The event that triggers the function (unused, but required by the callback interface)
    :param stop_event: A threading.Event object, indicating whether the animation should stop or not
    :param animation_to_stop: The animation object that needs to be stopped
    :param figure_to_close: The figure object that needs to be closed
    """
    if stop_event.is_set():
        animation_to_stop.event_source.stop()  # Stops the animation
        plt.close(figure_to_close)  # Closes the figure


def close_plot_when_complete(stop_event, animation_to_stop, figure_to_close):
    """
    Connects a draw event to the check_stop function, which will close the plot when the stop event is set.

    :param stop_event: A threading.Event or multiprocessing.Event object, indicating whether the animation should stop or not
    :param animation_to_stop: The animation object that needs to be stopped
    :param figure_to_close: The figure object that needs to be closed
    """
    plt.connect('draw_event', lambda event: check_stop(event, stop_event, animation_to_stop, figure_to_close))


if __name__ == '__main__':
    pass

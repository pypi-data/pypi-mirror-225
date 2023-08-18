from matplotlib import pyplot as plt


def check_stop(event, stop_event, animation_to_stop, figure_to_close):
    if stop_event.is_set():
        animation_to_stop.event_source.stop()  # Stops the animation
        plt.close(figure_to_close)


def close_plot_when_complete(stop_event, animation_to_stop, figure_to_close):
    plt.connect('draw_event', lambda event: check_stop(event, stop_event, animation_to_stop, figure_to_close))


if __name__ == '__main__':
    pass

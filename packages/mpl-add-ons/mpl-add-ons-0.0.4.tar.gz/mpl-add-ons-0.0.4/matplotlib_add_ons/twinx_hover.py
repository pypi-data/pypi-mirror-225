def make_format(ax, twinx):
    def format_coord(x, y):
        # convert data coordinates to display coordinates
        display_coord = twinx.transData.transform((x, y))
        inv = ax.transData.inverted()
        # convert back to data coordinates with respect to ax
        ax_coord = inv.transform(display_coord)
        coord1_str = f'({ax_coord[0]:.4f}, {ax_coord[1]:.4f})'
        coord2_str = f'({x:.4f}, {y:.4f})'
        return f'Primary: {coord1_str:<40}Secondary: {coord2_str:<}'

    return format_coord

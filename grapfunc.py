def add_vert_lines(plt, period, t_stop, color, linestyle, linewidth):
    t_vert = period
    while (t_vert < t_stop):
        plt.axvline(x = t_vert, color = color, linestyle = linestyle, linewidth = linewidth)
        t_vert += period

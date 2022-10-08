def draw_figure(canvas, figure):
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
            figure_canvas_agg.draw()
            figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
            
            return figure_canvas_agg
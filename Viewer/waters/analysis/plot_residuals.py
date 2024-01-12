from numpy import linspace, array

from PyGraphing import Graph, Icon
from PyGraphing.series import Scatter, Line

from PySVG import Text, Circle, Font, Path, Rect

font700 = Font('Jetbrains Mono', '700')
font500 = Font('Jetbrains Mono', '500')


class Figure(Graph):
    def __init__(self, cals, qcs, w=500, h=500, title=''):
        super().__init__(font700, w=w, h=h)
        self.cals = cals
        self.qcs = qcs

        self.data = [('cal', i[0], i[1]) for i in cals] + [('qc', i[0], i[1]) for i in qcs]
        self.xdict = list({xval[1] for xval in self.data})
        self.xdict.sort()
        self.xdict = {x: i + 1 for i, x in enumerate(self.xdict)}

        self.title.text = title

        self.xlabel.text = 'Conc. (ng/mL)'
        self.xlabel.textColor = (65, 65, 70)
        self.xlabel.textOpacity = 1
        self.xlabel.alignment = (1, 2)

        self.ylabel.text = 'Residual (%)'
        self.ylabel.textColor = (65, 65, 70)
        self.ylabel.textOpacity = 1
        self.ylabel.alignment = (1, 0)

    def text(self):
        text = Text(font500)
        text.anchor = 'start'
        text.baseline = 'central'
        text.size = 10
        text.fill_opacity = 1
        text.fill = (65, 65, 70)

        return text

    def _cal(self):
        color = (55, 222, 177)
        size = 10
        pt = Circle()
        pt.fill = color
        pt.fill_opacity = 0.25
        pt.stroke = color
        pt.stroke_width = 1
        pt.cx, pt.cy, pt.r = '50%', '50%', 0.4375 * size
        icon = Icon(pt, size, size)

        return icon

    def _qc(self):
        color = (177, 222, 55)
        size = 10
        pt = Rect()
        pt.fill = color
        pt.fill_opacity = 0.25
        pt.stroke = color
        pt.stroke_width = 1
        pt.x, pt.y, pt.w, pt.h = 0.1 * size, 0.1 * size, 0.8 * size, 0.8 * size
        icon = Icon(pt, size, size)

        return icon

    def _set_legend(self):
        self.legend.active = False

    def _set_frame(self):
        frame = self.frame
        frame.border.stroke = (65, 65, 70)
        frame.border.stroke_width = 2
        frame.R = False

        self._set_xaxis()
        self._set_yaxis()

    def _set_xaxis(self):
        self.plot.xmin = 0
        self.plot.xmax = len(self.xdict) + 1

        ax = self.frame.x_axis
        for x, i in self.xdict.items():
            ax.addTick(i, f'{x:.1f}')

        ax.text = self.text()
        ax.text.anchor = 'middle'
        ax.dist2text = 7

    def _set_yaxis(self):
        self.plot.ymin = -0.5
        self.plot.ymax = 0.5

        ax = self.frame.y_axis
        for i in linspace(self.plot.ymin, self.plot.ymax, 11):
            ax.addTick(i, f'{100 * i:.1f}%')

        ax.text = self.text()
        ax.text.anchor = 'end'
        ax.dist2text = 7

    def _set_plot(self):
        path = Path(fill_opacity=0, stroke=(55, 85, 125), stroke_width=1, stroke_opacity=1)
        line = Line(plot=self.plot, path=path,
                    x=array([self.plot.xmin, self.plot.xmax]),
                    y=array([0, 0]))
        self.plot.addChild(line)

        def set_limit(val):
            if val < self.plot.ymin:
                return self.plot.ymin
            elif val > self.plot.ymax:
                return self.plot.ymax

            return val

        x, y = zip(*[(self.xdict[i[1]], set_limit(i[2])) for i in self.data if i[0] == 'cal'])
        s = Scatter(plot=self.plot, icon=self._cal(), x=array(x), y=array(y))
        self.plot.addChild(s)

        x, y = zip(*[(self.xdict[i[1]], set_limit(i[2])) for i in self.data if i[0] == 'qc'])
        s = Scatter(plot=self.plot, icon=self._qc(), x=array(x), y=array(y))
        self.plot.addChild(s)

    def set_sizes(self, **kwargs):
        super().set_sizes((0.15, 0.2, 0.85, 0.70))

        self._set_legend()
        self._set_frame()
        self._set_plot()

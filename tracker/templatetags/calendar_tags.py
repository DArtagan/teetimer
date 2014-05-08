from django import template
from calendar import HTMLCalendar, SUNDAY
from datetime import date
from itertools import groupby
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

register = template.Library()

class TeeTimeCalendar(HTMLCalendar):
    def __init__(self, teetimes):
        super(TeeTimeCalendar, self).__init__()
        self.setfirstweekday(SUNDAY)
        self.teetimes = self.group_by_day(teetimes)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if (self.month in self.teetimes) and (day in self.teetimes[self.month]):
                cssclass += ' slots'
                body = []
                body.append('<a href="%s">' % reverse('tracker:day', kwargs={'date': '{year}-{month}-{day}'.format(year=self.year, month=self.month, day=day)}))
                body.append(str(day))
                body.append('</a>')
                return self.day_cell(cssclass, '%s' % (''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(TeeTimeCalendar, self).formatmonth(year, month)

    def group_by_day(self, teetimes):
        day = lambda teetime: teetime.time.day
        month = lambda teetime: teetime.time.month
        return dict([(the_month, dict([(the_day, list(cases)) for the_day, cases in groupby(items, day)])) for the_month, items in groupby(teetimes, month)])


    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


@register.filter()
def teetime_calendar(value, args):
    """
    The template tag's syntax is {% object|teetime_calendar:"year month" %}
    """

    arg_list = [arg.strip() for arg in args.split(' ')]

    return mark_safe(TeeTimeCalendar(value).formatmonth(int(arg_list[0]), int(arg_list[1])))

@register.filter()
def next_month(value, args):
    """
    The template tag's syntax is {% "link words"|next_month:"year month". Year and month refer to the current year and month. %}
    """

    year, month = args.split(' ')

    if month == '12':
        date = "{0}-{1}".format(int(year) + 1, 1)
    else:
        date = "{0}-{1}".format(year, int(month) + 1)
    
    return mark_safe("<a href=\"{0}\">{1}</a>".format(reverse('tracker:month', kwargs={'date': date}), value))

@register.filter()
def prev_month(value, args):
    """
    The template tag's syntax is {% "link words"|prev_month:"year month". Year and month refer to the current year and month. %}
    """

    year, month = args.split(' ')

    if month == '1':
        date = "{0}-{1}".format(int(year) - 1, 12)
    else:
        date = "{0}-{1}".format(year, int(month) - 1)
    
    return mark_safe("<a href=\"{0}\">{1}</a>".format(reverse('tracker:month', kwargs={'date': date}), value))

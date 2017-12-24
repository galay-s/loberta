from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from links.models import Link, Interval
from links.forms import IntervalForm
import requests
import gevent


def get_interval():
    """Get interval(singleton)."""
    return Interval.objects.get(id=1).value


def save_interval(request):
    """Save interval and return form."""
    interval_form = IntervalForm(request.POST)
    if interval_form.is_valid():
        interval_form.save()
    else:
        interval_form = IntervalForm(initial={'value': get_interval()})
    return interval_form


@login_required(login_url='/admin')
def links(request):
    """Show list of links."""
    status_code = None
    links = Link.objects.all()
    data = [(link, status_code) for link in links]
    interval_form = IntervalForm(initial={'value': get_interval()})
    if request.method == 'POST':
        interval_form = save_interval(request)

    return render(
        request,
        'links/index.html',
        {'data': data, 'interval_form': interval_form})


def get_url_status(link):
    """Returns status code one url."""
    if not link.paused:
        try:
            response = requests.get(link.url)
            return response.status_code
        except Exception:
            pass
    return None


@login_required(login_url='/admin')
def get_links_statuses(request):
    """Gets links status."""
    links = Link.objects.all()
    jobs = [gevent.spawn(get_url_status, link) for link in links]
    gevent.joinall(jobs, timeout=20)
    data = [(links[n], job.value) for n, job in enumerate(jobs)]
    return render(request, 'links/links_table.html', {'data': data})


def get_link(link_id):
    """Get link object by id."""
    try:
        link = Link.objects.get(pk=link_id)
    except Link.DoesNotExist:
        link = None
    return link


def change_status_link(link):
    """Сhanges and save paused."""
    link.paused = not link.paused
    link.save()


@login_required(login_url='/admin')
def up_down_link(request, link_id):
    """Сhanges paused field to the opposite status."""
    link = get_link(link_id)
    if link is not None:
        change_status_link(link)
    return links(request)

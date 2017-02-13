import pytest
import os
import re

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
        pytest_html = item.config.pluginmanager.getplugin('html')
        outcome = yield
        report = outcome.get_result()
        extra = getattr(report, 'extra', [])

        if report.when == 'call':
            extra.append(pytest_html.extras.html('<div> Details </div>'))
            xfail = hasattr(report, 'wasxfail')
            if not ((report.skipped and xfail) or (report.failed and not xfail)):
                if "maneuver" in item.funcargs:
                    regex = re.compile('[,\/.!?]')
                    directory = regex.sub('', item.funcargs["maneuver"].title)
                    directory = "testplots/"+directory
                    view_html = ""
                    view_html += "<table>"
                    view_html += "<tr><td class='maneuver_title' colspan=5><div>%s</div></td></tr><tr>" % (item.funcargs["maneuver"].title,)
                    for c in ['speeds.svg', 'accelerations.svg']:
                        view_html += "<td><img class='maneuver_graph' src='%s'/></td>" % (os.path.join(directory, c), )
                    view_html += "</tr><tr>"
                    for c in ['car_in_front.svg', 'pedals.svg']:
                        view_html += "<td><img class='maneuver_graph' src='%s'/></td>" % (os.path.join(directory, c), )
                    view_html += "</tr>"
                    view_html += "</table>"
                    extra.append(pytest_html.extras.html(view_html))
            report.extra = extra

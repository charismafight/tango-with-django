from datetime import datetime


def record_visits(func):
    """
    a decorator of visits
    """

    def visits(*args, **kwargs):
        # record visits to session
        request = args[0]
        visits_count = request.session.get('visits')
        last_visit = request.session.get('last_visit')
        reset_last_visit_time = False
        if visits_count:
            if last_visit:
                last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
                if (datetime.now() - last_visit_time).seconds > 1:
                    visits_count += 1
                    reset_last_visit_time = True
            else:
                visits_count += 1
                reset_last_visit_time = True
        else:
            visits_count = 1
            reset_last_visit_time = True

        request.session['visits'] = visits_count
        if reset_last_visit_time:
            request.session['last_visit'] = str(datetime.now())
        return func(*args, **kwargs)

    return visits

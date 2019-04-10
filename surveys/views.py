from django.shortcuts import render, redirect

from .models import Answer, Election, Thesis


def index(request):
    election = Election.get_current()
    context = {}
    if election and election.first_thesis():
        context = {
            'election': election,
            'first_thesis_id': election.first_thesis().id
        }
    return render(request, 'surveys/index.html', context)


def thesis(request, thesis_id=None):
    if 'stances' not in request.session or not request.session['stances']:
        request.session['stances'] = {}
    try:
        thesis = Thesis.objects.get(id=thesis_id)
        election = Election.get_current()
        if election and thesis.election == election:
            theses = election.all_theses()
            context = {
                'election': election,
                'thesis': thesis,
                'thesis_no': thesis.position(),
                'theses': theses,
                'stances': Answer.STANCE_OPTIONS,
                'my_stances': request.session['stances']
            }
            return render(request, 'surveys/thesis.html', context)
    except Thesis.DoesNotExist:
        pass
    return redirect(index)


def stance(request, thesis_id=None, stance=0):
    election = Election.get_current()
    try:
        this_thesis = Thesis.objects.get(id=thesis_id)
        if election and this_thesis.election == election and stance in [
                int(stance) for stance, _ in Answer.STANCE_OPTIONS
        ]:
            if 'stances' not in request.session or not request.session[
                    'stances']:
                request.session['stances'] = {thesis_id: stance}
            else:
                stances = request.session['stances']
                stances[thesis_id] = stance
                request.session['stances'] = stances

            request.session.modified = True

            next_thesis = this_thesis.next()
            if next_thesis:
                return redirect(thesis, thesis_id=next_thesis.id)
            else:
                return redirect(evaluation)
    except Thesis.DoesNotExist:
        pass
    return redirect(index)


def evaluation(request):
    election = Election.get_current()
    conformance = {}
    parties = []
    stances = []

    if election:
        for party in election.all_parties():
            parties.append(party)
            conformance[party.short_name] = 0

        for thesis in election.all_theses():
            row = [thesis.topic]
            for party in parties:
                field = None
                for answer in party.all_answers():
                    if answer.thesis == thesis:
                        field = answer
                        if 'stances' in request.session and str(
                                answer.thesis.id
                        ) in request.session['stances'] and int(
                                answer.stance) == request.session['stances'][
                                    str(answer.thesis.id)]:
                            conformance[party.short_name] += 1
                            break
                row.append(field)

            if 'stances' in request.session and str(
                    thesis.id) in request.session['stances']:
                row.append(request.session['stances'][str(thesis.id)])
            else:
                row.append(None)
            stances.append(row)

        for party in election.all_parties():
            conformance[
                party.short_name] /= election.all_theses().count() / 100

    context = {
        'conformance': conformance,
        'election': election,
        'parties': parties,
        'stances': stances
    }
    return render(request, 'surveys/result.html', context)

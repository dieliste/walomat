from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .models import Answer, Election


def index(request):
    context = {
        'election_thesis': [],
    }

    for election in Election.active_elections().all():
        if election.nth_thesis(1):
            context['election_thesis'].append(
                (election, election.nth_thesis(1)))

    return render(request, 'surveys/index.html', context)


def thesis_detail(request, slug, thesis_no):
    election = get_object_or_404(Election, slug=slug)
    thesis = election.nth_thesis(thesis_no)

    if 'stances-' + str(election.id) not in request.session:
        request.session['stances-' + str(election.id)] = {}

    if election.is_active() and thesis:
        theses = election.thesis_set.all()

        context = {
            'election': election,
            'thesis': thesis,
            'thesis_no': thesis_no,
            'theses': theses,
            'stances': Answer.STANCE_OPTIONS,
        }

        return render(request, 'surveys/thesis.html', context)
    else:
        raise Http404("No Thesis matches the given query.")


def stance_detail(request, slug, thesis_no, stance_id):
    election = get_object_or_404(Election, slug=slug)
    thesis = election.nth_thesis(thesis_no)

    if 'stances-' + str(election.id) not in request.session:
        request.session['stances-' + str(election.id)] = {}

    if election.is_active() and thesis and stance_id in [
            int(stance) for stance, _ in Answer.STANCE_OPTIONS
    ]:
        request.session['stances-' + str(election.id)][thesis.id] = stance_id
        request.session.modified = True

        thesis_no += 1
        next_thesis = election.nth_thesis(thesis_no)

        if next_thesis:
            return redirect(thesis_detail, slug=slug, thesis_no=thesis_no)
        else:
            return redirect(result_index, slug=slug)
    else:
        raise Http404("No Thesis matches the given query.")

    return redirect(index)


def result_index(request, slug):
    election = get_object_or_404(Election, slug=slug)

    if 'stances-' + str(election.id) not in request.session:
        request.session['stances-' + str(election.id)] = {}

    conformance = {}
    parties = []
    stances = []

    if election:
        for party in election.party_set.all():
            parties.append(party)
            conformance[party.short_name] = 0

        for thesis in election.thesis_set.all():
            row = [thesis.topic]
            for party in parties:
                field = None
                for answer in party.answer_set.all():
                    if answer.thesis == thesis:
                        field = answer
                        if str(answer.thesis.id) in request.session[
                                'stances-' + str(election.id)] and int(
                                    answer.stance) == request.session[
                                        'stances-' + str(election.id)][str(
                                            answer.thesis.id)]:
                            conformance[party.short_name] += 1
                            break
                row.append(field)

            if str(thesis.id) in request.session[
                    'stances-' + str(election.id)]:
                row.append(request.session['stances-' + str(election.id)][str(
                    thesis.id)])
            else:
                row.append(None)
            stances.append(row)

        for party in election.party_set.all():
            conformance[
                party.short_name] /= election.thesis_set.all().count() / 100

    context = {
        'conformance': conformance,
        'election': election,
        'parties': parties,
        'stances': stances
    }

    return render(request, 'surveys/result.html', context)

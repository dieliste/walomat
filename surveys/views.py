from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from csp.decorators import csp_update


from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

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


@csp_update(STYLE_SRC=["'unsafe-inline'", "'self'"])
def result_index(request, slug):
    election = get_object_or_404(Election, slug=slug)

    if 'stances-' + str(election.id) not in request.session:
        request.session['stances-' + str(election.id)] = {}

    conformance = {}
    parties = []
    stances = []

    if election.is_active():
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
    else:
        raise Http404("No Election matches the given query.")


def result_detail(request, slug, thesis_no):
    election = get_object_or_404(Election, slug=slug)
    thesis = election.nth_thesis(thesis_no)

    if 'stances-' + str(
            election.id) not in request.session or not request.session[
                'stances-' + str(election.id)][str(thesis.id)]:
        raise Http404("No Stance matches the given query.")
    else:
        position = request.session['stances-' + str(election.id)][str(
            thesis.id)]

    if election.is_active() and thesis:
        theses = election.thesis_set.all()

        answers = thesis.answer_set.all()
        next_thesis = election.nth_thesis(thesis_no + 1)

        context = {
            'election': election,
            'thesis': thesis,
            'thesis_no': thesis_no,
            'theses': theses,
            'next_thesis': next_thesis,
            'position': position,
            'answers': answers,
        }

        return render(request, 'surveys/result_thesis.html', context)
    else:
        raise Http404("No Thesis matches the given query.")


def theses_pdf(request, slug):
    election = get_object_or_404(Election, slug=slug)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(
        slug)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    offset = 0

    for i, thesis in enumerate(election.thesis_set.all()):
        p.rect(50, 450 - offset, 500, 320, fill=0)
        p.rect(50, 450 - offset, 110, 320, fill=0)
        p.rect(50, 660 - offset, 500, 85, fill=0)
        p.rect(50, 540 - offset, 500, 95, fill=0)

        p.drawString(60, 753 - offset, 'Thema')
        p.drawString(60, 728 - offset, 'These')
        p.drawString(60, 643 - offset, 'Standpunkt')
        p.drawString(60, 618 - offset, 'Begründung [de]')
        p.drawString(60, 523 - offset, 'Begründung [en]')

        p.drawString(170, 753 - offset, thesis.topic)

        textobject = p.beginText()
        textobject.setTextOrigin(170, 728)

        max_line = 62
        if len(thesis.thesis) > max_line:
            thesis_with_lines = ""
            cur_line = 0

            for word in thesis.thesis.split():
                if cur_line + len(word) > max_line:
                    thesis_with_lines += "\n{} ".format(word)
                    cur_line = len(word) + 1
                else:
                    thesis_with_lines += word + " "
                    cur_line += len(word) + 1

            thesis_with_lines = thesis_with_lines.strip()

            for line in thesis_with_lines.splitlines():
                textobject.textLine(text=line)
        else:
            textobject.textLine(thesis.thesis)

        p.drawText(textobject)

        p.circle(180, 647 - offset, 6, fill=0)
        p.drawString(195, 643 - offset, 'stimmen zu')

        p.circle(300, 647 - offset, 6, fill=0)
        p.drawString(315, 643 - offset, 'neutral')

        p.circle(420, 647 - offset, 6, fill=0)
        p.drawString(435, 643 - offset, 'stimmen nicht zu')

        if i % 2 == 1:
            offset = 0
            p.showPage()
        else:
            offset = 350

    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import F

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from paystackapi.transaction import Transaction

from contest.forms import VoteForm, ContestForm, ContestantForm
from contest.models import Contest, Contestant
from contest.paystack_api import PaystackAccount
from contestly import settings


class ContestListView(ListView):
    model = Contest
    template_name = 'poll/the_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'contests'
    # paginate_by = 10


class ContestDetail(DetailView):
    model = Contest
    template_name = 'contest/contest_detail.html'


class ContestantDetail(DetailView, FormMixin):
    model = Contestant
    context_object_name = 'contestants'
    template_name = 'contest/contestant_detail.html'
    form_class = VoteForm

    def get_success_url(self):
        return reverse('contest:contestant-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super(ContestantDetail, self).get_context_data(*args, **kwargs)
        context['vote_contestant'] = Contestant.objects.get(pk=self.kwargs.get('pk'))
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, *args, **kwargs):
        contestant = Contestant.objects.get(pk=self.kwargs['pk'])
        contestant.votes = F('votes') + 1
        contestant.save()

        messages.success(self.request, f'You have successfully voted for {contestant.name}.')
        return super().form_valid(form)


def contestant_free_vote(request, pk):
    contestant = Contestant.objects.get(pk=pk)
    contestant.votes = F('votes') + 1
    contestant.save()
    messages.success(request, f'Thank you! You have successfully voted for {contestant.name}.')
    return redirect('contest:contestant-detail', pk=pk)


def contestant_detail_display(request, pk):
    contestant = Contestant.objects.get(pk=pk)
    contest = contestant.contest
    if request.method == 'GET':
        vote = request.GET['votes']

        print(vote, '<<<<<<<>>>>>>>')

    print(vote, '<<<<<<<>>>>>>>')
    return redirect('/contest/contestant_detail_vote_payment.html/?votes=' + vote)


def payment_page(request):
    ctx = {
        'name': request.GET.get('name'),
        'address': request.GET.get('address')
    }
    return render(request, 'contribute/_membership-thank-you.html', ctx)


def contestant_detail_view(request, pk):
    contestant = Contestant.objects.get(pk=pk)
    contest = contestant.contest

    context = {}

    if request.method == 'POST':
        vote = request.POST['votes']
        total_vote = int(vote) * contest.vote_cost

        paystack = PaystackAccount(
            settings.PAYSTACK_EMAIL,
            settings.PAYSTACK_PUBLIC_KEY,
            total_vote
        )
        context['paystack'] = paystack
        if paystack.verify_transaction(request.POST['reference']):
            messages.success(request, "paystack payment successfull")
            form = VoteForm(request.POST)
            if form.is_valid():
                con = Contestant.objects.get(pk=pk)
                vote = form.cleaned_data['votes']
                print(vote)
                con.votes = F('votes') + vote
                con.save()

    else:
        form = VoteForm()
    context['contestants'] = get_object_or_404(Contestant, pk=pk)
    context['vote_contestant'] = contestant
    context['form'] = form
    context['pk_public'] = settings.PAYSTACK_PUBLIC_KEY
    context['currency'] = 'NGN'

    return render(request, 'contest/contestant_detail.html', context)


# After successful payment Contestant.votes is incremented by amount of votes


def paid_vote_view(request, pk):
    context = {}
    contestant = Contestant.objects.get(pk=pk)
    contest = contestant.contest
    vote = request.GET.get('votes')

    vote = int(vote)
    vote_cost = int(contest.vote_cost)
    total_cost = vote * vote_cost

    context['vote'] = vote
    context['contestants'] = get_object_or_404(Contestant, pk=pk)
    context['vote_contestant'] = contestant

    paystack = PaystackAccount(
        settings.PAYSTACK_EMAIL,
        settings.PAYSTACK_PUBLIC_KEY,
        total_cost
    )

    context = {'object': object, 'pk_public': settings.PAYSTACK_PUBLIC_KEY,
               'currency': 'NGN',
               'paystack': paystack,
               'vote': vote,
               'contestants': contestant,
               'total_cost': total_cost
               }

    # FOR PAYSTACK TRANSACTION COMPLETED
    if request.method == 'POST':
        if paystack.verify_transaction(request.POST['reference']):
            messages.success(request, "paystack payment successfull")
            vote_count = vote
            contestant.votes = F('votes') + vote_count
            contestant.save()
            messages.success(request, f"You have successfully casted {vote} vote for {contestant.name}")

    return render(request, 'contest/contestant_detail_vote_payment.html', context=context)


class ResultsView(DetailView):
    model = Contest
    template_name = 'contest/result.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ResultsView, self).get_context_data(*args, **kwargs)
        # context['contestant_list'] = Contestant.objects.get(contest__contest=contestant.contest)

        # context['contestant_list'] = Contestant.objects.filter(contest=self.kwargs.get('pk'))
        return context


class ContestCreateViewTest(CreateView):
    model = Contest
    form_class = ContestForm
    template_name = 'contest/contest_form_test.html'


class ContestCreateView(CreateView):
    model = Contest
    form_class = ContestForm
    # fields = ['name', 'photo', 'post', 'cash_vote', 'vote_cost', 'start_date', 'end_date']


def category_view(request, cats):
    contest_category = Contest.objects.filter(category=cats)
    return render(request, 'contest_category.html', {'cats': cats, 'contest_category': contest_category})


class ContestUpdateView(UpdateView):
    model = Contest
    fields = ['name', 'photo', 'post', 'cash_vote', 'vote_cost', 'start_date', 'end_date']


class ContestantCreateView(CreateView):
    model = Contestant
    # form_class = ContestantForm
    fields = ['name', 'title', 'brief_post', 'post', 'photo']

    def form_valid(self, form):
        form.instance.contest_id = self.kwargs.get('pk')
        return super().form_valid(form)


class ContestantUpdateView(UpdateView):
    model = Contestant
    fields = ['name', 'title', 'post', 'photo']

    def form_valid(self, form):
        form.instance.contest = self.kwargs.get('pk')
        return super().form_valid(form)


def verify(request, id):
    transaction = Transaction(authorization_key=settings.PAYSTACK_SCRET_KEY)
    response = transaction.verify(id)
    data = JsonResponse(response, safe=False)
    return data

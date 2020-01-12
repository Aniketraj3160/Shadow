from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from users.models import *
from django.utils import timezone
from datetime import datetime as dt
from datetime import date

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment, registerCamera, City, State
from .forms import *
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import jsonpickle

from django.utils.safestring import mark_safe
import csv
from .csvConverter import indiaCsv
from django.db.models import Count
from django.utils.timezone import datetime


AUTHORITYTYPES_CHOICES = (('Department of Consumer Affairs', 'Department of Consumer Affairs'), ('Department of Food and Public Distribution', 'Department of Food and Public Distribution'), ('Serious Fraud Investigation Office', 'Serious Fraud Investigation Office'), ('Forest Reserve Conservation Authority', 'Forest Reserve Conservation Authority'),
                          ('Criminal Investigation Department', 'Criminal Investigation Department'), ('Labour Bureau', 'Labour Bureau'), ('National Commission for Minorities', 'National Commission for Minorities'), ('National Commission for Women', 'National Commission for Women'), ('Income Tax Department', 'Income Tax Department'))


class StateObject:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, state, crimes):
        self.state = state
        self.crimereported = crimes


class deptObject:
    def __init__(self, month, dept1, dept2, dept3, dept4, dept5, dept6, dept7, dept8):
        self.month = month
        self.dept1 = dept1
        self.dept2 = dept2
        self.dept3 = dept3
        self.dept4 = dept4
        self.dept5 = dept5
        self.dept6 = dept6
        self.dept7 = dept7
        self.dept8 = dept8


def linkgraph(request):
    context = {}
    return render(request, 'blog/linktographs.html', context)


def indianmap(request):
    stateslist = {"Andaman & Nicobar Island": "ANI", "Andhra Pradesh": "AP", "Arunachal Pradesh": "AR", "Assam": "AS", "Bihar": "BR", "Chhattisgarh": "CT", "Puducherry": "PD", "Punjab": "PB", "Rajasthan": "RJ", "Sikkim": "SK", "Tamil Nadu": "TN", "Chandigarh": "CH", "Telangana": "TL", "Tripura": "TR", "West Bengal": "WB", "Odisha": "OR", "Dadara & Nagar Havelli": "DNH",
                  "Daman & Diu": "DD", "Goa": "GA", "Gujarat": "GJ", "Haryana": "HR", "Himachal Pradesh": "HP", "Jammu & Kashmir": "JK", "Jharkhand": "JH", "Karnataka": "KA", "Kerala": "KL", "Lakshwadweep": "L", "Madhya Pradesh": "MP", "Maharashtra": "MH", "Manipur": "MN", "Mizoram": "MZ", "Meghalaya": "ML", "Nagaland": "NL", "NCT of Delhi": "NCT", "Uttar Pradesh": "UP", "Uttarakhand": "UT"}
    data = []
    st, cr = [], []
    states = State.objects.all()
    for state in states:
        code = stateslist[state.name]
        obj = StateObject(code, 0)
        data.append(obj)
    PostState = Post.objects.all()
    for post in PostState:
        poststate = post.state.name
        for x in range(0, len(data)):
            if stateslist[poststate] == data[x].state:
                data[x].crimereported += 1
                break
    for x in data:
        st.append(x.state)
        cr.append(x.crimereported)

    context = {'state': mark_safe(json.dumps(st)),
               'crime': mark_safe(json.dumps(cr))}
    return render(request, 'blog/D3india.html', context)


def linegraph(request):
    form1 = SortLocation()
    mydata = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
              "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
    DeptList = []
    a1, a2, a3, a4, a5, a6, a7, a8, a9 = [], [], [], [], [], [], [], [], []
    for x in range(0, 12):
        dept = deptObject(x+1, 0, 0, 0, 0, 0, 0, 0, 0)
        DeptList.append(dept)
    print(DeptList)

    if request.method == 'POST':
        form1 = SortLocation(request.POST)
        if form1.is_valid():
            state = form1.cleaned_data['state']
            city = form1.cleaned_data['city']
            PostList = Post.objects.filter(state=state, city=city)

            for post in PostList:
                month = post.date_posted.strftime('%B')
                for x in range(0, len(DeptList)):
                    if mydata[month] == DeptList[x].month:
                        break
                authority = post.authority
                authority = authority.split(",")
                date1 = post.date_posted.strftime("%m/%d/%Y")
                date2 = dt.now().strftime("%m/%d/%Y")
                date1 = date1.split("/")
                date2 = date2.split("/")
                d0 = date(int(date1[2]), int(date1[0]), int(date1[1]))
                d1 = date(int(date2[2]), int(date2[0]), int(date2[1]))
                delta = d1 - d0
                if delta.days < 365:
                    for auth in authority:
                        if auth == 'Department of Consumer Affairs':
                            DeptList[x].dept1 += 1
                        elif auth == 'Department of Food and Public Distribution':
                            DeptList[x].dept2 += 1
                        elif auth == 'Serious Fraud Investigation Office':
                            DeptList[x].dept3 += 1
                        elif auth == 'Forest Reserve Conservation Authority':
                            DeptList[x].dept4 += 1
                        elif auth == 'Criminal Investigation Department':
                            DeptList[x].dept5 += 1
                        elif auth == 'Labour Bureau':
                            DeptList[x].dept6 += 1
                        elif auth == 'National Commission for Minorities':
                            DeptList[x].dept7 += 1
                        elif auth == 'National Commission for Women':
                            DeptList[x].dept8 += 1
            for x in DeptList:
                a1.append(x.month)
                a2.append(x.dept1)
                a3.append(x.dept2)
                a4.append(x.dept3)
                a5.append(x.dept4)
                a6.append(x.dept5)
                a7.append(x.dept6)
                a8.append(x.dept7)
                a9.append(x.dept8)
            context = {'form': form1, 'month': mark_safe(json.dumps(a1)), 'dept1': mark_safe(json.dumps(a2)), 'dept2': mark_safe(json.dumps(a3)), 'dept3': mark_safe(json.dumps(a4)), 'dept4': mark_safe(
                json.dumps(a5)), 'dept5': mark_safe(json.dumps(a6)), 'dept6': mark_safe(json.dumps(a7)), 'dept7': mark_safe(json.dumps(a8)), 'dept8': mark_safe(json.dumps(a9))}
            return render(request, 'blog/linegraph.html', context)

    PostList = Post.objects.all()
    for post in PostList:
        month = post.date_posted.strftime('%B')
        for x in range(0, len(DeptList)):
            if mydata[month] == DeptList[x].month:
                break
        authority = post.authority
        authority = authority.split(",")
        date1 = post.date_posted.strftime("%m/%d/%Y")
        date2 = dt.now().strftime("%m/%d/%Y")
        date1 = date1.split("/")
        date2 = date2.split("/")
        d0 = date(int(date1[2]), int(date1[0]), int(date1[1]))
        d1 = date(int(date2[2]), int(date2[0]), int(date2[1]))
        delta = d1 - d0
        if delta.days < 365:
            for auth in authority:
                if auth == 'Department of Consumer Affairs':
                    DeptList[x].dept1 += 1
                elif auth == 'Department of Food and Public Distribution':
                    DeptList[x].dept2 += 1
                elif auth == 'Serious Fraud Investigation Office':
                    DeptList[x].dept3 += 1
                elif auth == 'Forest Reserve Conservation Authority':
                    DeptList[x].dept4 += 1
                elif auth == 'Criminal Investigation Department':
                    DeptList[x].dept5 += 1
                elif auth == 'Labour Bureau':
                    DeptList[x].dept6 += 1
                elif auth == 'National Commission for Minorities':
                    DeptList[x].dept7 += 1
                elif auth == 'National Commission for Women':
                    DeptList[x].dept8 += 1

    for x in DeptList:
        a1.append(x.month)
        a2.append(x.dept1)
        a3.append(x.dept2)
        a4.append(x.dept3)
        a5.append(x.dept4)
        a6.append(x.dept5)
        a7.append(x.dept6)
        a8.append(x.dept7)
        a9.append(x.dept8)

    context = {'form': form1, 'month': mark_safe(json.dumps(a1)), 'dept1': mark_safe(json.dumps(a2)), 'dept2': mark_safe(json.dumps(a3)), 'dept3': mark_safe(json.dumps(a4)), 'dept4': mark_safe(
        json.dumps(a5)), 'dept5': mark_safe(json.dumps(a6)), 'dept6': mark_safe(json.dumps(a7)), 'dept7': mark_safe(json.dumps(a8)), 'dept8': mark_safe(json.dumps(a9))}
    return render(request, 'blog/linegraph.html', context)


def piechart(request):
    months = {'January':0,'February':1,'March':2,'April':3,'May':4,'June':5,'July':6,'August':7,'September':8,'October':9,'November':10,'December':11}
    authorities = {'Department of Consumer Affairs':0,'Department of Food and Public Distribution':1,'Serious Fraud Investigation Office':2,'Forest Reserve Conservation Authority':3,'Criminal Investigation Department':4,'Labour Bureau':5,'National Commission for Minorities':6,'National Commission for Women':7}
    piedata = [[],[],[],[],[],[],[],[]]
    for pie in piedata:
        for x in range(0,12):
            pie.append(0)
    for pie in piedata:
        print(pie)
    PostList = Post.objects.all()
    for post in PostList:
        date1 = post.date_posted.strftime("%m/%d/%Y")
        date2 = dt.now().strftime("%m/%d/%Y")
        date1 = date1.split("/")
        date2 = date2.split("/")
        d0 = date(int(date1[2]), int(date1[0]), int(date1[1]))
        d1 = date(int(date2[2]), int(date2[0]), int(date2[1]))
        delta = d1 - d0
        if delta.days < 365:
            authority = post.authority
            month = post.date_posted.strftime('%B')
            authority = authority.split(",")
            try:
                authority.remove('Income Tax Department')
            except:
                pass
            for auth in authority:
                piedata[authorities[auth]][months[month]]+=1
    print()
    for pie in piedata:
        print(pie)
    context={'piedata':mark_safe(json.dumps(piedata))}
    return render(request, 'blog/pie.html', context)



def donut(request):
    return render(request, 'blog/donut.html', {})


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def landing_page(request):
    return render(request, 'blog/index.html')


class PostDetailView(DetailView):
    model = Post
    
    # is_liked = False

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     post = context['post']
    #     if post.likes.filter(id=self.request.user.id).exists():
    #         context['is_liked'] = True
    #     return context

######################################################################################################################################################
    #EDIT STARTS#
######################################################################################################################################################


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = BlogForm
    # fields = ['title', 'location', 'pincode', 'country', 'city',
    #           'state',  'content', 'crimetype', 'photo1', 'photo2', 'photo3', 'photo4']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.tags = form.instance.state.name+"," + \
            form.instance.city.name+","+form.instance.crimetype1
        if form.instance.crimetype2 == "None":
            form.instance.crimetype2 = None
        else:
            form.instance.tags = form.instance.tags+","+form.instance.crimetype2
        if form.instance.crimetype3 == "None":
            form.instance.crimetype3 = None
        else:
            form.instance.tags = form.instance.tags+","+form.instance.crimetype3
        if form.instance.crimetype4 == "None":
            form.instance.crimetype4 = None
        else:
            form.instance.tags = form.instance.tags+","+form.instance.crimetype4
        crimetype = [form.instance.crimetype1, form.instance.crimetype2,
                     form.instance.crimetype3, form.instance.crimetype4]

        print(crimetype)
        form.instance.authority = find_authority(crimetype)
        return super().form_valid(form)


def find_authority(crimetype):
    authority = []
    ATH = ''
    for crime in crimetype:
        if crime:
            auth = crime_to_authority(crime)
            for au in auth:
                if au not in authority:
                    authority.append(au)
    ATH = authority[0]
    authority = authority[1:]
    for auth in authority:
        ATH = ATH+","+auth
    return ATH


def crime_to_authority(crime):
    if crime == 'White-Collar Crime':
        return ['Department of Consumer Affairs', 'Serious Fraud Investigation Office', 'Income Tax Department', 'Criminal Investigation Department']
    elif crime == 'Robbery':
        return ['Criminal Investigation Department']
    elif crime == 'Rape':
        return ['Criminal Investigation Department', 'National Commission for Women']
    elif crime == 'Assualt':
        return ['Criminal Investigation Department']
    elif crime == 'Arson':
        return ['Criminal Investigation Department']
    elif crime == 'Homicide':
        return ['Criminal Investigation Department']
    elif crime == 'Crimes Against Morality':
        return ['Criminal Investigation Department', 'National Commission for Women']
    elif crime == 'Illegal goods':
        return ['Criminal Investigation Department', 'Department of Consumer Affairs', 'Department of Food and Public Distribution', 'Serious Fraud Investigation Office', 'Income Tax Department']
    elif crime == 'Poaching and Illegal Felling':
        return ['Forest Reserve Conservation Authority']
    elif crime == 'Adultery in Food Sector':
        return ['Department of Food and Public Distribution', 'Department of Consumer Affairs']
    elif crime == 'Ill-treatment of Workers':
        return ['Labour Bureau', 'National Commission for Minorities']
    elif crime == 'Tax Evasion':
        return ['Income Tax Department']
    elif crime == 'Sexual Harrassment':
        return ['National Commission for Women', 'Criminal Investigation Department']
    elif crime == 'Communal Crimes':
        return ['National Commission for Minorities', 'Criminal Investigation Department']


@login_required
def PostListView(request):
    form1 = SortLocation()
    form2 = SortCrimeType()
    print("Kiran")
    pList = []
    PostList = Post.objects.all().order_by('-date_posted')
    if request.method == 'POST':
        print("Boy")
        try:
            form1 = SortLocation(request.POST)
        except:
            form1 = 0
        form2 = SortCrimeType(request.POST)
        if (form1.is_valid() and form2.is_valid()) or form2.is_valid():
            try:
                state = form1.cleaned_data['state']
                city = form1.cleaned_data['city']
                
            except:
                state = 0
                city = 0
            crimetype = form2.cleaned_data['crimetype']
            for post in PostList:
                tags = post.tags
                tags = tags.split(",")
                if crimetype != "All":
                    if state != 0 and city != 0:
                        if state.name in tags and city.name in tags and crimetype in tags:
                            pList.append(post)
                    else:
                        if crimetype in tags:
                            pList.append(post)
                else:
                    if state != 0 and city != 0:
                        if state.name in tags and city.name in tags:
                            pList.append(post)
                    else:
                        pList.append(post)
            context = {
                'form1': form1,
                'form2': form2,
                'posts': pList
            }
            return render(request, 'blog/home.html', context)
    context = {
        'form1': form1,
        'form2': form2,
        'posts': PostList
    }
    return render(request, 'blog/home.html', context)


# def PostListView(request):
#     PostList = Post.objects.all().order_by('-date_posted')

#     if request.method=='POST':
#         state=reque


@login_required
def PostListView_Auth(request,check):
    if check==1:
        PostList = []
        try:
            authority = Authority.objects.get(user=request.user)
        except:
           authority = 0
        if authority == 0:
            return redirect('invalid_page')
        else:
            authority = Authority.objects.get(user=request.user)
            Bloglist_complete = Post.objects.all()
            for post in Bloglist_complete:
                authList = post.authority
                authList = authList.split(',')
                if authority.Dept_name in authList:
                    PostList.append(post)
            form1 = SortLocation()
            form2 = SortCrimeType()
            pList = []
            if request.method=='POST':
                try:
                    form1=SortLocation(request.POST)
                except:
                    form1=0
                form2=SortCrimeType(request.POST)
                if (form1.is_valid() and form2.is_valid()) or form2.is_valid():
                    try:
                        state = form1.cleaned_data['state']
                        city = form1.cleaned_data['city']
                    except:
                        state=0
                        city=0
                    crimetype = form2.cleaned_data['crimetype']
                    for post in PostList:
                        tags = post.tags
                        tags=tags.split(",")
                        if crimetype!="All":
                            if state!=0 and city!=0:
                                if state.name in tags and city.name in tags and crimetype in tags:
                                    pList.append(post)
                            else:
                                if crimetype in tags:
                                    pList.append(post)
                        else:
                            if state!=0 and city!=0:
                                if state.name in tags and city.name in tags:
                                    pList.append(post)
                            else:
                                pList.append(post)
                    context = {
                        'form1':form1,
                        'form2':form2,
                        'posts':pList
                    }
            context = {
                'form1':form1,
                'form2':form2,
                'posts':PostList
            } 
            return render(request, 'blog/home.html', context)                    
    else:
        return redirect('invalid_page')





# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/home.html'
#     context_object_name = 'posts'
#     ordering = ['-date_posted']


######################################################################################################################################################
    #EDIT STOPS#
######################################################################################################################################################


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'location', 'pincode', 'city',
              'state', 'country', 'content', 'crimetype', 'photo1', 'photo2', 'photo3', 'photo4']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/home'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def RegisterCamera(request):
    # cam = get_object_or_404(registerCamera)
    # if request.method == "POST":
        # form = CameraForm(request.POST)
        #     if form.is_valid():
        #         camera = form.save(commit=False)
        #         camera.cam = cam
        #         camera.author = request.user
        #         camera.save()
        #         return redirect('blog-home')
        # else:
        #     form = CameraForm()
        # return render(request, 'blog/registerCamera.html', {'form': form})
    form = CameraForm(request.POST)
    if form.is_valid():
        form.save()
    context = {
        'form': CameraForm,
    }
    return render(request, 'blog/registerCamera.html', context)


def usertype(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    user = comment.author
    flag = []
    try:
        querry = Authority.objects.get(user=user)
    except:
        flag += [1]

    try:
        querry = Journalist.objects.get(user=user)
    except:
        flag += [2]

    try:
        querry = Anonymous.objects.get(user=user)
    except:
        flag += [3]


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def post_approve(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    flag5 = []
    try:
        querry5 = Authority.objects.get(user=user)
    except:
        flag5 += [1]

    try:
        querry5 = Journalist.objects.get(user=user)
    except:
        flag5 += [2]

    try:
        querry5 = Anonymous.objects.get(user=user)
    except:
        flag5 += [3]

    if 1 in flag5:
        print(flag5)

    else:
        print(flag5)
        post.approve()
    return redirect('post-detail', pk=post.pk)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post-detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user:
        comment.delete()
        return redirect('post-detail', pk=comment.post.pk)


is_upvoted = False
is_downvoted = False


@login_required
def upvote_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    user = request.user
    postuser = post.author
    flag0 = []
    try:
        querry1 = Authority.objects.get(user=user)
    except:
        flag0 += [1]

    try:
        querry1 = Journalist.objects.get(user=user)
    except:
        flag0 += [2]

    try:
        querry1 = Anonymous.objects.get(user=user)
    except:
        flag0 += [3]

    flag1 = []
    try:
        querry2 = Authority.objects.get(user=postuser)
    except:
        flag1 += [1]

    try:
        querry2 = Journalist.objects.get(user=postuser)
    except:
        flag1 += [2]

    try:
        querry2 = Anonymous.objects.get(user=postuser)
    except:
        flag1 += [3]

    print(postuser)
    print(flag1)
    if post.upvotes.filter(id=request.user.id).exists():
        post.upvotes.remove(request.user)
        if 1 not in flag0:
            if 3 not in flag1:
                print(flag1)
                print(querry2.credits)
                querry2.credits = querry2.credits-5
                print(querry2.credits)
                querry2.save()
        elif 2 not in flag0:
            if 3 not in flag1:
                print(flag1)
                print(querry2.credits)
                querry2.credits = querry2.credits-2
                print(querry2.credits)
                querry2.save()
        is_upvoted = False
    else:
        post.upvotes.add(request.user)
        if post.downvotes.filter(id=request.user.id).exists():
            if 1 not in flag0:
                if 3 not in flag1:
                    print(querry2.credits)
                    querry2.credits = querry2.credits+10
                    print(querry2.credits)
                    querry2.save()

            if 2 not in flag0:
                if 3 not in flag1:
                    print(querry2.credits)
                    querry2.credits = querry2.credits+4
                    print(querry2.credits)
                    querry2.save()
        else:
            if 1 not in flag0:
                if 3 not in flag1:
                    print(querry2.credits)
                    querry2.credits = querry2.credits+5
                    print(querry2.credits)
                    querry2.save()

            if 2 not in flag0:
                if 3 not in flag1:
                    print(querry2.credits)
                    querry2.credits = querry2.credits+2
                    print(querry2.credits)
                    querry2.save()
        post.downvotes.remove(request.user)
        is_downvoted = False
        is_upvoted = True

    context = {
        'post': post,
        'is_upvoted': is_upvoted,
        'total_upvotes': post.total_upvotes(),
        'credits': querry2.credits,
    }
    if request.is_ajax():
        html = render_to_string(
            'blog/upvotepost_section.html', context, request=request)
        return JsonResponse({'form': html})
    return redirect(post.get_absolute_url())


@login_required
def downvote_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    user = request.user
    postuser = post.author
    flag3 = []
    try:
        querry3 = Authority.objects.get(user=user)
    except:
        flag3 += [1]

    try:
        querry3 = Journalist.objects.get(user=user)
    except:
        flag3 += [2]

    try:
        querry3 = Anonymous.objects.get(user=user)
    except:
        flag3 += [3]

    flag4 = []
    try:
        querry4 = Authority.objects.get(user=postuser)
    except:
        flag4 += [1]

    try:
        querry4 = Journalist.objects.get(user=postuser)
    except:
        flag4 += [2]
    try:
        querry4 = Anonymous.objects.get(user=postuser)
    except:
        flag4 += [3]

    # is_downvoted = False
    print(flag3)
    print(flag4)
    print(user)
    print(postuser)
    if post.downvotes.filter(id=request.user.id).exists():
        post.downvotes.remove(request.user)
        if 1 not in flag3:
            if 3 not in flag4:
                print(flag4)
                print(querry4.credits)
                querry4.credits = querry4.credits+5
                print(querry4.credits)
                querry4.save()
        if 2 not in flag3:
            if 3 not in flag4:
                print(flag4)
                print(querry4.credits)
                querry4.credits = querry4.credits+2
                print(querry4.credits)
                querry4.save()
        is_downvoted = False

    else:
        post.downvotes.add(request.user)
        if post.upvotes.filter(id=request.user.id).exists():
            if 1 not in flag3:
                if 3 not in flag4:
                    print(flag4)
                    print(querry4.credits)
                    querry4.credits = querry4.credits-10
                    print(querry4.credits)
                    querry4.save()
        else:
            if 1 not in flag3:
                if 3 not in flag4:
                    print(flag4)
                    print(querry4.credits)
                    querry4.credits = querry4.credits-5
                    print(querry4.credits)
                    querry4.save()
        if post.upvotes.filter(id=request.user.id).exists():
            if 2 not in flag3:
                if 3 not in flag4:
                    print(flag4)
                    print(querry4.credits)
                    querry4.credits = querry4.credits-4
                    print(querry4.credits)
                    querry4.save()
        else:
            if 2 not in flag3:
                if 3 not in flag4:
                    print(flag4)
                    print(querry4.credits)
                    querry4.credits = querry4.credits-2
                    print(querry4.credits)
                    querry4.save()
        post.upvotes.remove(request.user)
        is_upvoted = False
        is_downvoted = True

    context = {
        'post': post,
        'is_downvoted': is_downvoted,
        'total_downvotes': post.total_downvotes(),
    }
    if request.is_ajax():
        html = render_to_string(
            'blog/downvotepost_section.html', context, request=request)
        return JsonResponse({'form': html})
    return redirect(post.get_absolute_url())


def cameraslist(request):
    context = {
        'cameras': registerCamera.objects.all()
    }
    return render(request, 'blog/cameralist.html', context)


def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'blog/city_dropdown_list_options.html', {'cities': cities})


# Create your views here.

class post_rest(APIView):

    def get(self, request):

        data = Post.objects.all()
        list1 = []
        for each in data:
            var = {
                'title': each.title,
                'location': each.location,
                'content': each.content,
                'crimetype': each.crimetype,
                'state': each.state,
                'city': each.city
            }
            list1.append(var)
        return Response(list1)


######################################################################################################################################################
        #EDIT STARTS#
######################################################################################################################################################


def load_cities(request):
    state_id = request.GET.get('state')
    print(state_id)
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'blog/city_dropdown_list_options.html', {'cities': cities})


def invalid(request):
    context = {}
    return render(request, 'blog/invalid.html', context)


@login_required
def authority_specific(request):
    Postlist = []
    authority = Authority.objects.filter(user=request.user)
    if authority == []:
        return redirect('invalid_page')
    else:
        authority = authority.objects.get(user=request.user)
        Bloglist_complete = Post.objects.all()
        for post in Bloglist_complete:
            authList = post.authority
            authList = authList.split(',')
            if authority.Dept_name in authList:
                Postlist.append(post)
        return render(request, 'blog/home.html', {'AuthoritySpecificList': Bloglist_complete, 'posts': Postlist})


######################################################################################################################################################
        #EDIT STOPS#
######################################################################################################################################################
def post_ordered_by_upvotes(request):
    today = datetime.today()
    context = {'post':Post.objects.filter(date_posted__year=today.year,date_posted__month=today.month,date_posted__day=today.day).annotate(upvote_count=Count('upvotes')).order_by('-upvote_count')[:20]}
    return render(request,'blog/trendingPosts.html',context)

def post_ordered_by_upvotes_monthly(request):
    today = datetime.today()
    context = {'post':Post.objects.filter(date_posted__year=today.year,date_posted__month=today.month).annotate(upvote_count=Count('upvotes')).order_by('-upvote_count')[:20]}
    return render(request,'blog/trendingMonthlyPosts.html',context)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from .models import StudyGroup, Membership, Topic, Course
from .forms import StudyGroupForm

def group_list(request):
    qs = StudyGroup.objects.all().annotate(
        members_count=Count('memberships', filter=Q(memberships__status='APPROVED'))
    ).order_by('-members_count', '-created_at')

    search = request.GET.get('q', '').strip()
    topic_name = request.GET.get('topic', '').strip()
    course_code = request.GET.get('course', '').strip()

    if search:
        qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(room__icontains=search))

    if topic_name:
        qs = qs.filter(topics__name__iexact=topic_name)

    if course_code:
        qs = qs.filter(course__code__iexact=course_code)

    topics = Topic.objects.order_by('name')[:50]
    courses = Course.objects.order_by('code')[:100]

    return render(request, 'groups/group_list.html', {
        'groups': qs,
        'topics': topics,
        'courses': courses,
        'search': search,
        'selected_topic': topic_name,
        'selected_course': course_code,
    })

@login_required
def group_create(request):
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            group = form.save(created_by=request.user)
            # create owner membership
            Membership.objects.create(user=request.user, group=group, role=Membership.OWNER, status=Membership.APPROVED)
            messages.success(request, 'Study group created!')
            return redirect('groups:detail', pk=group.pk)
    else:
        form = StudyGroupForm()
    return render(request, 'groups/group_form.html', {'form': form})

def group_detail(request, pk):
    group = get_object_or_404(StudyGroup, pk=pk)
    approved_members = Membership.objects.filter(group=group, status=Membership.APPROVED).select_related('user')
    is_owner = request.user.is_authenticated and approved_members.filter(user=request.user, role=Membership.OWNER).exists()
    existing = None
    if request.user.is_authenticated:
        existing = Membership.objects.filter(group=group, user=request.user).first()
    return render(request, 'groups/group_detail.html', {
        'group': group,
        'approved_members': approved_members,
        'existing_membership': existing,
        'is_owner': is_owner,
    })

@login_required
def group_request_join(request, pk):
    group = get_object_or_404(StudyGroup, pk=pk)
    membership, created = Membership.objects.get_or_create(user=request.user, group=group, defaults={'status': Membership.PENDING})
    if not created:
        messages.info(request, f'Your status is already {membership.status}.')
    else:
        messages.success(request, 'Join request sent to the group owner.')
    return redirect('groups:detail', pk=pk)

@login_required
def join_requests_list(request):
    # Pending requests for groups the user owns
    owning = Membership.objects.filter(user=request.user, role=Membership.OWNER, status=Membership.APPROVED).values_list('group_id', flat=True)
    pendings = Membership.objects.filter(group_id__in=owning, status=Membership.PENDING).select_related('group', 'user')
    return render(request, 'groups/join_requests.html', {'pending_memberships': pendings})

@login_required
def approve_request(request, membership_id):
    m = get_object_or_404(Membership, id=membership_id)
    # ensure requester is owner
    owner = Membership.objects.filter(group=m.group, user=request.user, role=Membership.OWNER, status=Membership.APPROVED).exists()
    if not owner:
        messages.error(request, 'You are not allowed to approve this request.')
        return redirect('groups:requests')
    m.status = Membership.APPROVED
    m.save()
    messages.success(request, f'Approved {m.user.username} for {m.group.title}.')
    return redirect('groups:requests')

@login_required
def reject_request(request, membership_id):
    m = get_object_or_404(Membership, id=membership_id)
    owner = Membership.objects.filter(group=m.group, user=request.user, role=Membership.OWNER, status=Membership.APPROVED).exists()
    if not owner:
        messages.error(request, 'You are not allowed to reject this request.')
        return redirect('groups:requests')
    m.status = Membership.REJECTED
    m.save()
    messages.success(request, f'Rejected {m.user.username} for {m.group.title}.')
    return redirect('groups:requests')

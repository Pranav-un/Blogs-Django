from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from django.core.exceptions import PermissionDenied
from django.conf import settings
from .models import BlogPost, Blogger, Comment, Reaction, Poll, PollChoice
from .forms import CommentForm, BlogPostForm, PollForm, PollChoiceForm, UserRegistrationForm
from django.contrib.auth.mixins import UserPassesTestMixin

class HomeView(ListView):
    model = BlogPost
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-created_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['most_engaging'] = BlogPost.objects.annotate(
            reaction_count=Count('reactions')
        ).order_by('-reaction_count')[:5]
        return context

class BloggerListView(ListView):
    model = Blogger
    template_name = 'blog/blogger_list.html'
    context_object_name = 'bloggers'

class BloggerDetailView(DetailView):
    model = Blogger
    template_name = 'blog/blogger_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.order_by('-created_date')
        return context

class PostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        if self.request.user.is_authenticated:
            context['user_reaction'] = self.object.reactions.filter(
                user=self.request.user
            ).first()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ['title', 'content', 'image', 'image_caption', 'image_position']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if not hasattr(self.request.user, 'blogger'):
            messages.error(self.request, 'You need to create a blogger profile first.')
            return redirect('blogger-create')
        form.instance.author = self.request.user.blogger
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'image', 'image_caption', 'image_position']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user.blogger
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user.blogger == post.author
    
    def get_success_url(self):
        return reverse_lazy('profile')

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('profile')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user.blogger == post.author

@login_required
def profile_view(request):
    user_posts = BlogPost.objects.filter(author=request.user.blogger).order_by('-created_date') if hasattr(request.user, 'blogger') else []
    return render(request, 'blog/profile.html', {
        'user_posts': user_posts
    })

@login_required
def add_comment(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, "Comment added successfully!")
            except Exception as e:
                messages.error(request, f"Error adding comment: {str(e)}")
        else:
            messages.error(request, "Please enter a valid comment.")
    return redirect('post-detail', pk=pk)

@login_required
def add_reaction(request, pk, reaction_type):
    try:
        post = get_object_or_404(BlogPost, pk=pk)
        reaction, created = Reaction.objects.get_or_create(
            post=post,
            user=request.user,
            defaults={'reaction_type': reaction_type}
        )
        
        if not created:
            if reaction.reaction_type == reaction_type:
                reaction.delete()
                return JsonResponse({'status': 'success', 'action': 'removed'})
            else:
                reaction.reaction_type = reaction_type
                reaction.save()
        
        reaction_counts = {
            'LIKE': post.reactions.filter(reaction_type='LIKE').count(),
            'LOVE': post.reactions.filter(reaction_type='LOVE').count(),
            'WOW': post.reactions.filter(reaction_type='WOW').count(),
        }
        
        return JsonResponse({
            'status': 'success',
            'action': 'updated' if not created else 'added',
            'counts': reaction_counts
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required
def create_poll(request, post_pk):
    post = get_object_or_404(BlogPost, pk=post_pk)
    
    # Check if user is the post owner
    if request.user != post.author.user:
        messages.error(request, "Only the post owner can create polls.")
        return redirect('post-detail', pk=post_pk)
    
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        choice_forms = [PollChoiceForm(request.POST, prefix=str(x)) 
                       for x in range(3)]
        
        if poll_form.is_valid() and all(f.is_valid() for f in choice_forms):
            try:
                poll = poll_form.save(commit=False)
                poll.post = post
                poll.save()
                
                valid_choices = 0
                for form in choice_forms:
                    if form.cleaned_data.get('choice_text', '').strip():
                        choice = form.save(commit=False)
                        choice.poll = poll
                        choice.save()
                        valid_choices += 1
                
                if valid_choices < 2:
                    poll.delete()
                    messages.error(request, "A poll must have at least 2 choices.")
                    return redirect('create-poll', post_pk=post_pk)
                
                messages.success(request, "Poll created successfully!")
                return redirect('post-detail', pk=post_pk)
            except Exception as e:
                messages.error(request, f"Error creating poll: {str(e)}")
                return redirect('post-detail', pk=post_pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        poll_form = PollForm()
        choice_forms = [PollChoiceForm(prefix=str(x)) for x in range(3)]
    
    return render(request, 'blog/create_poll.html', {
        'poll_form': poll_form,
        'choice_forms': choice_forms,
        'post': post
    })

@login_required
def vote_poll(request, choice_pk):
    try:
        choice = get_object_or_404(PollChoice, pk=choice_pk)
        poll = choice.poll
        
        # Check if user has already voted
        if request.user in poll.voters.all():
            return JsonResponse({
                'status': 'error',
                'message': 'You have already voted in this poll'
            }, status=400)
        
        choice.votes += 1
        choice.save()
        poll.voters.add(request.user)
        
        # Calculate percentages for all choices
        total_votes = poll.total_votes
        percentages = {}
        for c in poll.choices.all():
            percentages[str(c.id)] = round((c.votes / total_votes) * 100 if total_votes > 0 else 0, 1)
        
        return JsonResponse({
            'status': 'success',
            'votes': choice.votes,
            'total_votes': total_votes,
            'percentages': percentages
        })
    except ZeroDivisionError:
        return JsonResponse({
            'status': 'error',
            'message': 'Error calculating percentages'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            
            # If user registered as a blogger, create a blogger profile
            if user_type == 'blogger':
                Blogger.objects.create(
                    user=user,
                    bio=form.cleaned_data.get('bio')
                )
            
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

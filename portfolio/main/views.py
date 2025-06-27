from operator import getitem
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from .models import (
    Profile, Skill, Project, Certificate, 
    BlogCategory, BlogPost, ContactMessage
)

def get_profile():
    """Get or create profile instance"""
    try:
        profile = Profile.objects.get(pk=1)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(
            pk=1,
            name='Ananta Deva',
            title='Front-end Engineer & Designer',
            bio='I create futuristic digital experiences with clean code and innovative design.',
            about_desc = "I'm a passionate front-end engineer and designer with expertise in creating modern, responsive web applications. With a keen eye for design and strong technical skills, I bridge the gap between aesthetics and functionality. My approach combines clean code with innovative design to create digital experiences that are not only visually stunning but also highly functional and user-friendly.",
            email='anantadeva07@gmail.com',
            phone='+6281542678058',
            location='Malang, Jawa Timur',
            linkedin_url='www.linkedin.com/in/ananta-deva-a04a6827b', # Add this line
            instagram_url = 'https://www.instagram.com/admiralanant/',
            github_url = 'https://github.com/admiralannt07',
            resume='documents/Front_End_Developer_-_Ananta_Deva_587tjcb.pdf'
        )
    return profile

def home(request):
    """Home page view"""
    profile = get_profile()
    
    try:
        # Get featured content
        featured_projects = Project.objects.filter(
            status='published', 
            is_featured=True
        )[:3]
        
        skills = Skill.objects.filter(is_featured=True).order_by('order')
        
        # Get skills by type for display
        technical_skills = skills.filter(skill_type='technical')
        design_skills = skills.filter(skill_type='design')
        tools_skills = skills.filter(skill_type='tools')
        
        recent_posts = BlogPost.objects.filter(
            status='published'
        ).order_by('-published_at')[:3]
        
    except Exception as e:
        # Handle case where tables don't exist yet
        featured_projects = []
        technical_skills = []
        design_skills = []
        tools_skills = []
        recent_posts = []
    
    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'technical_skills': technical_skills,
        'design_skills': design_skills,
        'tools_skills': tools_skills,
        'recent_posts': recent_posts,
    }
    
    return render(request, 'main/index.html', context)

def projects(request):
    """Projects listing page"""
    try:
        projects_list = Project.objects.filter(status='published').order_by('-is_featured', 'order', '-created_at')
        
        # Filter by technology if specified
        tech_filter = request.GET.get('tech')
        if tech_filter:
            projects_list = projects_list.filter(technologies__name__icontains=tech_filter)
        
        # Pagination
        paginator = Paginator(projects_list, 9)
        page_number = request.GET.get('page')
        projects = paginator.get_page(page_number)
        
        # Get all technologies for filter
        all_technologies = set()
        for project in Project.objects.filter(status='published'):
            for tag in project.technologies.all():
                all_technologies.add(tag.name)
        
        context = {
            'projects': projects,
            'all_technologies': sorted(all_technologies),
            'current_tech': tech_filter,
        }
    except Exception as e:
        context = {
            'projects': [],
            'all_technologies': [],
            'current_tech': None,
        }
    
    return render(request, 'main/projects.html', context)

def project_detail(request, slug):
    """Project detail page"""
    try:
        project = get_object_or_404(Project, slug=slug, status='published')
        
        # Get related projects
        related_projects = Project.objects.filter(
            status='published'
        ).exclude(id=project.id)[:3]
        
        context = {
            'project': project,
            'related_projects': related_projects,
        }
    except Exception as e:
        context = {
            'project': None,
            'related_projects': [],
        }
    
    return render(request, 'main/project_detail.html', context)

def certificates(request):
    """Certificates page"""
    profile = get_profile()
    try:
        certificates_list = Certificate.objects.all().order_by('-is_featured', 'order', '-issue_date')
        
        # Filter by issuer if specified
        issuer_filter = request.GET.get('issuer')
        if issuer_filter:
            certificates_list = certificates_list.filter(issuer__icontains=issuer_filter)
        
        # Pagination
        paginator = Paginator(certificates_list, 12)
        page_number = request.GET.get('page')
        certificates = paginator.get_page(page_number)
        
        # Get all issuers for filter
        all_issuers = Certificate.objects.values_list('issuer', flat=True).distinct()
        
        context = {
            'certificates': certificates,
            'all_issuers': sorted(all_issuers),
            'current_issuer': issuer_filter,
            'profile': profile
        }
    except Exception as e:
        context = {
            'certificates': [],
            'all_issuers': [],
            'current_issuer': None,
            'profile': profile
        }
    
    return render(request, 'main/certificates.html', context)

def blog(request):
    """Blog listing page"""
    profile = get_profile() # Add this line to get the profile
    try:
        posts_list = BlogPost.objects.filter(status='published').order_by('-published_at')
        
        # Get featured post
        featured_post = posts_list.filter(is_featured=True).first()
        
        # Exclude featured post from main list
        if featured_post:
            posts_list = posts_list.exclude(id=featured_post.id)
        
        # Filter by category if specified
        category_filter = request.GET.get('category')
        if category_filter:
            posts_list = posts_list.filter(category__slug=category_filter)
        
        # Search functionality
        search_query = request.GET.get('search')
        if search_query:
            posts_list = posts_list.filter(
                Q(title__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        # Pagination
        paginator = Paginator(posts_list, 9)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        
        # Get all categories
        categories = BlogCategory.objects.all()
        
        context = {
            'posts': posts,
            'categories': categories,
            'featured_post': featured_post,
            'current_category': category_filter,
            'search_query': search_query,
            'profile': profile, # Add this line to pass the profile
        }
    except Exception as e:
        context = {
            'posts': [],
            'categories': [],
            'featured_post': None,
            'current_category': None,
            'search_query': None,
            'profile': profile, # Add this line to pass the profile in case of error
        }
    
    return render(request, 'main/blog.html', context)

def blog_detail(request, slug):
    """Blog post detail page"""
    try:
        post = get_object_or_404(BlogPost, slug=slug, status='published')
        
        # Increment views
        post.views += 1
        post.save(update_fields=['views'])
        
        # Get related posts
        related_posts = BlogPost.objects.filter(
            status='published'
        ).exclude(id=post.id)
        
        if post.category:
            related_posts = related_posts.filter(category=post.category)
        
        related_posts = related_posts[:3]
        
        context = {
            'post': post,
            'related_posts': related_posts,
        }
    except Exception as e:
        context = {
            'post': None,
            'related_posts': [],
        }
    
    return render(request, 'main/blog_detail.html', context)

def contact(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            try:
                # Save to database
                contact_message = ContactMessage.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message
                )
                
                # Send email notification (optional)
                try:
                    send_mail(
                        subject=f'Portfolio Contact: {subject}',
                        message=f'From: {name} ({email})\n\n{message}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.DEFAULT_FROM_EMAIL],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"Email sending failed: {e}")
                
                messages.success(request, 'Your message has been sent successfully! I\'ll get back to you soon.')
            except Exception as e:
                messages.error(request, 'There was an error sending your message. Please try again.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return redirect('home')

def api_projects(request):
    """API endpoint for projects (for AJAX requests)"""
    try:
        projects = Project.objects.filter(status='published').values(
            'title', 'slug', 'description', 'demo_url', 'github_url'
        )
        return JsonResponse(list(projects), safe=False)
    except Exception as e:
        return JsonResponse([], safe=False)

def api_skills(request):
    """API endpoint for skills (for AJAX requests)"""
    try:
        skills = Skill.objects.filter(is_featured=True).values(
            'name', 'skill_type', 'proficiency', 'color'
        )
        return JsonResponse(list(skills), safe=False)
    except Exception as e:
        return JsonResponse([], safe=False)

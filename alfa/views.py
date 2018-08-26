from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from alfa.models import *
from alfa.forms import *
from django.core.paginator import Paginator
from django.core.mail import send_mail
import sendgrid
from sendgrid.helpers.mail import *


def has_premission():
	def has(f):
		def func(request, *args, **kwargs):
			if request.user.is_authenticated:
				return f(request, *args, **kwargs)
			else:
				return HttpResponseRedirect(reverse('main_url'))
		return func
	return has

def home_page(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('admin_url'))
	context = {}
	template_name = 'home_page.html'
	try:
		page = request.GET.get('page')
		if not page:
			page = 1
		all_articles = Paginator(Article.objects.all(), 10)
		context['all_articles'] = all_articles.get_page(page)
		return render(request, template_name, context)
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка. <br>' + str(e)
		return render(request, template_name, context)


def admin_page(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login_url'))
	context = {}
	template_name = 'admin_page.html'
	try:
		page = request.GET.get('page')
		if not page:
			page = 1
		all_articles = Paginator(Article.objects.all(), 10)
		context['all_articles'] = all_articles.get_page(page)
		return render(request, template_name, context)
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка. <br>' + str(e)
		return render(request, template_name, context)

@has_premission()
def edit_article_page(request, id=None):
	context = {}
	template_name = 'edit_article_page.html'
	if id == None:
		context['header'] = 'Add new article'
	else:
		context['header'] = 'Edit article'
	try:
		try:
			article = Article.objects.get(id=id)
		except Exception:
			article = None
		if request.method == 'POST':
			form = ArticleForm(request.POST, request.FILES, instance=article)
			if form.is_valid():
				article = form.save(commit=False)
				text = article.content.splitlines()
				article.preview_text = ''
				for item in text:
					if len(article.preview_text) + len(item) > 100:
						break
					article.preview_text += item
				if len(article.preview_text) == 0:
					article.preview_text = text[0]
				article.save()
				return HttpResponseRedirect(reverse('admin_url'))
			else:
				context['form'] =  form
				context['form'].required_css_class = 'container p-0  rounded-0'
				context['error'] = True
				context['error_message'] = 'Not valid form.<br>' + str(form.errors)
				return render(request, template_name, context)
		else:
			context['form'] =  ArticleForm(instance=article)
			context['form'].required_css_class = 'container p-0  rounded-0'
			return render(request, template_name, context)
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка. <br>' + str(e)
		return render(request, template_name, context)

@has_premission()
def remove_article_page(request, id):
	try:
		article = Article.objects.get(id=id)
	except Article.DoesNotExist:
		return HttpResponseRedirect(reverse('admin_url'))
	article.delete()
	return HttpResponseRedirect(reverse('admin_url'))

def article_page(request, id=None):
	context = {}
	template_name = 'article_page.html'
	try:
		article = Article.objects.get(id=id)
	except Article.DoesNotExist:
		return HttpResponseRedirect(reverse('home_url'))
	context['article'] = article
	return render(request, template_name, context)

def login_page(request):
	context = {}
	template_name = 'login_page.html'
	context['login_form'] = LoginForm()
	context['reg_form'] = RegForm()
	try:
		if request.method == 'POST':
			form = LoginForm(request.POST)
			print(form.is_valid())
			if form.is_valid():
				user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
				if user is None:
					context['error'] = True
					context['error_message'] = 'Incorrect login and/or password.'
					context['login_form'] = form
					return render(request, template_name, context)
				else:
					login(request, user)
					return HttpResponseRedirect(reverse('admin_url'))
			else:
				context['error'] = True
				context['error_message'] = 'Bad form.<br>' + str(form.errors)
				print(str(form.errors))
				context['login_form'] = form
				return render(request, template_name, context)
		else:
			return render(request, template_name, context)
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Error.<br>' + str(e)
		return render(request, template_name, context)

def logout_page(request):
	logout(request)
	return HttpResponseRedirect(reverse('home_url'))

def reg_page(request):
	context = {}
	template_name = 'login_page.html'
	context['login_form'] = LoginForm()
	context['reg_form'] = RegForm()
	try:
		if request.method == 'POST':
			form = RegForm(request.POST)
			if form.is_valid():
				try:
					user = User.objects.get(username=form.cleaned_data['username'])
				except User.DoesNotExist:
					user = None
				if user is not None:
					context['error'] = True
					context['error_message'] = 'User with this usernsme already exist. Try another.'
					context['reg_form'] = form
					return render(request, template_name, context)
				try:
					user = User.objects.get(email=form.cleaned_data['email'])
				except User.DoesNotExist:
					user = None
				if user is not None:
					context['error'] = True
					context['error_message'] = 'User with this email already exist. Try another.'
					context['reg_form'] = form
					return render(request, template_name, context)
				user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
				user.save()
				login(request, user)
				return HttpResponseRedirect(reverse('admin_url'))
			else:
				context['error'] = True
				context['error_message'] = 'Bad form.<br>' + str(form.errors)
				context['reg_form'] = form
				return render(request, template_name, context)
		else:
			return render(request, template_name, context)
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Error.<br>' + str(e)
		return render(request, template_name, context)

def forgot_password_page(request):
	context= {}
	template_name = 'forgot_password_page.html'
	context['form'] = EmailForm()
	try:
		if request.method == 'POST':
			form = EmailForm(request.POST)
			if form.is_valid():
				try:
					user = User.objects.get(email=form.cleaned_data['email'])
				except User.DoesNotExist:
					user = None
				if user is None:
					context['error'] = True
					context['error_message'] = 'User with this email does not exist.'
					context['reg_form'] = form
					return render(request, template_name, context)
				else:
					message = 'Your password: ' + user.password
					sg = sendgrid.SendGridAPIClient(apikey='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')
					from_email = Email("passwordRecovert@vlb.com")
					to_email = Email(user.email)
					subject = "Your password!"
					content = Content("text/plain", message)
					mail = Mail(from_email, subject, to_email, content)
					response = sg.client.mail.send.post(request_body=mail.get())
					context['header'] = 'Recover Yout Account'
					context['success_message'] = 'Email with password was set to Your email.'
					context['url'] = reverse('login_url')
					return render(request, 'info_page.html', context)
			else:
				context['error'] = True
				context['error_message'] = 'Bad form.<br>' + str(form.errors)
				context['reg_form'] = form
				return render(request, template_name, context)
		else:
			return render(request, template_name, context)
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Error.<br>' + str(e)
		return render(request, template_name, context)

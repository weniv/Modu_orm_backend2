from django.db.models.query import QuerySet
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import CustomUserCreationForm
from .mixins import GroupRequiredMixin

# Create your views here.
class BookListView(ListView):
    model = Book # 이 뷰에서 사용할 모델
    template_name = 'books/book_list.html' # 랜더링할 템플릿 파일! 
    context_object_name = 'books' # 컨텍스트 객체 이름! 기본적으로 object_list를 사용함 books 변경
    ordering = ['-publication_date'] # 출판일 기준 내림차순으로 정렬
    paginate_by = 2 # 페이지네이션 기능을 사용하고 한 페이지에 2개의 객체를 보여줌
    
    def get_queryset(self):
        queryset = super().get_queryset() 
        
        query = self.request.GET.get('q') # q라는 파라미터로 전달된 값 가져오기 q는 query의 약자
        if query:
            queryset = queryset.filter(title__icontains=query)
        
        # 정렬조건에 대해서 처리
        sort = self.request.GET.get('sort')
        if sort == 'title':
            queryset = queryset.order_by('title')
        elif sort == 'author':
            queryset = queryset.order_by('author')
        elif sort == 'publication_date':
            queryset = queryset.order_by('publication_date')
        else:
            queryset = queryset.order_by('-publication_date')
        
        # 필터링 기능을 처리
        genre = self.request.GET.get('genre')
        if genre:
            queryset = queryset.filter(genre=genre)
        
        return queryset
        
    
    # https://yourdomain.com/books/?q=검색어

class MainView(TemplateView):
    template_name = 'main.html' # 랜더링할 템플릿 파일

# URL패턴을 지정!
# Template를 구성해서 사용자가 접근할 수 있도록 함!
# 첫번째 화면이 구성되게 됩니다!!

# 컨텍스트 객체 이름 -> 원래는 object_list로 사용되지만, book_list로 변경

class BookDetailView(DetailView):
    model = Book # 이 뷰에서 사용할 모델
    template_name = 'books/book_detail.html' # 랜더링할 템플릿 파일
    context_object_name = 'book' # 컨텍스트 객체 이름! 기본적으로 object를 사용함 book 변경
    
class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book 
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:book_list') # 성공시 이동할 페이지
    # reverse_lazy -> URL 이름을 지연해서 평가 -> 뷰가 로드된 다음에 URL을 생성! 
    # 뷰가 로드되기 전에 URL이 사용되는 상황에서 유용하다. -> 안전하게 URL을 참조하는 기능
    
class BookUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    group_name = 'Editor'
    
    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.pk})
    
class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin , DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('books:book_list') # 성공시 이동할 페이지
    permission_required = 'books/delete_book' # 권한이 필요한 경우 지정
    
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    
from django.views.generic import TemplateView

class RentalInfoView(TemplateView):
    template_name = 'books/rental_info.html'

from django.views.generic.edit import FormView
from .forms import RentalForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class BookRentalView(LoginRequiredMixin, FormView):
    template_name = 'books/book_rental.html'
    form_class = RentalForm
    success_url = reverse_lazy('books:rental_success')  # 네임스페이스와 함께 사용

    def form_valid(self, form):
        rental = form.save(commit=False)
        rental.user = self.request.user  # 로그인된 사용자를 할당
        rental.save()
        return super().form_valid(form)
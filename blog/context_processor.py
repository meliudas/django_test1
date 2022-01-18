from django.core.exceptions import ObjectDoesNotExist

from blog.models import Category, Post, Author, CustomUser


def asd(request):
    categories = Category.objects.all()
    cat_list = []
    for c in categories:
        post = Post.objects.filter(category_id=c.id)
        if post:
            cat_list.append(c.id)
    cat = categories.filter(id__in=cat_list)
    authors = Author.objects.all()
    users = CustomUser.objects.all()
    try:
        category_fan = Category.objects.get(title='Фантастика')
    except ObjectDoesNotExist:
        raise ValueError('Такой категори не существует!')

    params = {'categories': cat,
              'fan': category_fan, 'authors': authors,
              'users': users}



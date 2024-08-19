from django import template

# 커스텀 템플릿 태그와 필터를 등록하는데 사용하는 객체 생성
# register라는 변수에 템플릿 라이브러리 객체를 할당
register = template.Library()

# add_class라는 이름의 커스텀 필터를 등록
# add_class:css_class_name 이러한 방식으로 사용이 가능
@register.filter(name='add_class')
# 필터의 동작을 정의하는 메서드를 정의!
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})
    #form 필드의 HTML 위젯을 변경! css_class -> class속성으로 추가한 상태로 반환!
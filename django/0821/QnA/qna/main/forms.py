from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]

    def clean_title(self):
        """
        title 필드의 유효성 검사를 진행합니다.
        """
        title = self.cleaned_data.get("title")
        if "abcdef" in title:
            print("금지된 언어 사용")
            raise forms.ValidationError("abcdef는 금지된 단어입니다.")
        if "바보" in title:
            print("금지된 언어 사용")
            raise forms.ValidationError("바보는 금지된 단어입니다.")
        if "멍청이" in title:
            print("금지된 언어 사용")
            raise forms.ValidationError("멍청이는 금지된 단어입니다.")
        if "멍충이" in title:
            print("금지된 언어 사용")
            raise forms.ValidationError("멍충이는 금지된 단어입니다.")
        if len(title) < 7:
            raise forms.ValidationError("제목은 7글자 이상 입력해주세요.")
        return title

    def clean(self):
        """
        전체 필드의 유효성 검사를 진행합니다.
        """
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
        if title and content and title.lower() in content.lower():
            raise forms.ValidationError("내용에 제목을 그대로 포함할 수 없습니다.")
        return cleaned_data

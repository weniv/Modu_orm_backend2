# modeling_tip/012.py
# 모델 인스턴스를 삭제하는 대신 비활성화하는 방식을 사용할 수 있습니다.
# 어떤 경우에 이렇게 하는 것이 좋을까요?
# 1. User가 탈퇴한 경우: User 모델을 삭제하는 대신 비활성화합니다. 나중에 활성화 할 수 있도록 합니다.
# 2. 게시판에 게시물 삭제: 게시물을 삭제하는 대신 비활성화합니다. 데이터를 저장할 수 있도록 합니다. 예를 들어, 형사 사건이 발생했을 때, 삭제된 게시물을 복구할 수 있습니다. 캡쳐된 것은 위조가 될 수 있습니다.
# 2.1 형사 사건이 발생했을 때, 협조하지 않는다? 대한민국에서 형사 사건이 발생했을 때, 협조하지 않는다면 처벌을 받을 수 있습니다.(판례를 좀 보서야 합니다. '서버 형사사건 비협조 처벌 사례'로 검색해보세요.)
# 2.2 카카오도 형사사건이 있으면 영장을 받아 채팅을 복구합니다.
# https://www.legaltimes.co.kr/news/articleView.html?idxno=67015
# https://news.kbs.co.kr/news/pc/view/view.do?ncd=5477371
# 2.3 텔레그램은 형사사건이 있었을 때 협조를 안해서 프랑스 체포


class Post(models.Model):
    # ...
    is_active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

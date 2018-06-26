from django.conf.urls import url

from . import stack_views

app_name = 'stack_under_flow'
urlpatterns = [
    url(r'^commitquestion/', stack_views.commitquestion, name='commitquestion'),
    url(r'^displayquestion/', stack_views.displayquestion, name='displayquestion'),
    url(r'^questioninfo/(.+)/$', stack_views.questioninfo, name='questioninfo'),
    url(r'^tag/(.+)/$', stack_views.itemsintag, name='tag'),
    url(r'^search/$', stack_views.search, name='search'),
    url(r'^searchtable/$', stack_views.searchtable, name='searchtable'),
    url(r'^my/', stack_views.my, name='my'),
    url('give_point', stack_views.sendgiftpoint, name='give_point'),
    url('myadmin', stack_views.myadmin, name='myadmin'),
    url('deletetable', stack_views.deletetable, name='deletetable'),
    url('mynews', stack_views.mynews, name='mynews'),
    url('readallmessage', stack_views.readallmessage, name='readallmessage'),
    url(r'^rewritequestion/', stack_views.rewritequestion, name='rewritequestion'),
    url('returnquestioninfo', stack_views.returnquestioninfo, name='returnquestioninfo'),
    url('commitrewritequestion', stack_views.commitrewritequestion, name='commitrewritequestion'),
    url('addtag', stack_views.addtag, name='addtag'),
]

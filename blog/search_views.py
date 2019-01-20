from haystack.views import SearchView
from .models import *
import markdown
from blog.views import Date_time ,Tag_show


class MySeachView(SearchView):
    def extra_context(self):  # 重载extra_context来添加额外的context内容
        context = super(MySeachView, self).extra_context()
        (paginator, page) = self.build_page()
        for item in page.object_list:
            item.object.content = markdown.markdown(item.object.content,
                            extensions =[
                                            'markdown.extensions.extra',
                                            'markdown.extensions.codehilite',
                            ] )
            # context["content"] = item.object.content
            # context['title'] = item.object.title
        # 归档
        data_time_list = Date_time()
        # 标签云
        tags_show = Tag_show()
        # 最新评论
        new_comment = Comment.objects.all().order_by("time")[0:5]

        context["data_time_list"] = data_time_list
        context["tags_show"] = tags_show
        context["new_comment"] = new_comment
        return context

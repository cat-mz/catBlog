from django.views import View
from django.http import JsonResponse, HttpResponse
from django_redis import get_redis_connection
from libs.captcha.captcha import captcha
from utils.constants import REDIS_IMAGES_CODE_TIMEOUT


# imagecode?uuid=xxxxx-xxxx-xxxxxx
class Capcha(View):

    def get(self, request):
        uuid = request.GET.get('uuid')

        if uuid is None:
            return JsonResponse({'errno': 1, 'errmsg': 'uid not found'})

        # value
        text, image = captcha.generate_captcha()
        # 将图片验内容保存到redis中，并设置过期时间
        redis_con = get_redis_connection()
        redis_con.setex('img:%s' % uuid, REDIS_IMAGES_CODE_TIMEOUT, text)
        # 返回响应，将生成的图片以content_type为image/jpeg的形式返回给请求
        return HttpResponse(image, content_type='image/jpeg')

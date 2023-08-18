from ..auth import AuthInfo
from ..base import AlgoBase
from ..tools import FileInfo


class ReplaceHair(AlgoBase):
    __algo_name__ = 'replace_hair'

    def __init__(self, auth_info: AuthInfo, oss_file: FileInfo, styles, process=None, need_cache=True,
                 custom_data=None, **kwargs):
        """
        人像转卡通算法
            文档见 https://www.yuque.com/fenfendeyouzhiqingnian/algorithm/rwibgpgc8d7k6584
        @param auth_info:个人权限配置参数
        @param oss_file:文件对象,FileInfo对象
        @param process:图片缩放参数
        @param need_cache:是否使用缓存
        @param styles:风格类型列表
        @param custom_data:自定义参数,将会随着响应参数原样返回
        """
        super().__init__(auth_info)
        self.request['oss_file'] = oss_file.get_oss_name(self)
        self.request['process'] = process
        self.request['custom_data'] = custom_data
        self.request['need_cache'] = need_cache
        self.request['styles'] = styles
        self.request.update(kwargs)

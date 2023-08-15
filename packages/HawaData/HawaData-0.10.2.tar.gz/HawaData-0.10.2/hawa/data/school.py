from dataclasses import dataclass

from hawa.common.utils import Util
from hawa.config import project
from hawa.paper.health import HealthReportData, HealthApiData
from hawa.paper.mht import MhtWebData, MhtApiData


@dataclass
class SchoolMixin:
    """为了在 __mro__ 中有更高的优先级， mixin 在继承时，应该放在最前"""
    meta_unit_type: str = 'school'


@dataclass
class SchoolHealthApiData(SchoolMixin, HealthApiData):
    def get_class_scores(self):
        """获取年级各班级的分数"""
        scores = self.final_scores
        scores['cls'] = scores['student_id'].apply(lambda x: f"{int(str(x)[13:15])}班")
        res = scores.groupby('cls').score.mean().to_dict()
        keys, values = res.keys(), [Util.format_num(i) for i in res.values()]
        return {'keys': list(keys), 'values': list(values)}


@dataclass
class SchoolHealthReportData(SchoolMixin, HealthReportData):
    pass


@dataclass
class SchoolMhtApiData(SchoolMixin, MhtApiData):
    meta_unit_type: str = 'school'


@dataclass
class SchoolMhtWebData(SchoolMixin, MhtWebData):
    meta_unit_type: str = 'school'
    pass

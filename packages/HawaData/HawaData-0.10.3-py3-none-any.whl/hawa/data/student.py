from dataclasses import dataclass
from typing import Optional

from hawa.base.errors import NoAnswersError
from hawa.config import project
from hawa.paper.health import HealthApiData


@dataclass
class StudentMixin:
    """为了在 __mro__ 中有更高的优先级， mixin 在继承时，应该放在最前"""
    meta_unit_type: str = 'student'


@dataclass
class StudentHealthApiData(StudentMixin, HealthApiData):
    meta_student_id: Optional[int] = None  # 必填
    student_name: Optional[str] = ''

    def _to_init_a0_meta(self):
        if not self.meta_student_id:
            raise ValueError("meta_student_id 必填")

    def _to_init_a_meta_unit(self):
        self.meta_unit = self.query.query_unit(self.meta_unit_type, str(self.meta_student_id))
        self.student_name = self.meta_unit.name

    def _to_init_d_cases(self, is_cleared: bool = True):
        super()._to_init_d_cases(is_cleared=False)

    def _to_init_e_answers(self):
        """筛选学生的答案"""
        self.answers = self.query.query_answers(case_ids=self.case_ids, student_id=self.meta_student_id)

        if len(self.answers) == 0:
            raise NoAnswersError(f"学生 {self.meta_student_id} 没有答题记录")

        project.logger.debug(f'student answers: {len(self.answers)}')

from sqlalchemy.orm import Session
from app.models.module import Module

class ModuleRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, module_id: int) -> Module | None:
        return self.session.query(Module).filter(Module.id == module_id).one_or_none()

    def get_all_by_course(self, course_id: int) -> list[Module]:
        return self.session.query(Module).filter(Module.course_id == course_id).order_by(Module.order_index).all()

    def get_by_course_and_order(self, course_id: int, order_index: int) -> Module | None:
        return self.session.query(Module).filter(Module.course_id == course_id, Module.order_index == order_index).one_or_none()

    def add(self, module: Module) -> Module:
        self.session.add(module)
        self.session.commit()
        self.session.refresh(module)
        return module

    def update(self, module: Module) -> Module:
        self.session.commit()
        self.session.refresh(module)
        return module

    def delete(self, module: Module) -> None:
        self.session.delete(module)
        self.session.commit()
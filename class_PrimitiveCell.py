import numpy as np
import class_Atom as atom


class PrimitiveCell:
    def __init__(self, atoms_cell, a1, a2, angel=60):
        self.atoms_cell = atoms_cell  # 原胞坐标信息(可以计算出键长、键角等信息，后期可以调整反算) atom类型
        self.a1 = a1  # 原胞基矢a1长度
        self.a2 = a2  # 原胞基矢a2长度
        self.angel = angel  # 原胞基矢a1与a2夹角，理论上应该满足12346规则
        self.num_atoms = len(self.atoms_cell)
        self.atom_id = []
        if self.num_atoms == 1:
            self.atom_id = [1]
        elif self.num_atoms == 2:
            self.atom_id = [1, 2]
        else:
            pass

    def get_atoms(self):
        return self.atoms_cell

    def get_num_atoms(self):
        return self.num_atoms

    def get_a(self):
        return self.a1, self.a2

    def get_id_by_element(self, element):
        id_ = 0
        if self.num_atoms == 1:
            return 1
        elif self.num_atoms == 2:
            if self.atoms_cell[0].get_element() != self.atoms_cell[1].get_element():
                for i, item in enumerate(self.atoms_cell):
                    if item.get_element() == element:
                        id_ = self.atom_id[i]
                        break
                return id_
            else:
                return 1
        else:
            return id_

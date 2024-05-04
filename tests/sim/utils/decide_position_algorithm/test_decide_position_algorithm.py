import unittest
import uuid

from src.sim.utils.decide_position_algorithm.enum_algorithm import Algorithm
from src.sim.utils.decide_position_algorithm.algorithm import decide_position
from src.sim.material import Material
from src.sim.drawer import Drawer
from src.sim.warehouse import Warehouse


class BaseDecidePositionAlgorithm(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.warehouse.cleanup()

class TestHighPositionAlgorithm(BaseDecidePositionAlgorithm):
    def test_high_position_algorithm_one_column(self):
        # arrange
        column = self.warehouse.get_column(0)
        last_pos_height = column.get_height_last_position()
        def_space_warehouse = self.warehouse.get_def_space()

        # act
        drawer = Drawer([Material(
            barcode=uuid.uuid4().hex, name='MaterialName',
            height=(last_pos_height + 1) * def_space_warehouse,
            length=100, width=100
        )])
        drawer_last_position = Drawer([Material(
            barcode=uuid.uuid4().hex, name='MaterialName',
            height=1 * def_space_warehouse,
            length=100, width=100
        )])
        alg_res = decide_position([column], drawer.get_num_space_occupied(), Algorithm.HIGH_POSITION)
        alg_res_last_pos = decide_position([column], drawer_last_position.get_num_space_occupied(), Algorithm.HIGH_POSITION)

        # assert
        self.assertEqual(alg_res.column, column)
        self.assertEqual(alg_res_last_pos.column, column)
        self.assertEqual(alg_res.index, last_pos_height)
        self.assertEqual(alg_res_last_pos.index, last_pos_height-1)

    def test_high_position_algorithm_multiple_columns(self):
        pass

    def test_high_position_algorithm_no_more_space(self):
        pass
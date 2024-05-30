import uuid
from unittest import TestCase

from src.tray import Tray
from src.material import Material
from src.status_warehouse.entry.tray_entry import TrayEntry
from src.utils.decide_position_algorithm.algorithm import decide_position
from src.utils.decide_position_algorithm.enum_algorithm import Algorithm
from src.warehouse import Warehouse


class BaseDecidePositionAlgorithm(TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.warehouse.cleanup()

    def test_algorithm_enum(self):
        # arrange
        algorithm = Algorithm

        # act

        # assert
        self.assertRaises(NotImplementedError, decide_position, [None], 1, algorithm)

class TestHighPositionAlgorithm(BaseDecidePositionAlgorithm):
    def test_high_position_algorithm_one_column(self):
        # arrange
        column = self.warehouse.get_column(0)
        last_pos_height = column.get_height_last_position()
        def_space_warehouse = self.warehouse.get_def_space()

        # act
        tray = Tray([Material(
            barcode=uuid.uuid4().hex, name='MaterialName',
            height=(last_pos_height + 1) * def_space_warehouse,
            length=100, width=100
        )])
        tray_last_position = Tray([Material(
            barcode=uuid.uuid4().hex, name='MaterialName',
            height=1 * def_space_warehouse,
            length=100, width=100
        )])
        alg_res = decide_position([column], tray.get_num_space_occupied(), Algorithm.HIGH_POSITION)
        alg_res_last_pos = decide_position([column], tray_last_position.get_num_space_occupied(), Algorithm.HIGH_POSITION)

        # assert
        self.assertEqual(alg_res.column, column)
        self.assertEqual(alg_res_last_pos.column, column)
        self.assertEqual(alg_res.index, last_pos_height)
        self.assertEqual(alg_res_last_pos.index, last_pos_height-1)

    def test_high_position_algorithm_multiple_columns(self):
        # arrange
        column = self.warehouse.get_column(0)
        full_column = self.warehouse.get_column(1)
        full_column_container = full_column.get_container()
        last_pos_height = column.get_height_last_position()
        def_space_warehouse = self.warehouse.get_def_space()
        # fill the whole column except the bottom position
        for i in range(len(full_column_container)-(last_pos_height + 1)):
            entry = full_column_container[i]
            full_column_container[i] = TrayEntry(entry.get_offset_x(), entry.get_pos_y())

        # act
        tray = Tray([Material(
            barcode=uuid.uuid4().hex, name='MaterialName',
            height=(last_pos_height + 1) * def_space_warehouse,
            length=100, width=100
        )])
        tray_last_position = Tray([Material(
            barcode=uuid.uuid4().hex, name='MaterialName',
            height=1 * def_space_warehouse,
            length=100, width=100
        )])
        alg_res = decide_position([full_column, column], tray.get_num_space_occupied(), Algorithm.HIGH_POSITION)
        alg_res_last_pos = decide_position([full_column, column], tray_last_position.get_num_space_occupied(),
                                           Algorithm.HIGH_POSITION)

        # assert
        self.assertNotEqual(alg_res.column, full_column)
        self.assertNotEqual(alg_res_last_pos.column, full_column)
        self.assertEqual(alg_res.column, column)
        self.assertEqual(alg_res_last_pos.column, column)
        self.assertEqual(alg_res.index, last_pos_height)
        self.assertEqual(alg_res_last_pos.index, last_pos_height - 1)

    def test_high_position_algorithm_no_more_space(self):
        # arrange
        column = self.warehouse.get_column(0)
        column_container = column.get_container()
        def_space_warehouse = self.warehouse.get_def_space()
        for i, entry in enumerate(column_container):
            column_container[i] = TrayEntry(entry.get_offset_x(), entry.get_pos_y())

        # act
        tray = Tray([Material(
            barcode=uuid.uuid4().hex, name='MaterialName',
            height=1 * def_space_warehouse,
            length=100, width=100
        )])

        # assert
        self.assertRaises(ValueError, decide_position, [column], tray.get_num_space_occupied(), Algorithm.HIGH_POSITION)

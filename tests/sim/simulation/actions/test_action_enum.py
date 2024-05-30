from unittest import TestCase

from src.simulation.actions.action_enum import ActionEnum


class TestActionEnum(TestCase):
    def test_str(self):
        # arrange
        extract_tray_expected = ActionEnum.EXTRACT_TRAY.value
        send_back_tray_expected = ActionEnum.SEND_BACK_TRAY.value
        insert_random_material_expected = ActionEnum.INSERT_RANDOM_MATERIAL.value
        remove_random_material_expected = ActionEnum.REMOVE_RANDOM_MATERIAL.value

        # act
        extract_tray = ActionEnum.EXTRACT_TRAY.__str__()
        send_back_tray = ActionEnum.SEND_BACK_TRAY.__str__()
        insert_random_material = ActionEnum.INSERT_RANDOM_MATERIAL.__str__()
        remove_random_material = ActionEnum.REMOVE_RANDOM_MATERIAL.__str__()

        # assert
        self.assertEqual(extract_tray, extract_tray_expected)
        self.assertEqual(send_back_tray, send_back_tray_expected)
        self.assertEqual(insert_random_material, insert_random_material_expected)
        self.assertEqual(remove_random_material, remove_random_material_expected)

    def test_from_str(self):
        # arrange
        extract_tray_expected = ActionEnum.EXTRACT_TRAY
        send_back_tray_expected = ActionEnum.SEND_BACK_TRAY
        insert_random_material_expected = ActionEnum.INSERT_RANDOM_MATERIAL
        remove_random_material_expected = ActionEnum.REMOVE_RANDOM_MATERIAL

        # act
        extract_tray = ActionEnum.from_str(extract_tray_expected.__str__())
        send_back_tray = ActionEnum.from_str(send_back_tray_expected.__str__())
        insert_random_material = ActionEnum.from_str(insert_random_material_expected.__str__())
        remove_random_material = ActionEnum.from_str(remove_random_material_expected.__str__())
        none = ActionEnum.from_str("ThisActionDoesn'tExist")

        # assert
        self.assertEqual(extract_tray, extract_tray_expected)
        self.assertEqual(send_back_tray_expected, send_back_tray)
        self.assertEqual(insert_random_material_expected, insert_random_material)
        self.assertEqual(remove_random_material_expected, remove_random_material)
        self.assertIsNone(none)
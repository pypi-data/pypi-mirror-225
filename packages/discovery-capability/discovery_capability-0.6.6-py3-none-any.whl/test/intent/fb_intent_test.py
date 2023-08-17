import unittest
import os
from pathlib import Path
import shutil
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from ds_capability import FeatureBuild
from ds_capability.intent.feature_build_intent import FeatureBuildIntentModel
from aistac.properties.property_manager import PropertyManager

# Pandas setup
pd.set_option('max_colwidth', 320)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 99)
pd.set_option('expand_frame_repr', True)


class FeatureBuilderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # clean out any old environments
        for key in os.environ.keys():
            if key.startswith('HADRON'):
                del os.environ[key]
        # Local Domain Contract
        os.environ['HADRON_PM_PATH'] = os.path.join('working', 'contracts')
        os.environ['HADRON_PM_TYPE'] = 'parquet'
        # Local Connectivity
        os.environ['HADRON_DEFAULT_PATH'] = Path('working/data').as_posix()
        # Specialist Component
        try:
            os.makedirs(os.environ['HADRON_PM_PATH'])
        except OSError:
            pass
        try:
            os.makedirs(os.environ['HADRON_DEFAULT_PATH'])
        except OSError:
            pass
        PropertyManager._remove_all()

    def tearDown(self):
        try:
            shutil.rmtree('working')
        except OSError:
            pass

    def test_for_smoke(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntentModel = fb.tools
        tbl = tools.get_synthetic_data_types(100)
        self.assertEqual((100, 6), tbl.shape)
        self.assertCountEqual(['cat', 'num', 'int', 'bool', 'date', 'string'], tbl.column_names)
        tbl = tools.get_synthetic_data_types(100, inc_nulls=True, prob_nulls=0.03)
        self.assertEqual((100, 19), tbl.shape)

    def test_run_component_pipeline(self):
        fb = FeatureBuild.from_env('test', has_contract=False)
        tools: FeatureBuildIntentModel = fb.tools
        # reload the properties
        fb = FeatureBuild.from_env('test')
        _ = tools.get_synthetic_data_types(10, inc_nulls=True, column_name='d_types')
        result = fb.tools.run_intent_pipeline(size=20)
        self.assertEqual((20, 19), result.shape)

    def test_model_noise(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntentModel = fb.tools
        tbl = tools.get_noise(10, num_columns=3)
        self.assertEqual((10, 3), tbl.shape)
        self.assertEqual(['A', 'B', 'C'], tbl.column_names)
        tbl = tools.get_noise(10, num_columns=3, name_prefix='P_')
        self.assertEqual(['P_A', 'P_B', 'P_C'], tbl.column_names)

    def test_raise(self):
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))


if __name__ == '__main__':
    unittest.main()

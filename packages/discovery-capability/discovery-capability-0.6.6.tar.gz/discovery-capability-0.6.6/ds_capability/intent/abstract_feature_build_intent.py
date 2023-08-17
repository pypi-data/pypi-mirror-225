import numpy as np
import pandas as pd
import pyarrow as pa
from ds_core.intent.abstract_intent import AbstractIntentModel
from ds_core.properties.abstract_properties import AbstractPropertyManager
from ds_capability.components.commons import Commons

class AbstractFeatureBuildIntentModel(AbstractIntentModel):

    _INTENT_PARAMS = ['self', 'save_intent', 'column_name', 'intent_order',
                      'replace_intent', 'remove_duplicates', 'seed']

    def __init__(self, property_manager: AbstractPropertyManager, default_save_intent: bool=None,
                 default_intent_level: [str, int, float]=None, default_intent_order: int=None,
                 default_replace_intent: bool=None):
        """initialisation of the Intent class.

        :param property_manager: the property manager class that references the intent contract.
        :param default_save_intent: (optional) The default action for saving intent in the property manager
        :param default_intent_level: (optional) the default level intent should be saved at
        :param default_intent_order: (optional) if the default behaviour for the order should be next available order
        :param default_replace_intent: (optional) the default replace existing intent behaviour
        """
        default_save_intent = default_save_intent if isinstance(default_save_intent, bool) else True
        default_replace_intent = default_replace_intent if isinstance(default_replace_intent, bool) else True
        default_intent_level = default_intent_level if isinstance(default_intent_level, (str, int, float)) else 'A'
        default_intent_order = default_intent_order if isinstance(default_intent_order, int) else 0
        intent_param_exclude = ['size', 'canonical']
        intent_type_additions = [np.int8, np.int16, np.int32, np.int64, np.float32, np.float64, pd.Timestamp]
        super().__init__(property_manager=property_manager, default_save_intent=default_save_intent,
                         intent_param_exclude=intent_param_exclude, default_intent_level=default_intent_level,
                         default_intent_order=default_intent_order, default_replace_intent=default_replace_intent,
                         intent_type_additions=intent_type_additions)

    def run_intent_pipeline(self, canonical: pa.Table=None, intent_levels: [str, int, list]=None, run_book: str=None,
                            seed: int=None, simulate: bool=None, **kwargs) -> pa.Table:
        """Collectively runs all parameterised intent taken from the property manager against the code base as
        defined by the intent_contract. The whole run can be seeded though any parameterised seeding in the intent
        contracts will take precedence

        :param canonical: a direct or generated pd.DataFrame. see context notes below
        :param intent_levels: (optional) a single or list of intent_level to run in order given
        :param run_book: (optional) a preset runbook of intent_level to run in order
        :param seed: (optional) a seed value that will be applied across the run: default to None
        :param simulate: (optional) returns a report of the order of run and return the indexed column order of run
        :return: a pandas dataframe
        """
        simulate = simulate if isinstance(simulate, bool) else False
        col_sim = {"column": [], "order": [], "method": []}
        # legacy
        canonical = self._get_canonical(canonical)
        size = canonical.shape[0] if isinstance(canonical, pa.Table) else kwargs.pop('size', 1000)
        rtn_tbl = canonical if isinstance(canonical, pa.Table) else None
        # test if there is any intent to run
        if self._pm.has_intent():
            # get the list of levels to run
            if isinstance(intent_levels, (str, list)):
                column_names = Commons.list_formatter(intent_levels)
            elif isinstance(run_book, str) and self._pm.has_run_book(book_name=run_book):
                column_names = self._pm.get_run_book(book_name=run_book)
            else:
                # put all the intent in order of model, get, correlate, associate
                _model = []
                _get = []
                _correlate = []
                for column in self._pm.get_intent().keys():
                    for order in self._pm.get(self._pm.join(self._pm.KEY.intent_key, column), {}):
                        for method in self._pm.get(self._pm.join(self._pm.KEY.intent_key, column, order), {}).keys():
                            if str(method).startswith('get_'):
                                _get.append(column)
                            elif str(method).startswith('model_'):
                                _model.append(column)
                            elif str(method).startswith('correlate_'):
                                if column in _get:
                                    _get.remove(column)
                                _correlate.append(column)
                column_names = Commons.list_unique(_get + _model + _correlate)
            for column in column_names:
                level_key = self._pm.join(self._pm.KEY.intent_key, column)
                for order in sorted(self._pm.get(level_key, {})):
                    for method, params in self._pm.get(self._pm.join(level_key, order), {}).items():
                        try:
                            if method in self.__dir__():
                                if simulate:
                                    col_sim['column'].append(column)
                                    col_sim['order'].append(order)
                                    col_sim['method'].append(method)
                                    continue
                                result = None
                                params.update(params.pop('kwargs', {}))
                                if isinstance(seed, int):
                                    params.update({'seed': seed})
                                _ = params.pop('intent_creator', 'Unknown')
                                if str(method).startswith('get_'):
                                    result = eval(f"self.{method}(size=size, save_intent=False, **params)",
                                                  globals(), locals())
                                elif str(method).startswith('correlate_'):
                                    result = eval(f"self.{method}(canonical=canonical, save_intent=False, **params)",
                                                  globals(), locals())
                                elif str(method).startswith('model_'):
                                    result = eval(f"self.{method}(canonical=canonical, save_intent=False, **params)",
                                                  globals(), locals())
                                # if the return table is not the same assume this is a model change
                                if isinstance(rtn_tbl, pa.Table) and rtn_tbl.num_rows != result.num_rows:
                                    rtn_tbl = None
                                rtn_tbl = Commons.table_append(rtn_tbl, result)
                        except ValueError as ve:
                            raise ValueError(f"intent '{column}', order '{order}', method '{method}' failed with: {ve}")
                        except TypeError as te:
                            raise TypeError(f"intent '{column}', order '{order}', method '{method}' failed with: {te}")
        if simulate:
            return pa.Table.from_pydict(col_sim)
        return rtn_tbl

    """
        PRIVATE METHODS SECTION
    """

    def _get_canonical(self, data: [pa.Table, pa.Array, str]) -> pa.Table:
        """
        :param data: a dataframe or action event to generate a dataframe
        :return: a pa.Table
        """
        if not data:
            return None
        if isinstance(data, pa.Table):
            return data
        if isinstance(data, str):
            if not self._pm.has_connector(connector_name=data):
                raise ValueError(f"The data connector name '{data}' is not in the connectors catalog")
            handler = self._pm.get_connector_handler(data)
            canonical = handler.load_canonical()
            return canonical
        raise ValueError(f"The canonical format is not recognised, {type(data)} passed")

    def _intent_builder(self, method: str, params: dict, exclude: list = None) -> dict:
        """builds the intent_params. Pass the method name and local() parameters
            Example:
                self._intent_builder(inspect.currentframe().f_code.co_name, **locals())

        :param method: the name of the method (intent). can use 'inspect.currentframe().f_code.co_name'
        :param params: the parameters passed to the method. use `locals()` in the caller method
        :param exclude: (optional) convenience parameter identifying param keys to exclude.
        :return: dict of the intent
        """
        exclude = []
        if 'canonical' in params.keys() and not isinstance(params.get('canonical'), (str, dict, list)):
            exclude.append('canonical')
        if 'other' in params.keys() and not isinstance(params.get('other'), (str, dict, list)):
            exclude.append('other')
        return super()._intent_builder(method=method, params=params, exclude=exclude)

    def _set_intend_signature(self, intent_params: dict, column_name: [int, str] = None, intent_order: int = None,
                              replace_intent: bool = None, remove_duplicates: bool = None, save_intent: bool = None):
        """ sets the intent section in the configuration file. Note: by default any identical intent, e.g.
        intent with the same intent (name) and the same parameter values, are removed from any level.

        :param intent_params: a dictionary type set of configuration representing a intent section contract
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        """
        if save_intent or (not isinstance(save_intent, bool) and self._default_save_intent):
            if not isinstance(column_name, (str, int)) or not column_name:
                raise ValueError(f"if the intent is to be saved then a column name must be provided")
        super()._set_intend_signature(intent_params=intent_params, intent_level=column_name, intent_order=intent_order,
                                      replace_intent=replace_intent, remove_duplicates=remove_duplicates,
                                      save_intent=save_intent)
        return

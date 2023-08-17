from process_bigraph.composite import Composite
from process_bigraph.type_system import types


sed_types = {
    'sbml': {
        '_super': 'string',
        '_default': '"something.sbml"',
        '_description': 'sbml model file'
    }
}

types.type_registry.register_multiple(sed_types)  # TODO -- this should go through __init__


sed_compositions = {
    'simulate_and_plot': {
        'time_start': 'float',
        'time_end': 'float',
        'num_points': 'int',
        'selection_list': 'list',
        'model_path': 'directory_path',
        'curves': 'dict',
        'figure1name': 'string',
        'model_instance': 'sbml_model',
        'sbml_model_from_path': {
            '_type': 'step',
            '_ports': {
                'inputs': {
                    'path_to_sbml': 'str'},
                'outputs': {
                    'model': 'Model'}
            }
        },
        'plot2d': {
            '_type': 'step',
            '_ports': {
                'results': 'results',
                'curves': 'curves',
                'name': 'figure1name',
                'figure': 'figure'
            },
        },
        'uniform_time_course': {
            '_type': 'step',
            '_ports': {
                'model': 'model_instance',
                'time_start': 'time_start',
                'time_end': 'time_end',
                'num_points': 'num_points',
                'selection_list': 'selection_list',
                'results': 'results',
            },
        },
    }
}



def test_sed_composite_registry():



    simulation_state = {
        'time_start': 0,
        'time_end': 10,
        'num_points': 50,
        'selection_list': ['time', 'S', 'Z'],
        'model_path': 'data/susceptible_zombie.xml',
        'curves': {
            'Susceptible': {'x': 'time', 'y': 'S'},
            'Zombie': {'x': 'time', 'y': 'Z'}
        },
        'figure1name': '"Figure1"',
        'sbml_model_from_path': {
            'wires': {
                'path_to_sbml': 'model_path',
                'model': 'model_instance'
            },
        },
        'plot2d': {
            'wires': {
                'results': 'results',
                'curves': 'curves',
                'name': 'figure1name',
                'figure': 'figure'
            },
            '_depends_on': ['uniform_time_course'],
        },
        'uniform_time_course': {
            'wires': {
                'model': 'model_instance',
                'time_start': 'time_start',
                'time_end': 'time_end',
                'num_points': 'num_points',
                'selection_list': 'selection_list',
                'results': 'results',
            },
            '_depends_on': ['sbml_model_from_path'],
        }
    }

    workflow = Composite({
        'composition': sed_compositions['simulate_and_plot'],
        # 'schema': {
        #     'results': 'tree[any]'},
        # 'bridge': {
        #     'results': ['analysis_results']},
        'state': simulation_state
    },
    )

    workflow.update({}, 0)


def test_sed_composite_local():

    workflow = Composite({
        'composition': {
            'data': 'tree[any]',
            'model': 'sbml',
            'parameters': 'tree[any]',
            'simulation_results': 'tree[any]',
            'analysis_results': 'tree[any]',
            'parameter_estimation': {
                '_type': 'step',
                '_ports': {
                    'inputs': {
                        'data': 'tree[any]',
                        'model': 'sbml'},
                    'outputs': {
                        'parameters': 'tree[any]'}}},
            'simulator': {
                '_type': 'step',
                '_ports': {
                    'inputs': {
                        'model': 'sbml',
                        'parameters': 'tree[any]'},
                    'outputs': {
                        'simulation_results': 'tree[any]'}}},
            'analysis': {
                '_type': 'step',
                '_ports': {
                    'inputs': {
                        'simulation_results': 'tree[any]'},
                    'outputs': {
                        'analysis_results': 'tree[any]'}
                }
            }
        },
        'schema': {
            'results': 'tree[any]'},
        'bridge': {
            'results': ['analysis_results']},
        'state': {
            'data': {},
            'model': '"something.sbml"',
            'parameter_estimation': {
                'address': 'local:sed2.toy_processes.EstimateParameters',  # using a local toy process
                'config': {},
                'wires': {
                    'inputs': {
                        'data': ['data'],
                        'model': ['model']},
                    'outputs': {
                        'parameters': ['parameters']}}},
            'simulator': {
                'address': 'local:sed2.toy_processes.UniformTimecourse',  # using a local toy process
                'config': {},
                'wires': {
                    'inputs': {
                        'model': ['model'],
                        'parameters': ['parameters']},
                    'outputs': {
                        'simulation_results': ['simulation_results']}}},
            'analysis': {
                'address': 'local:sed2.toy_processes.AnalyzeResults',  # using a local toy process
                'config': {},
                'wires': {
                    'inputs': {
                        'simulation_results': ['simulation_results']},
                    'outputs': {
                        'analysis_results': ['analysis_results']}}}}},
    )

    workflow.update({}, 0)   # TODO -- this is a step-only workflow, should not require interval



if __name__ == '__main__':
    test_sed_composite_registry()

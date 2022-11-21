import os
import re

from mylogger import *
from result_recorder import Recorder
from run_config import *


def test_targets():
    results = []
    results_save_file_path = os.path.join(os.path.dirname(__file__), 'outputs', 'results.csv')
    scene = ['' for i in range(100)]
    order = ['' for i in range(100)]
    error_index = 0

    output_dir = os.path.dirname(__file__).replace('\\', '/') + '/outputs'
    output_picture_dir = output_dir + '/pictures'
    if not os.path.exists(output_picture_dir):
        os.makedirs(output_picture_dir)

    recorder = Recorder(results_save_file_path)
    with open('results.txt', 'w') as _:
        pass
    headers = ['render', 'scene', 'backend', 'integrator', 'sampler', 'resolution',
               'spp', 'max depth', 'rr depth', 'spectrum', 'time consumption']
    while not recorder.init(headers):
        pass

    # clear_log_file()
    logger.info('')
    logger.info('===================== start =====================')

    for renderer in target_settings['renderer']:
        k = 0

        settings = renderer_settings[renderer]

        order[k] = settings['exe']['path'] + ' ' + settings['exe']['appendix']

        for scene_name, scene_targets in target_settings['scene'].items():
            k = 1

            render_directory = os.path.join(os.path.realpath(os.path.dirname(__file__)), renderer)
            scene_directory = os.path.join(render_directory, scene_name)
            scene_file_settings = settings['scene_file']
            scene_file_path = os.path.join(scene_directory, scene_file_settings['scene_file_name'])

            with open(scene_file_path, 'r') as scene_file:
                scene[k] = scene_file.read()
            order[k] = order[k - 1]

            for integrator in target_settings['integrator']:
                k = 2

                integrator_name = scene_file_settings['integrator']['name'][integrator]
                if integrator_name is None:
                    continue
                scene[k] = re.sub(scene_file_settings['integrator']['regex'],
                                  scene_file_settings['integrator']['replace'].
                                  format(integrator_name), scene[k - 1])
                order[k] = order[k - 1] + settings['exe']['integrator']['order'].format(
                    settings['exe']['integrator']['name'][integrator])

                for sampler in target_settings['sampler']:
                    k = 3

                    scene[k] = re.sub(scene_file_settings['sampler']['regex'],
                                      scene_file_settings['sampler']['replace'].
                                      format(scene_file_settings['sampler']['name'][sampler]), scene[k - 1])
                    order[k] = order[k - 1]

                    for resolution in scene_targets['resolution']:
                        k = 4

                        # deal with different resolution format
                        scene[k] = scene[k - 1]
                        if len(scene_file_settings['resolution']) == 2:
                            for i in range(2):
                                scene[k] = re.sub(scene_file_settings['resolution'][i]['regex'],
                                                  scene_file_settings['resolution'][i]['replace'].
                                                  format(resolution[i]), scene[k])
                        elif len(scene_file_settings['resolution']) == 1:
                            scene[k] = re.sub(scene_file_settings['resolution'][0]['regex'],
                                              scene_file_settings['resolution'][0]['replace'].
                                              format(f'{resolution[0]}, {resolution[1]}'), scene[k])
                        else:
                            raise Exception('wrong resolution channels')
                        order[k] = order[k - 1]

                        for spp in target_settings['spp']:
                            k = 5

                            scene[k] = re.sub(scene_file_settings['spp']['regex'],
                                              scene_file_settings['spp']['replace'].
                                              format(spp), scene[k - 1])
                            order[k] = order[k - 1]

                            for max_depth, rr_depth in target_settings['max_depth_and_rr_depth']:
                                k = 6

                                scene[k] = re.sub(scene_file_settings['max_depth']['regex'],
                                                  scene_file_settings['max_depth']['replace'].
                                                  format(max_depth), scene[k - 1])
                                order[k] = order[k - 1]

                                if scene_file_settings['rr_depth'] is None:
                                    rr_depth_unknown = True
                                else:
                                    rr_depth_unknown = False

                                # for rr_depth in target_settings['rr_depth']:
                                k = 7

                                scene[k] = scene[k - 1]
                                order[k] = order[k - 1]

                                if rr_depth_unknown:
                                    rr_depth = 'unknown'
                                else:
                                    scene[k] = re.sub(scene_file_settings['rr_depth']['regex'],
                                                        scene_file_settings['rr_depth']['replace'].
                                                        format(rr_depth), scene[k])

                                for backend in target_settings['backend']:
                                    k = 8

                                    scene[k] = scene[k - 1]
                                    order[k] = order[k - 1]

                                    backend_name = settings['exe']['backend']['name'][backend]
                                    if backend_name is None:
                                        continue
                                    order[k] += settings['exe']['backend']['order'].format(backend_name)

                                    for spectrum in target_settings['spectrum']:
                                        k = 9

                                        # deal with different spectrum format: scene/cmd
                                        scene[k] = scene[k - 1]
                                        order[k] = order[k - 1]
                                        if scene_file_settings['spectrum'] is not None:
                                            scene[k] = re.sub(scene_file_settings['spectrum']['regex'],
                                                                scene_file_settings['spectrum']['replace'].
                                                                format(scene_file_settings['spectrum']['name'][spectrum]),
                                                                scene[k])
                                        else:
                                            spectrum_name = settings['exe']['spectrum']['name'][spectrum]
                                            if spectrum_name is None:
                                                continue
                                            order[k] += settings['exe']['spectrum']['order'].format(spectrum_name)

                                        # output file
                                        output_file_name = f'{renderer}-{scene_name}-{backend}-{integrator}-' \
                                                            f'{sampler}-{resolution[0]}_{resolution[1]}-{spp}spp-' \
                                                            f'{max_depth}max_depth-{rr_depth}rr_depth-{spectrum}'

                                        output_file_name = output_picture_dir + '/' + output_file_name
                                        scene[k] = re.sub(scene_file_settings['output_file']['regex'],
                                                            scene_file_settings['output_file']['replace'].format(
                                                                output_file_name), scene[k])
                                        order[k] += settings['exe']['output'].format(output_file_name + '.exr')

                                        # new scene file confirmed
                                        scene_file_path_new = f'scene-{integrator}-{sampler}-' \
                                                                f'{resolution[0]}_{resolution[1]}-{spp}spp-' \
                                                                f'{max_depth}max_depth-{rr_depth}rr_depth-{spectrum}'
                                        scene_file_path_new = os.path.join(os.path.dirname(scene_file_path),
                                                                            scene_file_path_new) + \
                                                                os.path.splitext(scene_file_settings['scene_file_name'])[
                                                                    -1]
                                        with open(scene_file_path_new, 'w') as f:
                                            f.write(scene[k])

                                        # device
                                        if settings['exe']['device'] is not None:
                                            order[k] += settings['exe']['device'].format(0)

                                        # target scene file
                                        order[k] += ' ' + scene_file_path_new

                                        # order confirmed
                                        logger.info(order[k])

                                        # render
                                        with os.popen(order[k]) as f:
                                            output_info = f.read()
                                        try:
                                            time = re.search(settings['results_regex']['time'], output_info).group(1)
                                        except:
                                            time = 'Error'
                                            error_text = f'Error {error_index}: \n{output_info}\n'
                                            error_index += 1
                                            logger.warning(error_text)

                                        result = [
                                            renderer, scene_name, backend, integrator,
                                            sampler, f'({resolution[0]}, {resolution[1]})',
                                            spp, max_depth, rr_depth, spectrum, time]

                                        results.append(result)
                                        logger.info(result)
                                        recorder.write_row(result)

                                # if rr_depth_unknown:
                                #     break

    while not recorder.flush():
        pass

    logger.info('#################### results ####################')
    logger.info(results)
    logger.info('#################### results ####################')

    # gather_breakdown()

    logger.info('====================== end ======================')
    logger.info('')


if __name__ == '__main__':
    test_targets()

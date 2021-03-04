import click
from logml.commons.config import Config
from logml.eda_tools.runner import ProfilersRunner

def get_eda_config(project_id: str):
    """Returns a Config object for a given project id."""
    path_to_config = f'cfg/eda/{project_id}.yaml'

    return Config(path_to_config)


@click.command('eda', help='Perform EDA.')
@click.argument('run_description', type=click.STRING)
@click.option('--project-id', '-p', help='Unique project identifier.')
@click.option('--dataset-path', '-d', type=click.Path(exists=True),
              help='Local path to the target dataset file.')
@click.pass_context
def main(ctx, run_description: str, project_id: str, dataset_path: str):
    cfg = get_eda_config(project_id)
    # Update config with global params for later use.
    cfg.cfg.update({
        'global_params': dict(
            run_description=run_description,
            project_id=project_id,
            dataset_path=dataset_path,
            destination_folder=f'data/experiments/{run_description}/eda')
    })

    ProfilersRunner(cfg).run()

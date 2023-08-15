import click

from pcsFilter.app import run_all


@click.command()
@click.argument('path')
@click.option(
    '--output-path',
    '-o',
    required=False,
    type=str,
    default='.pcsFilter',
    show_default=True,
    help='Output path for generated files',
)
@click.option('--strict', '-s', is_flag=True, help='Turn on strict mode')
def main(path, output_path, strict):
    """
    pcsFilter is a tool that refactors and runs static code analyses.
    pcsFilter goal is to improve code maintainability
    and prevent its degradation.
    """
    run_all(path, output_path, strict)


if __name__ == '__main__':
    main()

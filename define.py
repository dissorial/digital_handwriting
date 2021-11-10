import click


@click.group()
def main():
    pass


@main.command()
@click.option('--cls',
              prompt='Choose which class of characters to define',
              type=click.Choice([
                  'lowercase_mid', 'lowercase_high', 'lowercase_low',
                  'punctuation_low', 'punctuation_mid', 'punctuation_high'
              ],
                                case_sensitive=False))
def define_characters(cls):
    chars = click.prompt('Define the characters as one string', type=str)

    with open(f'txtsplit/{cls}.txt', 'w') as f:
        f.write(f'{chars}')


if __name__ == "__main__":
    main()

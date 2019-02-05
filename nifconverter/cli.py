import click
import sys
from pynif import NIFCollection
from nifconverter.dbpedia import FromDBpediaConverter
from nifconverter.dbpedia import ToDBpediaConverter
from nifconverter.translator import NIFTranslator

registered_converters = {
    'dbr:wd': FromDBpediaConverter('http://www.wikidata.org/entity/'),
    'wd:dbr': ToDBpediaConverter('http://www.wikidata.org/entity/'),
}

def get_allowed_modes():
    return ', '.join(registered_converters.keys())

@click.command()
@click.option('--mode', required=True, help='Conversion mode, in the form of "source prefix":"target prefix". Supported modes are: '+get_allowed_modes())
@click.option('-i', '--infile', default='-', help='The source NIF file to read. If not provided, stdin is used.')
@click.option('-o', '--outfile', default='-', help='The target NIF file to write. If not provided, stdout is used.')
@click.option('--format', default='turtle', help='The RDF serialization format to use.')
def main(mode, infile, outfile, format):
    """
    Conversion utility for NIF files.

    This converts the identifiers used to annotate mentions in documents
    across knowledge bases. For instance, the following will convert
    a NIF file with DBpedia identifiers to a NIF file with Wikidata identifiers:

       nivconvert --mode dbr:wd -i dbpedia_nif.ttl -o wikidata_nif.ttl

    """

    converter = registered_converters.get(mode)
    if converter is None:
        raise click.BadParameter('Invalid mode. Supported modes are: '+get_allowed_modes())

    translator = NIFTranslator(converter)

    with click.open_file(infile) as f:
        nif = NIFCollection.loads(f.read())

    translator.translate_collection(nif)

    with click.open_file(outfile, 'w') as out:
        out.write(nif.dumps())

if __name__ == '__main__':
    main()

import os
from nifconverter.cli import main
import pynif
from click.testing import CliRunner

def test_invoke_cli():
    testdir = os.path.dirname(os.path.abspath(__file__))
    dbpedia_nif_path = os.path.join(testdir, 'data/sample_dbpedia.ttl')
    wikidata_nif_path = os.path.join(testdir, 'data/sample_wikidata.ttl')
    target_file = os.path.join(testdir, 'out.ttl')

    runner = CliRunner()
    result = runner.invoke(main, ['--mode', 'dbr:wd', '-i', dbpedia_nif_path])
    assert result.exit_code == 0

    nif = pynif.NIFCollection.loads(result.output)
    expected_nif = pynif.NIFCollection.load(wikidata_nif_path)
    assert expected_nif == nif


import tarfile
import shutil
from pankmer.index import subset as _subset
from pankmer.version import __version__

def subset(pk_results, output, genomes, exclusive=False, gzip_level=6):
    output_is_tar = output.endswith('.tar')
    output_dir = output[:-4] if output_is_tar else output
    _subset(str(pk_results.results_dir),
                (str(pk_results.results_dir) if pk_results.input_is_tar else ''),
                 genomes, output, gzip_level, exclusive)
    if output_is_tar:
        with tarfile.open(output, 'w') as tar:
            tar.add(output_dir)
        shutil.rmtree(output_dir)

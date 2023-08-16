import click
from .blast import loadBlastDir, BlastResult
from .fasta import loadFastaFile, Sequence, saveFastaFile, loadFastaFile
from .version import __version__
import os
from typing import Dict, Tuple


@click.group()
@click.version_option(__version__, message="%(version)s")
def cli():
    pass


@cli.group("blast")
def cli_blast():
    pass


@cli_blast.command(name="block_extract")
@click.argument("blast_dir", nargs=1, type=str)
@click.argument("fasta_file", nargs=1, type=str)
@click.argument("output_path", nargs=1, type=str)
@click.option(
    "--only_first", required=False, help="Extract only the first result", is_flag=True
)
def blast_block_extract(
    blast_dir: str, fasta_file: str, output_path: str, only_first: bool
):
    blastResults = loadBlastDir(blast_dir)
    fastaAnnotations = loadFastaFile(fasta_file)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if only_first:
        for br in blastResults:
            fsta = fastaAnnotations[br]
            blst = blastResults[br]

            resultDict: Dict[str, Tuple[BlastResult, Sequence]] = {}
            for result in blst.results:
                splitted = result.name.split('-')
                radical = splitted[0]
                if radical not in resultDict:
                    seqBlock = fsta.getBlockFromBlastResult(result)
                    resultDict[radical] = [result, seqBlock]
                else:
                    if resultDict[radical][0].score < result.score:
                        seqBlock = fsta.getBlockFromBlastResult(result)
                        resultDict[radical] = [result, seqBlock]

            for _, block in resultDict.items():
                block[1].writeFasta(output_path)

    else:
        for br in blastResults:
            fsta = fastaAnnotations[br]
            blst = blastResults[br]

            for r in blst.results:
                result = blst.results[r]
                seqBlock = fsta.getBlockFromBlastResult(result)
                seqBlock.writeFasta(output_path)


@cli.group("fasta")
def cli_fasta():
    pass


@cli_fasta.command(name="summarize")
@click.argument("fasta_file", nargs=1, type=str)
@click.argument("output_path", nargs=1, type=str)
def fasta_summarize(fasta_file: str, output_path: str):
    fastaAnnotations = loadFastaFile(fasta_file)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    summary = {}
    id_counter = 0
    for annotationName, annotation in fastaAnnotations.items():
        if annotationName not in summary:
            i = id_counter
            summary[annotationName] = i
            id_counter += 1

        annotation.name = i

    inputFastaDataSuffix = os.path.splitext(fasta_file)[0]
    inputFastaDataSuffix = os.path.basename(inputFastaDataSuffix)
    outputFastaFilePath = os.path.join(
        output_path, inputFastaDataSuffix + "_summirized.fasta"
    )

    saveFastaFile(outputFastaFilePath, fastaAnnotations)

    outputSummaryFilePath = os.path.join(
        output_path, inputFastaDataSuffix + "_summary.csv"
    )
    file = open(outputSummaryFilePath, 'w')
    for annotationName, id in summary.items():
        file.write(f"{id};{annotationName}\n")
    file.close()


if __name__ == "__main__":
    cli()

from io import BufferedWriter
from typing import Dict
import os

from dataclasses import dataclass
from .blast import BlastResult


@dataclass(slots=True)
class Sequence:
    sequence: str
    name: str
    start: int
    end: int

    @staticmethod
    def loadFromFasta(fastaString: str):
        lines = fastaString.split("\n")
        name = lines[0][1:].replace(" ", "-")
        sequence = "".join(lines[1:]).upper()
        start = 1
        end = len(sequence)
        return Sequence(sequence, name, start, end)

    def getBlock(self, start, end):
        seq = self.sequence[start - 1 : end].upper()
        return Sequence(seq, self.name, start, end)

    def getBlockFromBlastResult(self, blast: BlastResult):
        block = self.getBlock(blast.query_begin, blast.query_end)
        block.name += "--" + blast.name
        return block

    def writeFasta(self, outputDir):
        fileName = self.name + ".fasta"
        with open(os.path.join(outputDir, fileName), "w") as file:
            self._writeFastaOnFile(file)

    def _writeFastaOnFile(self, file: BufferedWriter):
        file.write(f">{self.name}\n")
        for i in range(0, len(self.sequence), 70):
            file.write(self.sequence[i : i + 70] + "\n")


def loadFastaFile(path: str) -> Dict[str, Sequence]:
    file = open(path, "r")

    fastaAnnotations = {}
    fastaAnnotationString = None
    for line in file:
        if '>' in line:
            if fastaAnnotationString is not None:
                annotation = Sequence.loadFromFasta(fastaAnnotationString)
                fastaAnnotations[annotation.name] = annotation
            fastaAnnotationString = line
        else:
            fastaAnnotationString = fastaAnnotationString + line

    if fastaAnnotationString is not None:
        annotation = Sequence.loadFromFasta(fastaAnnotationString)
        fastaAnnotations[annotation.name] = annotation

    return fastaAnnotations


def saveFastaFile(path: str, fastas: Dict[str, Sequence]) -> None:
    file = open(path, "w")

    for _, annotation in fastas.items():
        annotation._writeFastaOnFile(file)

    file.close()

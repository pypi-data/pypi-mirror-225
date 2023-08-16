import os
import re
from dataclasses import dataclass
from typing import List, Dict


@dataclass(slots=True)
class BlastDataset:
    database: str
    sequencies: int
    letters: int


@dataclass(slots=True)
class BlastQuery:
    name: str
    length: int


@dataclass(slots=True)
class BlastResult:
    name: str
    length: int
    score: float
    score_unit: str
    expect: float
    identity_max: int
    identity_obtained: int
    gaps: int
    strand: str
    query_begin: int
    query_end: int
    subject_begin: int
    subject_end: int


@dataclass(slots=True)
class Blast:
    blastType: str
    dataset: BlastDataset
    query: BlastQuery
    results: List[BlastResult]
    file: str
    reference: str

    @staticmethod
    def _getNextRelevantLineFromFile(file) -> str:
        line = "\n"
        while line == "\n":
            line = file.readline()
        return line

    def __init__(self, filePath):
        self.file = filePath
        file = open(filePath)

        self.blastType = file.readline().rstrip()

        line = self._getNextRelevantLineFromFile(file)

        self.reference = ""

        while line != "\n":
            self.reference = self.reference + line.rstrip()
            line = file.readline()
        self.reference = self.reference.replace("Reference: ", "")

        line = self._getNextRelevantLineFromFile(file)
        database = line.rstrip().replace("Database: ", "")
        line = file.readline()
        line = line.split(";")
        sequencies = int(line[0].replace(" sequences", "").strip())
        letters = int(
            line[1]
            .replace(" letters", "")
            .replace(" total", "")
            .replace(",", "")
            .strip()
        )

        self.dataset = BlastDataset(database, sequencies, letters)

        line = self._getNextRelevantLineFromFile(file)
        name = line.replace("Query= ", "").strip().replace(" ", "-")
        line = self._getNextRelevantLineFromFile(file)
        length = int(line.replace("Length=", "").strip())

        self.query = BlastQuery(name, length)

        while "> " not in line and line != '':
            line = file.readline()

        self.results = {}

        while line != '':
            if line == '':
                break

            seq_name = line.replace("> ", "").strip()
            length = int(file.readline().replace("Length=", "").strip())

            line = self._getNextRelevantLineFromFile(file)

            line = line.split(",")
            line[0] = line[0].replace("Score =", "").strip().split(" ")
            line[1] = line[1].replace("Expect =", "").strip().split(" ")

            score = float(line[0][0])
            score_unit = line[0][1]
            expect = float(line[1][0])

            line = file.readline()
            line = line.split(",")
            line[0] = (
                line[0].replace("Identities =", "").strip().split(" ")[0].split("/")
            )
            line[1] = line[1].replace("Gaps =", "").strip().split(" ")[0].split("/")
            identity_max = int(line[0][1])
            identity_obtained = int(line[0][0])
            gaps = int(line[1][0])

            strand = file.readline().replace("Strand=", "").strip()
            queryLines = []
            subjectLines = []

            while "> " not in line and line != '':
                line = file.readline()
                if "Query" in line:
                    queryLines.append(line)
                elif "Sbjct" in line:
                    subjectLines.append(line)

            firstQueryLine = re.sub(" +", " ", queryLines[0].strip()).split(" ")
            lastQueryLine = re.sub(" +", " ", queryLines[-1].strip()).split(" ")
            query_begin = int(firstQueryLine[1])
            query_end = int(lastQueryLine[3])

            firstSubjectLine = re.sub(" +", " ", subjectLines[0].strip()).split(" ")
            lastSubjectLine = re.sub(" +", " ", subjectLines[-1].strip()).split(" ")
            subject_begin = int(firstSubjectLine[1])
            subject_end = int(lastSubjectLine[3])

            self.results[seq_name] = BlastResult(
                seq_name,
                length,
                score,
                score_unit,
                expect,
                identity_max,
                identity_obtained,
                gaps,
                strand,
                query_begin,
                query_end,
                subject_begin,
                subject_end,
            )

        file.close()


def loadBlastDir(path) -> Dict[str, Blast]:
    blasts = {}

    for file in os.listdir(path):
        ext = os.path.splitext(file)[1]
        if ext == ".out":
            blast = Blast(os.path.join(path, file))
            blasts[blast.query.name] = blast

    return blasts

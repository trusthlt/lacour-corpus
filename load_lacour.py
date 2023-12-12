import logging
import os
import re
import xml.etree.ElementTree as ET
from itertools import groupby
from typing import Dict, List


def write_xml(file: str, output_dir: str) -> None:
    """Write an xml file from a txt file transcript.

    Args:
        file (str): Location of the txt file.
        output_dir (str): Target location of the xml file.
    """
    transcript, w_id = load_transcript(file, fformat="txt")
    rootname = "Transcript"
    root = ET.Element(rootname)
    root.tail = "\n"
    webcast = ET.SubElement(root, "WebcastID")
    webcast.text = w_id
    webcast.tail = "\n"
    for _, value in groupby(transcript, lambda x: x["segment_id"]):
        snippets = list(value)
        assert (
            len(set([v["speaker_name"] for v in snippets])) == 1
        ), "There are non unique names in the speaker segment"
        assert (
            len(set([v["speaker_role"] for v in snippets])) == 1
        ), "There are non unique roles in the speaker segment"
        speaker_segment = ET.SubElement(root, "SpeakerSegment")
        speaker_segment.tail = "\n"
        role = ET.SubElement(speaker_segment, "Role")
        role.text = snippets[0]["speaker_role"]
        role.tail = "\n"
        name = ET.SubElement(speaker_segment, "Name")
        name.text = snippets[0]["speaker_name"]
        name.tail = "\n"
        for snip in snippets:
            snippet = ET.SubElement(speaker_segment, "Snippet")
            snippet.tail = "\n"

            language = ET.SubElement(snippet, "Language")
            language.text = snip["language"]
            language.tail = "\n"

            timestamp_begin = ET.SubElement(snippet, "TimestampBegin")
            timestamp_begin.text = str(snip["begin"])
            timestamp_begin.tail = "\n"

            timestamp_end = ET.SubElement(snippet, "TimestampEnd")
            timestamp_end.text = str(snip["end"])
            timestamp_end.tail = "\n"

            text_element = ET.SubElement(snippet, "Text")
            text_element.text = snip["text"]
            text_element.tail = "\n"

    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write(
        f"{output_dir}/{w_id}_transcript.xml", encoding="utf-8", xml_declaration=True
    )


def load_transcript(f: str, fformat: str = "txt") -> (List[Dict[str, str]], str):
    """Load a transcript from a file and parse it by snippets

    Args:
        f (str): Location of the file.
        fformat (str, optional): Defines the file format to load. Supports 'txt' or 'xml'. Defaults to 'txt'.

    Raises:
        NotImplementedError: File formats other than 'txt' or 'xml' are not supported.

    Returns:
        (List[Dict[str, str]], str): List of dictionaries containing snippets and the webcast id.
    """
    # assert that file exists
    assert os.path.exists(f), f"File does not exist or is not accessible: {f}"

    if fformat == "txt":
        # assert that file is txt file
        assert f.endswith(".txt"), f"File is not a txt file: {f}"
        # extract webcast_id from file name
        try:
            w_id = re.search(r"([0-9]+\_[0-9]+)(?=\_transcript)", f)[0]
        except AttributeError:
            logging.warning(f"Could not find a valid webcast id in the file name {f}")
        with open(f, "r", encoding="utf-8-sig") as transcript:
            lines = transcript.readlines()
            segment_id = -1
            speech_line_idx = -1
            role, name, lang = "UNK", "UNK", "UNK"
            begin, end = 0, 0
            segments = []
            for idxl, l in enumerate(lines):
                if l.startswith("\n"):
                    continue
                elif l.startswith("[["):
                    segment_id += 1
                    try:
                        role, name = l.split("[[")[1].split("]]")[0].split(";")
                    except ValueError:
                        logging.warning(
                            f"There was an issue reading line {idxl} in {f}"
                        )
                elif l.startswith("<<"):
                    try:
                        begin, end, lang = l.split("<<")[1].split(">>")[0].split(";")
                        begin = float(begin)
                        end = float(end)
                    except ValueError:
                        logging.warning(
                            f"There is an incorrectly formed speech tag in {f} in line {l}"
                        )
                else:
                    speech_line_idx += 1
                    segments.append(
                        {
                            "webcast_id": w_id,
                            "segment_id": segment_id,
                            "snippet_id": speech_line_idx,
                            "speaker_role": role,
                            "speaker_name": name,
                            "language": lang,
                            "begin": begin,
                            "end": end,
                            "text": l.lstrip().rstrip(),
                        }
                    )
            return segments, w_id

    elif fformat == "xml":
        # assert that file is xml file
        assert f.endswith(".xml"), f"File is not an xml file: {f}"
        id_ = 0
        tree = ET.parse(f)
        root = tree.getroot()
        # webcast_id is in field
        w_id = root.findtext("WebcastID")
        segment_id = 0
        segments = []
        for speaker_segment in root.findall("SpeakerSegment"):
            for snippet in speaker_segment.findall("Snippet"):
                segments.append(
                    {
                        "webcast_id": w_id,
                        "segment_id": segment_id,
                        "snippet_id": id_,
                        "speaker_role": speaker_segment.findtext("Role", ""),
                        "speaker_name": speaker_segment.findtext("Name", ""),
                        "language": snippet.findtext("Language", ""),
                        "begin": float(snippet.findtext("TimestampBegin", "")),
                        "end": float(snippet.findtext("TimestampEnd", "")),
                        "text": snippet.findtext("Text", "").strip(),
                    }
                )
                id_ += 1
            segment_id += 1
        return segments, w_id
    else:
        # no other file formats are supported for now
        raise NotImplementedError

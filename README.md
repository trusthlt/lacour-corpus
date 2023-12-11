# LaCour! Corpus

Companion dataset to the [arXiv preprint](http://arxiv.org/abs/2312.05061) presenting the ``LaCour!`` corpus.


Please use the following citation

```plain
@article{held2023lacour,
    author = {Held, Lena and Habernal, Ivan},
    title = {{LaCour!: Enabling Research on Argumentation in Hearings of the European Court of Human Rights}},
    journal = {arXiv preprint},
    year = {2023},
    doi = {10.48550/arXiv.2312.05061},
}
```

> **Abstract** Why does an argument end up in the final court decision? Was it deliberated or questioned during the oral hearings? Was there something in the hearings that triggered a particular judge to write a dissenting opinion? Despite the availability of the final judgments of the European Court of Human Rights (ECHR), none of these legal research questions can currently be answered as the ECHR's multilingual oral hearings are not transcribed, structured, or speaker-attributed. We address this fundamental gap by presenting LaCour!, the first corpus of textual oral arguments of the ECHR, consisting of 154 full hearings (2.1 million tokens from over 267 hours of video footage) in English, French, and other court languages, each linked to the corresponding final judgment documents. In addition to the transcribed and partially manually corrected text from the video, we provide sentence-level timestamps and manually annotated role and language labels. We also showcase LaCour! in a set of preliminary experiments that explore the interplay between questions and dissenting opinions. Apart from the use cases in legal NLP, we hope that law students or other interested parties will also use LaCour! as a learning resource, as it is freely available in various formats at https://huggingface.co/datasets/TrustHLT/LaCour. 

**Contact person**: Lena Held, lena.held@tu-darmstadt.de

## tl;dr
||||
|:---:|:---|:---|
|:book:|Reading some ECHR hearing transcripts? |[LaCour! Preview](https://www.trusthlt.org/lacour/transcripts.html)|
|:hugs:|Dataset convenient and easy usage |[Huggingface Dataset](https://huggingface.co/datasets/TrustHLT/LaCour)|
||Download the individual transcript files |[.txt](transcripts-txt) [.xml](transcripts-xml)|
||Download the documents meta data |[documents](lacour_linked_documents.json)|
|:woman_technologist:|Creation code for reproduction |[trusthlt/lacour-generation](https://github.com/trusthlt/lacour-generation)|
|:interrobang:|Questions and opinions dataset |[trusthlt/lacour-qando](https://github.com/trusthlt/lacour-quando)|

## Data

The dataset consists of 2 subsets.

### Subset transcripts
The first subset ``transcripts`` contains the 154 transcripts of court hearings. It is provided in 2 different formats, ``.xml`` or ``.txt``. All text and information is the same in both formats.
 
Files in .txt format have the following structure:

```
[[Announcer;UNK]]

<<22.32;23.16;fr>>
La Cour!
```
``[[]]`` denotes a segment with the information ``Role`` and ``Name`` for the speaker, ``<<>>`` marks snippets with a begin, end and language tag, followed by the text.

Files in .xml format have the following structure:

```
<transcript_20117_21112018>
  <SpeakerSegment>
    <Segment>
      <meta_data>
        <Role>Announcer</Role>
        <Name>UNK</Name>
        <TimestampBegin>22.32</TimestampBegin>
        <TimestampEnd>23.16</TimestampEnd>
        <Language>fr</Language>
      </meta_data>
      <text>La Cour!</text>
    </Segment>
    ...
  </SpeakerSegment>
  ...
  </transcript_20117_21112018>
```
We provide this nested format to make potential annotation tasks easier.

Both file formats contain the following information:

* webcast_id: the identifier for the hearing (allows linking to documents)
* Role: the role/party the speaker represents (`Announcer` for announcements, `Judge` for judges, `JudgeP` for judge president, `Applicant` for representatives of the applicant, `Government` for representatives of the respondent government, `ThirdParty` for representatives of third party interveners)
* Name: the name of the speaker (not given for Applicant, Government or Third Party)
* Begin: the timestamp for begin of line (in seconds)
* End: the timestamp for end of line (in seconds)
* Language: the language spoken (in ISO 639-1)
* text: the spoken line

### Subset documents

The second subset ``documents`` contains information on all relevant documents found in the [HUDOC database](https://hudoc.echr.coe.int) which have a link to a webcast hearing. This link is established by the application number associated with the hearing and a case. To link transcripts with these documents, the ``webcast_id`` can be used.
Each instance in documents represents information on a document in hudoc associated with a hearing and the metadata associated with a hearing. Note: `hearing_type` states the type of the hearing, `type` states the type of the document. If the hearing is a "Grand Chamber hearing", the "CHAMBER" document refers to a different hearing.

```
 '4': {
    'webcast_id': '2438419_29092021',
    'hearing_date': '2021-09-29 00:00:00',
    'hearing_title': 'H.F. and M.F. v. France and J.D. and A.D. v. France (nos. 24384/19 and 44234/20)',
    'hearing_type': 'Grand Chamber hearing',
    'appno': '44234/20',
    'case_id': '001-219333',
    'case_name': 'CASE OF H.F. AND OTHERS v. FRANCE',
    'case_url': 'https://hudoc.echr.coe.int/eng?i=001-219333',
    'type': 'GRANDCHAMBER',
    'typedescription': 15,
    'document_date': '2022-09-14 00:00:00',
    'collection': 'CASELAW;JUDGMENTS;GRANDCHAMBER;ENG',
    'importance': 1,
    'court': '8',
    'issue': 'Inter-ministerial instruction no. 5995/SG of 23 February 2018 on “Provisions to be made for minors on their return from areas of terrorist group operations (in particular the Syria-Iraq border area)”',
    'represented_by': 'DOSÉ M.',
    'respondent': 'FRA',
    'articles': '1;34;35;35-3-a;41;46;46-2;P4-3;P4-3-2',
    'strasbourg_caselaw': 'Abdi Ibrahim v. Norway [GC], no. 15379/16, § 180, 10 December 2021;Abdul Wahab Khan v. the United Kingdom (dec.), no. 11987/11, §§ 27-28, 28 January 2014;Airey v. Ireland, 9 October 1979, §§ 24-25, Series A no. 32;Al-Dulimi and Montana Management Inc. v. Switzerland [GC], no. 5809/08, §§ 134 and 145-146, 21 June 2016;[...]',
    'external_sources': 'Article 12 § 4 of the International Covenant on Civil and Political Rights (ICCPR);United Nations Human Rights Committee’s (UNCCPR) General Comment no. 27 on the Freedom of Movement under Article 12 of the ICCPR, adopted on 1 November 1999 (UN Documents CCPR/C/21/Rev.1/Add.9);Article 19 of the International Law Commission (ILC) Draft Articles on Diplomatic Protection and commentary;[...]',
    'conclusion': 'Preliminary objection dismissed (Art. 34) Individual applications;(Art. 34) Locus standi;Remainder inadmissible (Art. 35) Admissibility criteria;(Art. 35-3-a) Ratione loci;(Art. 35-3-a) Ratione personae;Violation of Article 3 of Protocol No. 4 - Prohibition of expulsion of nationals (Article 3 para. 2 of Protocol No. 4 - Enter own country);Respondent State to take individual measures (Article 46-2 - Individual measures);Non-pecuniary damage - finding of violation sufficient (Article 41 - Non-pecuniary damage;Just satisfaction)',
    'separate_opinion': 'TRUE',
    'judges': "Ganna Yudkivska;Jon Fridrik Kjølbro;Krzysztof Wojtyczek;Mārtiņš Mits;Robert Spano;Síofra O'Leary;Stéphanie Mourou-Vikström;Yonko Grozev;Georges Ravarani;Ksenija Turković;Lorraine Schembri Orland",
    'ecli': 'ECLI:CE:ECHR:2022:0914JUD002438419'
    },

```
The fields in documents are:

* id: the identifier
* webcast_id: the identifier for the hearing (allows linking to transcripts)
* hearing_date: the date of the hearing
* hearing_title: the title of the hearing
* hearing_type: the type of hearing (Grand Chamber, Chamber or Grand Chamber Judgment Hearing)
* appno: the application number which is associated with the hearing and case
* case_id: the id of the case
* case_name: the name of the case 
* case_url: the direct link to the document
* type: the type of the document
* typedescription: the exact identifier of the document type (distinction between e.g. Merits and Just Satisfaction, no key provided)
* document_date: the date of the document
* collection: the categorization of the document, i.e. type of document, type of chamber, language
* importance: the importance score of the case (1 is the highest importance, key case)
* court: the identifier for the court that issued the document
* issue: the references to the issue of the case
* represented_by: the person(s) representing the applicant(s)
* respondent: the code of the respondent government(s) (in ISO-3166 Alpha-3)
* articles: the concerning articles of the Convention of Human Rights
* strasbourg_caselaw: the list of cases in the ECHR which are relevant to the current case
* external_sources: the relevant references outside of the ECHR
* conclusion: the short textual description of the conclusion
* separate_opinion: the indicator if there is a separate opinion
* judges: the judges appearing in the associated document
* ecli: the ECLI (European Case Law Identifier)

## Usage

tbd


## Questions and Opinions

The companion dataset for the experimental part using questions asked during the hearings and dissenting or concurring opinions can be found in the repository [trusthlt/lacour-qando](https://github.com/trusthlt/lacour-qando).

## Data creation

Companion code for the creation of this dataset is available in the repository [trusthlt/lacour-generation](https://github.com/trusthlt/lacour-generation). 


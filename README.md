# ai-conference-keywords

This is a simple python script that searches for keywords in papers of major AI conferences (CVPR, ICML, and NIPS currently supported) and extracts their frequency.

## Installation

Install the requirements:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python ckc.py --conferences="CVPR2019,ICML2018,NIPS2017" --keywords="deep,network"
```

searches for papers in CVPR2019, ICML2018, and NIPS2017 with the keywords "deep" or "network" in their title and extracts the frequency.

Example output:

```bash
CVPR2019: 10.74% (139 out of 1294)
ICML2018: 9.98% (62 out of 621)
NIPS2017: 9.43% (64 out of 679)
```


## Contributing
Pull requests are welcome.


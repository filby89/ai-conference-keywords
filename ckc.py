# !/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from lxml import html
import argparse
from colorama import init
init()
from colorama import Fore, Style

def parse_opts():
	parser = argparse.ArgumentParser()
	parser.add_argument('--conferences', default='CVPR2018,ICCV2017,ECCV2018,NIPS2018,ICML2018', type=str, help='conferences to crawl')

	parser.add_argument('--keywords', default='network', type=str, help='keywords to search')

	args = parser.parse_args()

	args.conferences = [x.strip() for x in args.conferences.split(",")]
	args.keywords = [x.strip() for x in args.keywords.split(",")]

	return args


def parse_thecvf(conference, keywords):
	response = requests.get("http://openaccess.thecvf.com/"+conference+".py")
	tree = html.fromstring(response.text) # get html tree
	papers = tree.find_class('ptitle') 

	paper_titles = [paper.find("a").text for paper in papers]

	found = [1 if paper.lower().find(keyword) >= 0 else 0 for keyword in keywords for paper in paper_titles]

	return found

def parse_icml(conference, keywords):
	icml_to_vol = {
		"ICML2018": "v80",
		"ICML2017": "v70",
		"ICML2016": "v48",
		"ICML2015": "v37",
		"ICML2014": "v32",
		"ICML2013": "v28"
	}

	response = requests.get("http://proceedings.mlr.press/"+icml_to_vol[conference])
	tree = html.fromstring(response.text) # get html tree
	papers = tree.find_class('paper') 

	paper_titles = [paper.find_class("a")[0].text for paper in papers]

	found = [1 if paper.lower().find(keyword) >= 0 else 0 for keyword in keywords for paper in paper_titles]

	return found

def parse_nips(conference, keywords):
	nips_to_vol = {
		"NIPS2018": "advances-in-neural-information-processing-systems-31-2018",
		"NIPS2017": "advances-in-neural-information-processing-systems-30-2017",
		"NIPS2016": "advances-in-neural-information-processing-systems-29-2016",
		"NIPS2015": "advances-in-neural-information-processing-systems-28-2015",
		"NIPS2014": "advances-in-neural-information-processing-systems-27-2014",
		"NIPS2013": "advances-in-neural-information-processing-systems-26-2013",
	}

	response = requests.get("https://papers.nips.cc/book/"+nips_to_vol[conference])
	tree = html.fromstring(response.text) # get html tree
	all_links = tree.xpath('.//a')

	paper_titles = [x.text for x in all_links if "/paper/" in x.get("href") ]

	found = [1 if paper.lower().find(keyword) >= 0 else 0 for keyword in keywords for paper in paper_titles]

	return found

def main(args):
	for conference in args.conferences:
		if "CVPR" in conference or "ICCV" in conference or "ECCV" in conference:
			found = parse_thecvf(conference, args.keywords)
		elif "ICML" in conference:
			found = parse_icml(conference, args.keywords)
		elif "NIPS" in conference:
			found = parse_nips(conference, args.keywords)

		percent = sum(found)/len(found)*100
		print(Fore.RED + "%s: %.2f%% (%d out of %d)" % (conference, percent, sum(found), len(found)) + Style.RESET_ALL)


if __name__ == '__main__':
	args = parse_opts()
	main(args)


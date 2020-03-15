import sys
import os,re
import pdb

# takes 2 arguments: unlabelled file, labelled file
# python format_checker.py input.txt output.txt 

wo_lbl = open(sys.argv[1],"r")
w_lbl = open(sys.argv[2],"r")

wo_lbl_lines = wo_lbl.readlines()
w_lbl_lines = w_lbl.readlines()

if len(wo_lbl_lines)!=len(w_lbl_lines):
	print "damn!!! number of lines incorrect... (error!!!)"
	exit(1)

for i in range(len(wo_lbl_lines)):
	wo_items = wo_lbl_lines[i].strip().split(" ")
	w_items = w_lbl_lines[i].strip().split(" ")

	if wo_items[0]=="" and w_items[0]=="":
		continue

	if wo_items[0]=="" and w_items[0]!="":
		print "Error:: Line %d in labelled file should have been blank" %(i+1)
		exit(1)

	if len(wo_items)!=1:
		print "Error:: Unlabelled file doesn't have exactly 1 token in line %d" %(i+1)
		exit(1)

	if len(w_items)!=2:
		print "Error:: Labelled file doesn't have exactly 2 tokens in line %d" %(i+1)
		exit(1)

	if w_items[0]!=wo_items[0]:
		print "Error:: token mismatch, between labelled and unlabelled files, on line %d" %(i+1)
		exit(1)

	
	if w_items[1]!="L" and w_items[1]!="P" and w_items[1]!="LA" and w_items[1]!="C" and w_items[1]!="N" and w_items[1]!="T" and w_items[1]!="A" and w_items[1]!="O":
		print "darn!!! label token is different from Locality (L), Total Price (P), Land Area (LA), Cost per land area (C), Contact name (N), Contact telephone (T), Attributes of the property (A), Other (O) on line %d... (error!!!)" %(i+1)
		exit(1)


print "congratulations!! your format is spot on!!!"

wo_lbl.close()
w_lbl.close()

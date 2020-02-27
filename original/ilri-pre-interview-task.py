#!/usr/bin/python3

# ILRI Pre-interview task
# Sam Larkin
# selarkin96@gmail.com
# +44 (0) 7599009273
# 2019-09-02 to 2019-09-04

### TASK GIVEN: 'calculate the categorical HFIAS indicator for all households' ###

import csv, re

### Read codebook csv file and extract the relevant section on HFIAS (9 questions); write the redacted version of the codebook to a csv file './outputs/HFIAS_codebook.csv'
with open('./provided/codebook for complete survey.csv') as codebook:
    codebook_read = csv.reader(codebook, delimiter=',')
    codebook_relevant = []
    line_count = 0
    for row in codebook_read:
        if line_count == 0:
            codebook_relevant.append(row)
        short_name = row[2]
        if re.search("HFIAS\S+", short_name):
            codebook_relevant.append(row)
        line_count += 1
#    print(codebook_relevant)
    with open("./outputs/HFIAS_codebook.csv",'w+') as HFIAS_codebook:
        wr = csv.writer(HFIAS_codebook, dialect='excel')
        wr.writerows(codebook_relevant)

### Read survey data csv file and extract the relevant responses to the 9 HFIAS questions; use these responses to calculate the categorical HFIAS indicator for each household; calculate the prevalence of each category; write results to csv files
with open('./provided/Full_Survey_Data_public.csv') as responses:
    responses_read = csv.reader(responses, delimiter=',')
#    responses_relevant = []
    columns_relevant = []
    hh_HFIA_cat = [['', 'hh_HFIA_cat', 'hh_HFIA_cat_full']]
    line_count = 0
    for row in responses_read:
        if line_count == 0:
            col_count = 0
            for col in row:
                if re.search("HFIAS\S+", col):
                    columns_relevant.append(col_count)
                col_count += 1
                line_count += 1
            a = int(columns_relevant[0])
            b = int(columns_relevant[len(columns_relevant)-1])+1
#            print(columns_relevant)
        else:
#            responses_relevant.append(row[a:b])
            hh = len(hh_HFIA_cat)
            HFIA_cat = 'NA'
            HFIA_cat_full = 'NA'
            ## Determine HFIA category variable for each household
            # HFIA category 1?
            if (row[b-1] == 'never' or row[b-1] == 'monthly') and row[a:b-1] == ['never','never','never','never','never','never','never','never']:
                HFIA_cat = 1
                HFIA_cat_full = 'Food.secure'
                # HFIA category 2?
            elif (row[b-1] == 'weekly' or row[b-1] == 'daily' or row[b-2] == 'monthly' or row[b-2] == 'weekly' or row[b-2] == 'daily' or row[b-3] == 'monthly' or row[b-4] == 'monthly') and row[a:b-4] == ['never', 'never', 'never', 'never', 'never']:
                HFIA_cat = 2
                HFIA_cat_full = 'Mildly.food.insecure.access'
                # HFIA category 3?
            elif (row[b-3] == 'weekly' or row[b-3] == 'daily' or row[b-4] == 'weekly' or row[b-4] == 'daily' or row[b-5] == 'monthly' or row[b-5] == 'weekly' or row[b-6] == 'monthly' or row[b-6] == 'weekly') and row[a:b-6] == ['never', 'never', 'never']:
                HFIA_cat = 3
                HFIA_cat_full = 'Moderately.food.insecure.access'
                # HFIA category 4?
            elif row[b-5] == 'daily' or row[b-6] == 'daily' or row[b-7] == 'monthly' or row[b-7] == 'weekly' or row[b-7] == 'daily' or row[b-8] == 'monthly' or row[b-8] == 'weekly' or row[b-8] == 'daily' or row[b-9] == 'monthly' or row[b-9] == 'weekly' or row[b-9] == 'daily':
                HFIA_cat = 4
                HFIA_cat_full = 'Severely.food.insecure.access'
            hh_HFIA_cat.append([hh, HFIA_cat, HFIA_cat_full])
#    print(hh_HFIA_cat, len(hh_HFIA_cat))
    with open("./outputs/hh_HFIA_cat.csv",'w+') as csv_hh_HFIA_cat:
        wr = csv.writer(csv_hh_HFIA_cat, dialect='excel')
        wr.writerows(hh_HFIA_cat)
#    print(responses_relevant)
    ## Prevalence of each level of HFIA
    instances_catx = [0, 0, 0, 0, 0]
    for row in hh_HFIA_cat:
        if row[1] == 'NA':
            instances_catx[0] += 1
        elif row[1] == 1:
            instances_catx[1] += 1
        elif row[1] == 2:
            instances_catx[2] += 1
        elif row[1] == 3:
            instances_catx[3] += 1
        elif row[1] == 4:
            instances_catx[4] += 1
    # Percentage of hh (which have a HFIA category) which fall in each of the 4 categories
    prevalence_catx = [(x/sum(instances_catx[0:]))*100 for x in instances_catx[0:]]
    # Percentage of the total hh surveyed which do not have a HFIA category (i.e. answered 'NA' to too many questions for the category to be determined
    prevalence_catx[0] = instances_catx[0]/sum(instances_catx)
#    print(instances_catx, prevalence_catx, sum(instances_catx), sum(instances_catx[1:4]), sum(instances_catx[1:]))
    with open("./outputs/HFIA_cat_prevalence.csv",'w+') as csv_HFIA_cat_prevalence:
        wr = csv.writer(csv_HFIA_cat_prevalence, dialect='excel')
        wr.writerow(['percent_no_category','prevalence_cat1','prevalence_cat2','prevalence_cat3','prevalence_cat4'])
        wr.writerow(prevalence_catx)

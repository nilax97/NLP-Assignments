import os
import ipdb
import sys

### Script to compute the mean reciprocal rank

def process_file(fp):
    fields_list = []
    for line in open(fp):
        line = line.strip('\n')
        fields = line.split()
        fields = [int(f) for f in fields]
        assert len(set(fields)) == len(fields), "Every word must be assigned a unqiue rank"
        fields_list.append(fields)

    return fields_list

def get_targets(fp):
    targets = []
    for line in open(fp,'r'):
        line = line.strip('\n')
        target = line.split('::::')[1]
        targets.append(target)

    return targets

def get_dict(fp):
    td = []
    for line in open(fp,'r'):
        line = line.strip('\n')
        td.append(line.split())

    return td

def main():
    data_fp = sys.argv[1] # The ground truth ranks of the words
    td_fp = sys.argv[2]
    pred_fp = sys.argv[3] # The predicted ranks of the words

    targets = get_targets(data_fp)
    td = get_dict(td_fp)
    pred_dist = process_file(pred_fp)

    assert len(td) == len(pred_dist), "Number of data points not matching"

    mrr = 0
    for i in range(len(td)):
        act = targets[i]
        act_index = td[i].index(act)
        pred_rank = pred_dist[i][act_index]
        mrr += 1./pred_rank

    mrr = mrr / len(td)
    print('Mean reciprocal rank = %f'%mrr)
    
if __name__ == "__main__":
    main()

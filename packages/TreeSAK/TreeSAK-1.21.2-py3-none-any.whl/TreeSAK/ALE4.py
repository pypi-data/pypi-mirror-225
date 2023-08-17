import os
import argparse


ALE4_usage = '''
===================================== ALE4 example commands =====================================

TreeSAK ALE4 -h

cd /Users/songweizhi/Desktop/333
python /Users/songweizhi/PycharmProjects/TreeSAK/TreeSAK/ALE4.py -i in_files -o ALE4_op_dir -f

=================================================================================================
'''


def ale_parser(rec_folder, SpeciesTreeRef_newick, TableInfo_tsv, TableEvents_tsv, GeneTrees_nwk):

    rec_files = [x for x in os.listdir(rec_folder) if x.endswith("uml_rec")]

    table_info = list()
    table_events = list()
    for rec_file in rec_files:
        with open(os.path.join(rec_folder, rec_file)) as f:
            fam = rec_file.replace(".ale.uml_rec", "")
            lines = f.readlines()
            stree = lines[2].strip()
            ll = lines[6].strip().split()[-1]
            dp, tp, lp = lines[8].strip().split("\t")[1:]
            n_reconciled_trees = int(lines[9].strip().split()[0])
            reconciled_trees = lines[11:n_reconciled_trees + 11]
            de, te, le, se = lines[11 + n_reconciled_trees + 1].split("\t")[1:]
            table = lines[11 + n_reconciled_trees + 3:]

        table_info.append((fam, ll, dp, tp, lp, de, te, le, se))
        table_events.append((fam, table))

    # write out SpeciesTreeRef.newick
    with open(SpeciesTreeRef_newick, "w") as f:
        f.write(stree.split("\t")[-1])

    # write out TableInfo.tsv
    with open(TableInfo_tsv, "w") as f:
        head = "\t".join(["Family", "LL", "Dp", "Tp", "Lp", "De", "Te", "Le", "Se"]) + "\n"
        f.write(head)
        for info in table_info:
            f.write("\t".join(info))

    # write out TableEvents.tsv
    with open(TableEvents_tsv, "w") as f:
        header = "Family\tBranchType\t" + table[0].replace("# of", "Branch")
        f.write(header)
        for fam, events in table_events:
            for b in events[1:]:
                f.write(fam + "\t" + b)

    # write out GeneTrees.nwk
    with open(GeneTrees_nwk, "w") as f:
        for t in reconciled_trees:
            f.write(t)


def ALE4(args):

    uml_rec_dir             = args['i']
    gene_presence_cutoff    = args['c']
    op_dir                  = args['o']
    force_create_op_dir     = args['f']

    if os.path.isdir(op_dir) is True:
        if force_create_op_dir is True:
            os.system('rm -r %s' % op_dir)
        else:
            print('Output folder detected, program exited!')
            exit()
    os.system('mkdir %s' % op_dir)

    SpeciesTreeRef_newick   = '%s/SpeciesTreeRef.newick'    % op_dir
    TableInfo_tsv           = '%s/TableInfo.tsv'            % op_dir
    TableEvents_tsv         = '%s/TableEvents.tsv'          % op_dir
    GeneTrees_nwk           = '%s/GeneTrees.nwk'            % op_dir

    ale_parser(uml_rec_dir, SpeciesTreeRef_newick, TableInfo_tsv, TableEvents_tsv, GeneTrees_nwk)

    col_index = {}
    for each_line in open(TableEvents_tsv):
        each_line_split = each_line.strip().split('\t')
        if each_line.startswith('Family'):
            col_index = {key: i for i, key in enumerate(each_line_split)}
        else:
            gene_family   = each_line_split[col_index['Family']]
            gene_presence = float(each_line_split[col_index['presence']])
            if gene_presence >= gene_presence_cutoff:
                print('%s\t%s' % (gene_family, gene_presence))





if __name__ == '__main__':

    ALE4_parser = argparse.ArgumentParser()
    ALE4_parser.add_argument('-i',   required=True,                              help='Folder with uml_rec files')
    ALE4_parser.add_argument('-c',   required=False, type=float, default=0.8,    help='gene family presence cutoff, default: 0.8')
    ALE4_parser.add_argument('-o',   required=True,                              help='output convergence plot')
    ALE4_parser.add_argument('-f',   required=False, action="store_true",        help='force overwrite')

    args = vars(ALE4_parser.parse_args())
    ALE4(args)

import typing

import pandas as pd
import tqdm

from cryoloBM.bmtool import BMTool
from argparse import ArgumentParser
import argparse
from typing import List
import numpy as np
from cryolo.utils import Filament, BoundBox
from cryolo.CoordsIO import read_star_file
from glob import glob
from pyStarDB import sp_pystardb as star
import tqdm
import os


class class_2d_extract(BMTool):

    def split_star(self, pth_star) -> typing.Dict[str,pd.DataFrame]:
        sfile = star.StarFile(pth_star)
        picks = sfile['particles']
        micrographs = picks['_rlnMicrographName']

        unique_mics = np.unique(micrographs)
        micrographs_np = micrographs.to_numpy()
        splitted_mics = {}
        for m in tqdm.tqdm(unique_mics):
            mask = micrographs_np==m
            splitted_mics[m] = picks.iloc[mask].copy()
        return splitted_mics

    def get_command_name(self) -> str:
        '''
        :return: Command name
        '''
        return "class2Dextract"

    def create_parser(self, parentparser: ArgumentParser) -> ArgumentParser:
        parser_autopick = parentparser.add_parser(
            self.get_command_name(),
            help="Extract coordinates from STAR files to make them usable for training with crYOLO.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        autopick_required_group = parser_autopick.add_argument_group(
            "Required arguments",
            "Extract coordinates from STAR files to make them usable for training with crYOLO.",
        )

        autopick_required_group.add_argument(
            "-s",
            "--star",
            required=True,
            help="Path to star file",
        )

        autopick_required_group.add_argument(
            "-o",
            "--out",
            required=True,
            help="Output path",
        )

        autopick_required_group.add_argument(
            "-n",
            "--number",
            required=False,
            type=int,
            default=-1,
            help="Return only n most crowded micrographs.",
        )

    def run(self, args):

        star_pth = args.star
        os.makedirs(args.out,exist_ok=True)
        splitted_star = self.split_star(star_pth)
        splitted_star = dict(sorted(splitted_star.items(), key=lambda item: -1*len(item[1])))
        # use  tqdm here...
        for t_num, t in tqdm.tqdm(enumerate(splitted_star)):
            if args.number > 0 and t_num >= args.number:
                break

            mic_name = os.path.splitext(os.path.basename(t))[0]
            data = splitted_star[t][['_rlnCoordinateX','_rlnCoordinateY']]
            out_pth = os.path.join(args.out, f"{mic_name}.star")
            new_sfile = star.StarFile(out_pth)
            new_sfile.update('', data, loop=True)
            new_sfile.write_star_file(overwrite=True)
            print(f"Wrote {len(data)} particle to {out_pth}")



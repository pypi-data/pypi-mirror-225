from cryoloBM.bmtool import BMTool
import argparse
from argparse import ArgumentParser
import os
from pyStarDB import sp_pystardb as star
import pandas as pd
from cryolo.CoordsIO import read_star_file
from typing import List
from cryolo.utils import BoundBox
class MakeCryoSparcStar(BMTool):

    def get_command_name(self) -> str:
        return "createCryoSparsStar"

    def create_parser(self, parentparser : ArgumentParser) -> ArgumentParser:
        parser_autopick = parentparser.add_parser(
            self.get_command_name(),
            help="Convert coordinates into a cryosparc STAR files.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        autopick_required_group = parser_autopick.add_argument_group(
            "Required arguments",
            "Create STAR file that can be imported into cryoSPARC.",
        )

        autopick_required_group.add_argument(
            "-m",
            "--micrographs",
            required=True,
            nargs='+',
            help="Folder to micrographs",
        )

        autopick_required_group.add_argument(
            "-c",
            "--coordinates",
            required=True,
            nargs='+',
            help="Folder to star files from crYOLO",
        )

        autopick_required_group.add_argument(
            "-o",
            "--output",
            required=True,
            help="Output folder where to write the autopick.star.",
        )

    def run(self, args):
        micrographs = args.micrographs
        coordinates = args.coordinates


        micrographs_filename = [os.path.splitext(os.path.basename(m))[0] for m in micrographs]
        coordinates_filename = [os.path.splitext(os.path.basename(m))[0] for m in coordinates]

        micrographs_mapped = []
        coordinates_mapped = []
        for m_i,m in enumerate(micrographs_filename):
            try:
                index = coordinates_filename.index(m)

                micrographs_mapped.append(micrographs[m_i])
                coordinates_mapped.append(coordinates[index])
            except ValueError:
                print("Did not found matching coordinate file for ", micrographs[m_i])

        coords_x = []
        coords_y = []
        micrograph_names = []
        for c_i, coords_pth in enumerate(coordinates_mapped):
            coordinates: List[BoundBox] = read_star_file(coords_pth,box_size=0)
            for box in coordinates:
                micrograph_names.append(os.path.basename(micrographs_mapped[c_i]))
                coords_x.append(box.x)
                coords_y.append(box.y)

        data_dict = {'_rlnMicrographName': micrograph_names, '_rlnCoordinateX': coords_x, '_rlnCoordinateY': coords_y}
        data = pd.DataFrame(data_dict)

        new_sfile = star.StarFile(os.path.join(args.output,"cryosparc_pick.star"))
        new_sfile.update('', data, loop=True)
        new_sfile.write_star_file(overwrite=True)



        pass
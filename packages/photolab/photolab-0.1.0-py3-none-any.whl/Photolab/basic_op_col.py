
import numpy as np

class color_operations(object):

    def __init__(self,photo) -> None:
        self.photo = photo
        return None

    def invert (self):

        photo = self.photo
        new = []
        avg = np.average(photo)
        for i in photo :
            row = []
            for j in i :
                row.append(255-j)
                new.append(row)

        new = np.array(new)

        return new


    def col_slice_mask (self,offr1: 'int', offr2: 'int',offg1: 'int', offg2: 'int',offb1: 'int', offb2: 'int' ):

        photo = self.photo
        new = []
        avg = np.average(photo)
        for i in photo :
            row = []
            for j in i :
                pix = []
                if j[0] >= offb1 and j[0] <= offb2 :
                    pix.append(j[0])
                else :
                    pix.append(0)
                if j[1] >= offg1 and j[1] <= offg2 :
                    pix.append(j[1])
                else :
                    pix.append(0)
                if j[2] >= offr1 and j[2] <= offr2 :
                    pix.append(j[2])
                else :
                    pix.append(0)

                row.append(pix)

            new.append(row)

        new = np.array(new)

        return new



    def col_slice_bg (self,offr1: 'int', offr2: 'int',offg1: 'int', offg2: 'int',offb1: 'int', offb2: 'int' ):

        photo = self.photo
        new = []
        avg = np.average(photo)
        for i in photo :
            row = []
            for j in i :
                pix = []
                if j[0] >= offb1 and j[0] <= offb2 :
                    pix.append(255)
                else :
                    pix.append(j[0])
                if j[1] >= offg1 and j[1] <= offg2 :
                    pix.append(255)
                else :
                    pix.append(j[1])
                if j[2] >= offr1 and j[2] <= offr2 :
                    pix.append(255)
                else :
                    pix.append(j[2])

                row.append(pix)

            new.append(row)

        new = np.array(new)

        return new



    def col_threshold (self,offr:'int',offg:'int',offb:'int'):

        photo = self.photo
        new = []
        avg = np.average(photo)
        for i in photo :
            row = []
            for j in i :
                pix = []
                if j[0] >= offb:
                    pix.append(255)
                else :
                    pix.append(0)
                if j[1] >= offg:
                    pix.append(255)
                else :
                    pix.append(0)
                if j[2] >= offr:
                    pix.append(255)
                else :
                    pix.append(0)
                row.append(pix)
            new.append(row)

        new = np.array(new)

        return new

    def col_threshold_bg (self,offr:'int',offg:'int',offb:'int'):

        photo = self.photo
        new = []
        avg = np.average(photo)
        for i in photo :
            row = []
            for j in i :
                pix = []
                if j[0] >= offb:
                    pix.append(255)
                else :
                    pix.append(j[0])
                if j[1] >= offg:
                    pix.append(255)
                else :
                    pix.append(j[1])
                if j[2] >= offr:
                    pix.append(255)
                else :
                    pix.append(j[2])
                row.append(pix)
            new.append(row)

        new = np.array(new)

        return new

    def col_threshold_mask (self,offr:'int',offg:'int',offb:'int'):

        photo = self.photo
        new = []
        avg = np.average(photo)
        for i in photo :
            row = []
            for j in i :
                pix = []
                if j[0] >= offb:
                    pix.append(j[0])
                else :
                    pix.append(0)
                if j[1] >= offg:
                    pix.append(j[1])
                else :
                    pix.append(0)
                if j[2] >= offr:
                    pix.append(j[2])
                else :
                    pix.append(0)
                row.append(pix)
            new.append(row)

        new = np.array(new)

        return new




from src.load_optimiser_core.constants import RotationType, Axis
from .auxiliary_methods import set2Decimal

cdef int DEFAULT_NUMBER_OF_DECIMALS = 0
cdef int[3] START_POSITION = [0, 0, 0]


cdef class Item:
    cdef public object partno
    cdef public object name
    cdef public object type_of
    cdef public float width
    cdef public float height
    cdef public float depth
    cdef public object weight
    cdef public int level
    cdef public int loadbear
    cdef public bint updown
    cdef public object color
    cdef public int rotation_type
    cdef public int[3] position
    cdef public int number_of_decimals

    def __init__(self, partno, name, type_of, WHD, weight, level, loadbear, updown, color):
        self.partno = partno
        self.name = name
        self.type_of = type_of
        self.width = WHD[0]
        self.height = WHD[1]
        self.depth = WHD[2]
        self.weight = weight
        # Packing Priority level ,choose 1-3
        self.level = level
        # loadbear
        self.loadbear = loadbear
        # Upside down? True or False
        self.updown = updown if type_of == 'cube' else False
        # Draw item color
        self.color = color
        self.rotation_type = 0
        self.position = START_POSITION
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS

    def formatNumbers(self, number_of_decimals):
        ''' '''
        self.width = set2Decimal(self.width, number_of_decimals)
        self.height = set2Decimal(self.height, number_of_decimals)
        self.depth = set2Decimal(self.depth, number_of_decimals)
        self.weight = set2Decimal(self.weight, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def string(self):
        ''' '''
        return "%s(%sx%sx%s, weight: %s) pos(%s) rt(%s) vol(%s)" % (
            self.partno, self.width, self.height, self.depth, self.weight,
            self.position, self.rotation_type, self.getVolume()
        )

    def getVolume(self):
        ''' '''
        return set2Decimal(self.width * self.height * self.depth, self.number_of_decimals)

    def getMaxArea(self):
        ''' '''
        a = sorted([self.width, self.height, self.depth], reverse=True) if self.updown == True else [self.width,
                                                                                                     self.height,
                                                                                                     self.depth]

        return set2Decimal(a[0] * a[1], self.number_of_decimals)

    def getDimension(self):
        ''' rotation type '''
        if self.rotation_type == RotationType.RT_WHD:
            dimension = [self.width, self.height, self.depth]
        elif self.rotation_type == RotationType.RT_HWD:
            dimension = [self.height, self.width, self.depth]
        elif self.rotation_type == RotationType.RT_HDW:
            dimension = [self.height, self.depth, self.width]
        elif self.rotation_type == RotationType.RT_DHW:
            dimension = [self.depth, self.height, self.width]
        elif self.rotation_type == RotationType.RT_DWH:
            dimension = [self.depth, self.width, self.height]
        elif self.rotation_type == RotationType.RT_WDH:
            dimension = [self.width, self.depth, self.height]
        else:
            dimension = []

        return dimension
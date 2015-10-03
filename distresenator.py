import png
import argparse
from png import Writer
from random import random, randint


def color(percent=0.5):
    return random() > percent

def colored_tuple():
    return (randint(145,225), randint(200,255))

def build(width, height, percent):
    return [[(0, 0) if color(percent) else colored_tuple() for _ in range(width)] for _ in range(height)]

def add_clump(m, i, j):
    for r in [i-1, i, i+1]:
        for c in [j-1, j, j+1]:
            m[r][c] = m[i][j]
    
def clump(matrix, match_value=255, cluster_coeficient=0.8):
    for i in range(1, len(matrix) - 1):
        for j in range(1, max(map(len, matrix)) - 1):
            if matrix[i][j][1] == match_value and random() > cluster_coeficient:
                add_clump(matrix, i, j)
    return matrix

def clump_times(matrix, times=1, match_value=255, cluster_coeficient=0.8):
    for _ in range(times):
        matrix = clump(matrix, match_value, cluster_coeficient)
    return matrix


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates png layer of greyscale speckles')
    parser.add_argument('out_file', help='file name to output to')
    parser.add_argument('width', type=int, help='width of image in pixels')
    parser.add_argument('height', type=int, help='height of image in pixels')
    parser.add_argument('percent', type=float, help='percent pixels to color')
    parser.add_argument('clumpiness', type=float, help='float representing how clumpy to be')
    parser.add_argument('clump_iter', type=int, help='number of times to clump')
    args = parser.parse_args()
    mt = build(args.width, args.height, args.percent)
    mt_clumped = clump_times(mt, args.clump_iter, cluster_coeficient=args.clumpiness)
    png.from_array(mt_clumped, 'LA').save(args.out_file)
